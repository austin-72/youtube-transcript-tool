"""Command-line interface.

    python yt.py run                     search + list + transcripts using config.toml
    python yt.py run -k "ai agents" -k "claude code" --min-views 50000 --within week
    python yt.py search -k "python tutorial"     # only build the list
    python yt.py transcripts output/video_list.csv   # transcripts for an existing list
    python yt.py channel @mkbhd --max 50  # transcripts for a channel's newest 50 videos (0 = all)
    python yt.py related "ai agents"      # find related keywords to search for
    python yt.py doctor                  # check that everything is installed and YouTube is reachable
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys
from contextlib import contextmanager
from pathlib import Path

from . import __version__
from .config import Settings, build_settings, load_config, read_keywords_file
from .utils import format_duration, setup_logging

log = logging.getLogger("yt_transcripts")
PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = PROJECT_DIR / "config.toml"


def _bool_flag(p: argparse.ArgumentParser, name: str, help_on: str, help_off: str | None = None) -> None:
    dest = name.replace("-", "_")
    g = p.add_mutually_exclusive_group()
    g.add_argument(f"--{name}", dest=dest, action="store_true", default=None, help=help_on)
    g.add_argument(f"--no-{name}", dest=dest, action="store_false", default=None, help=help_off or argparse.SUPPRESS)


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-c", "--config", default=None, help="config file (default: config.toml next to yt.py)")
    common.add_argument("-o", "--output-dir", help="where lists and transcripts are saved (default: output)")
    common.add_argument("-v", "--verbose", action="store_true", default=None, help="show debug output")
    common.add_argument("--delay", dest="delay_seconds", type=float, help="seconds between videos (default 5)")
    common.add_argument("--workers", help='parallel downloads: "auto" (one per proxy) or a number')
    common.add_argument("--workers-per-proxy", type=int, help="workers sharing one proxy (rotating services)")
    common.add_argument("--per-hour", dest="videos_per_hour_per_ip", type=int,
                        help="most videos per hour through one IP (default 200, 0 = no cap)")
    common.add_argument("--cookies", dest="cookies_file", help="cookies.txt (Netscape format) to send to YouTube")
    common.add_argument("--cookies-from-browser", help="read YouTube cookies from a browser: firefox, chrome, edge...")
    common.add_argument("--proxy", help="proxy, e.g. http://user:pass@host:port (several: separate with spaces)")
    common.add_argument("--proxy-file", help="text file with one proxy per line; a blocked proxy is swapped "
                                             "for the next")
    _bool_flag(common, "open", "open the HTML video list when finished")
    common.add_argument("--search-direct", dest="proxy_for_search", action="store_false", default=None,
                        help="search over your own connection (proxies only for the transcripts)")
    common.add_argument("--transcripts-direct", dest="proxy_for_transcripts", action="store_false", default=None,
                        help="download transcripts over your own connection")
    common.add_argument("--data-saver", choices=["auto", "on", "off", "max"],
                        help="fewer bytes per video through proxies (default auto = on with proxies)")
    common.add_argument("--data-limit", dest="proxy_limit_run_mb", type=float, metavar="MB",
                        help="stop starting new videos after this much proxy data in this run")
    common.add_argument("--month-limit", dest="proxy_limit_month_mb", type=float, metavar="MB",
                        help="...or after this much proxy data in the current month")

    search_opts = argparse.ArgumentParser(add_help=False)
    g = search_opts.add_argument_group("search")
    g.add_argument("-k", "--keyword", dest="keyword_list", action="append", help="search term (repeatable)")
    g.add_argument("--keywords-file", help="text file with one search term per line")
    g.add_argument("-m", "--min-views", type=int, help="minimum view count (default 10000)")
    g.add_argument("--max-views", type=int, help="skip videos with more views than this")
    g.add_argument("--after", dest="published_after", metavar="DATE",
                   help="only videos uploaded on/after this date, e.g. 2026-10-01")
    g.add_argument("--before", dest="published_before", metavar="DATE", help="...and on/before this date")
    g.add_argument("--rising", dest="rising_views_per_day", type=int,
                   help="also keep videos under --min-views that get at least this many views per day")
    g.add_argument("-w", "--within", choices=["today", "week", "month", "year", "any"],
                   help="only videos uploaded within this window (default month)")
    g.add_argument("--max-age-days", type=float, help="finer age limit in days, e.g. 3")
    g.add_argument("-n", "--max-results", type=int, help="keep the newest N matching videos per keyword (0 = all)")
    g.add_argument("--scan", dest="scan_per_keyword", type=int, help="search results to scan per keyword (default 150)")
    g.add_argument("--backend", choices=["auto", "ytdlp", "api"], help="search with yt-dlp (no key) or the YouTube Data API")
    g.add_argument("--api-key", help="YouTube Data API v3 key (or set YOUTUBE_API_KEY)")
    g.add_argument("--min-duration", type=int, help="minimum length in seconds")
    g.add_argument("--max-duration", type=int, help="maximum length in seconds")
    _bool_flag(g, "include-shorts", "include YouTube Shorts")
    _bool_flag(g, "subtitles-only", "only videos with uploaded (non-auto) captions")
    _bool_flag(g, "exact-dates", "look up exact upload dates (slower)")

    tr_opts = argparse.ArgumentParser(add_help=False)
    t = tr_opts.add_argument_group("transcripts")
    t.add_argument("-l", "--lang", dest="languages", action="append", help="preferred transcript language (repeatable, default en)")
    t.add_argument("-f", "--format", dest="formats", action="append",
                   choices=["txt", "md", "srt", "vtt", "json"], help="output format (repeatable, default txt + json)")
    t.add_argument("--organize-by", choices=["keyword", "channel", "month", "flat"], help="folder layout for transcripts")
    t.add_argument("--methods", dest="transcript_methods", help="comma list, e.g. ytdlp or api,ytdlp")
    _bool_flag(t, "timestamps", "put [mm:ss] timestamps in the .txt files")
    _bool_flag(t, "allow-other-languages", "fall back to the video's own language if the preferred one is missing")
    _bool_flag(t, "translate", "if your language is missing, use YouTube's machine translation into it")
    _bool_flag(t, "retry-failed", "retry videos that previously had no transcript / were unavailable")
    _bool_flag(t, "combine", "also write one combined Markdown file per run")

    p = argparse.ArgumentParser(
        prog="yt.py",
        description="Search YouTube for keywords, keep the newest videos above a view threshold, "
                    "save the list, and download their transcripts.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command")
    sub.add_parser("run", parents=[common, search_opts, tr_opts], help="search, save the list, download transcripts")
    sub.add_parser("search", parents=[common, search_opts], help="search and save the list only")
    tp = sub.add_parser("transcripts", parents=[common, tr_opts], help="download transcripts for an existing list")
    tp.add_argument("list_file", nargs="+", metavar="LIST_OR_URL",
                    help="video_list.csv / .json, a .txt file of YouTube URLs or IDs, or the URLs/IDs themselves")
    cp = sub.add_parser("channel", parents=[common, tr_opts],
                        help="transcripts for every video of one or more channels (or playlists)")
    cp.add_argument("channel_specs", nargs="*", metavar="CHANNEL",
                    help="@handle, channel link, channel ID or playlist link (default: `channels` in config.toml)")
    cp.add_argument("--tabs", dest="channel_tabs", help="comma list of videos, shorts, streams (default videos)")
    cp.add_argument("-n", "--max", dest="channel_max_videos", type=int, help="newest N videos per channel (0 = all)")
    cp.add_argument("-m", "--min-views", dest="channel_min_views", type=int, help="minimum views (default 0)")
    cp.add_argument("-w", "--within", dest="channel_within", choices=["today", "week", "month", "year", "any"],
                    help="only videos uploaded within this window (default any)")
    cp.add_argument("--after", dest="published_after", metavar="DATE", help="only videos uploaded on/after this date")
    cp.add_argument("--before", dest="published_before", metavar="DATE", help="...and on/before this date")
    cp.add_argument("--min-duration", type=int, help="minimum length in seconds")
    cp.add_argument("--max-duration", type=int, help="maximum length in seconds")
    cp.add_argument("--list-only", action="store_true", help="only make the list, no transcripts")
    rp = sub.add_parser("related", parents=[common], help="find related keywords to search for")
    rp.add_argument("seeds", nargs="*", metavar="KEYWORD", help="keyword(s) to start from (default: your keywords)")
    rp.add_argument("--max", dest="related_max", type=int, default=40, help="how many to show (default 40)")
    rp.add_argument("--no-titles", dest="related_titles", action="store_false", default=True,
                    help="don't run a YouTube search to mine video titles (suggestions only)")
    rp.add_argument("--add", dest="related_add", type=int, default=0, metavar="N",
                    help="add the top N to the keywords in config.toml")
    dp = sub.add_parser("doctor", parents=[common], help="check installation and connectivity")
    dp.add_argument("--video", default="dQw4w9WgXcQ", help="video ID to test transcript download with")
    sub.add_parser("gui", parents=[common], help="open the simple window interface")
    sub.add_parser("status", parents=[common], help="show what has been downloaded so far")
    sub.add_parser("export", parents=[common],
                   help="bundle all transcripts into one .jsonl and one .csv (for AI tools / spreadsheets)")
    fp = sub.add_parser("find", parents=[common], help="search the downloaded transcripts for words or a phrase")
    fp.add_argument("phrase", help='what to look for, e.g. "context window"')
    fp.add_argument("--max", dest="max_hits", type=int, default=200, help="stop after this many matches")
    sub.add_parser("init", help="create config.toml from the example")
    up = sub.add_parser("selfupdate", help="update yt-dlp and youtube-transcript-api (used by the daily task)")
    up.add_argument("--if-older-than", type=float, default=0, metavar="DAYS",
                    help="only if the last update was more than DAYS ago")
    return p


def settings_from_args(args: argparse.Namespace) -> Settings:
    cfg_path = args.config or (DEFAULT_CONFIG if DEFAULT_CONFIG.exists() else None)
    if args.config and not Path(args.config).exists() and getattr(args, "command", "") != "gui":
        from .config import ConfigError

        raise ConfigError(f"The settings file {args.config} does not exist.")
    config = load_config(cfg_path)
    ov = {k: v for k, v in vars(args).items() if v is not None}
    for k in ("command", "config", "list_file", "keyword_list", "keywords_file", "video", "phrase", "max_hits",
              "channel_specs", "list_only", "seeds", "related_max", "related_titles", "related_add"):
        ov.pop(k, None)
    if isinstance(ov.get("channel_tabs"), str):
        ov["channel_tabs"] = [t.strip().lower() for t in ov["channel_tabs"].split(",") if t.strip()]
    if "open" in ov:
        ov["open_list_when_done"] = ov.pop("open")
    if "timestamps" in ov:
        ov["txt_timestamps"] = ov.pop("timestamps")
    if isinstance(ov.get("transcript_methods"), str):
        ov["transcript_methods"] = [m.strip() for m in ov["transcript_methods"].split(",") if m.strip()]
    kws = list(getattr(args, "keyword_list", None) or [])
    if getattr(args, "keywords_file", None):
        kws += read_keywords_file(args.keywords_file)
    if kws:
        ov["keywords"] = kws
    elif config.get("keywords_file"):  # file keywords are added to the `keywords` list (duplicates dropped)
        listed = config.get("keywords") or []
        if isinstance(listed, str):  # "a, b" -> ["a", "b"], same as without keywords_file
            listed = [x.strip() for x in listed.split(",") if x.strip()]
        config["keywords"] = list(listed) + read_keywords_file(_rel(config["keywords_file"]))
    config.pop("keywords_file", None)
    s = build_settings(config, ov)
    cli_proxy, cli_file = getattr(args, "proxy", None), getattr(args, "proxy_file", None)
    if cli_proxy or cli_file:  # proxies given on the command line replace the ones in config.toml
        s.proxies = []
        s.proxy = cli_proxy or ""
        s.proxy_file = str(Path(cli_file).resolve()) if cli_file else ""  # relative to where you are
    from .proxies import resolve as resolve_proxies

    resolve_proxies(s, PROJECT_DIR)  # raises ConfigError for a missing proxy_file
    # relative output dir is relative to the project folder, so double-clicking works
    s.output_dir = str(_rel(s.output_dir))
    if s.cookies_file:
        s.cookies_file = str(_rel(s.cookies_file))
    for k in getattr(s, "_unknown_keys", []):
        print(f"warning: unknown setting {k!r} in config ignored", file=sys.stderr)
    for msg in getattr(s, "_coerce_problems", []):
        print(f"warning: {msg}", file=sys.stderr)
    return s


def _rel(p: str) -> Path:
    path = Path(p).expanduser()
    return path if path.is_absolute() else PROJECT_DIR / path


LIST_PRINTER = print  # the window interface swaps this for its log


def print_list(videos, limit: int = 50) -> None:
    out = LIST_PRINTER
    if not videos or (out is print and sys.stdout is None):
        return
    out("")
    out(f"{'Published':<11} {'Views':>11}  {'Length':>8}  Title / Channel")
    out("-" * 100)
    for v in videos[:limit]:
        pub = (v.published[:10] if v.published else "?") + ("" if v.published_exact else "~")
        views = f"{v.views:,}" if v.views is not None else "?"
        new = "NEW " if v.is_new else ""
        out(f"{pub:<11} {views:>11}  {format_duration(v.duration_seconds):>8}  {new}{v.title[:60]}  -  {v.channel[:25]}")
    if len(videos) > limit:
        out(f"... and {len(videos) - limit} more (see the CSV)")
    out("(~ = approximate date from YouTube's 'x days ago' text)\n")


def _library(s: Settings, out: Path):
    """Rebuild library.html; never let a problem there spoil the run."""
    from .writers import write_library

    try:
        return write_library(out, s)
    except Exception as e:  # noqa: BLE001
        log.debug("library.html not updated: %s", e)
        return None


@contextmanager
def metered(s: Settings, label: str):
    """Count proxy data for this run (or join the run that's already counting) and report it at the end."""
    from . import netmeter

    if netmeter.active() is not None:
        yield netmeter.active()
        return
    with netmeter.Session(s, label) as sess:
        try:
            yield sess
        finally:
            line = sess.summary()
            if line:
                log.info(line)


def cmd_search(s: Settings, save: bool = True, should_stop=None, channels: list[str] | None = None):
    with metered(s, "channels" if channels else "search"):
        return _cmd_search(s, save, should_stop, channels)


def _cmd_search(s: Settings, save: bool = True, should_stop=None, channels: list[str] | None = None):
    from .search import rank_newest, run_search
    from .writers import write_video_list

    problems = s.validate()
    if channels:  # `yt.py channel ...`: keywords aren't needed
        problems = [p for p in problems if not p.startswith("No keywords")]
    if not problems:
        from .ytdlp_common import warn_if_stale

        warn_if_stale(log)
    if problems:
        for pr in problems:
            log.error(pr)
        return None, None
    stem = "channel_list" if channels else "video_list"
    if channels:
        from .channels import run_channels

        videos = run_channels(s, channels, should_stop=should_stop)
    else:
        videos = run_search(s, should_stop=should_stop) if s.all_keywords() else []
        if s.channels and not (should_stop and should_stop()):
            from .channels import run_channels

            seen = {v.video_id: v for v in videos}
            for v in run_channels(s, should_stop=should_stop):
                if v.video_id in seen:
                    seen[v.video_id].merge(v)
                else:
                    videos.append(v)
            videos = rank_newest(videos)
    from .search import sort_for_list

    videos = sort_for_list(videos, s.list_sort)
    global LAST_STEM
    LAST_STEM = stem
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    paths = None
    if save:
        from .writers import mark_new

        from .pipeline import apply_manifest

        out = Path(s.output_dir)
        apply_manifest(videos, s)  # links to transcripts from earlier runs, even if this run stops early
        n_new = mark_new(videos, out)
        if n_new:
            log.info("%d of them are new since your last search.", n_new)
        from .report import search_summary

        summary = search_summary(s, channels)
        write_video_list(videos, out / "lists", f"{stamp}_{stem}", summary)
        paths = write_video_list(videos, out, stem, summary)
        global LAST_LIST_HTML
        LAST_LIST_HTML = paths["html"]
        _library(s, out)
        log.info("Saved list of %d videos: %s", len(videos), paths["csv"].resolve())
    print_list(videos)
    return videos, stamp


LAST_LIST_HTML: Path | None = None
LAST_STEM = "video_list"

_STAT_LABELS = {
    "ok": "transcripts saved", "skipped": "already done (skipped)", "no_transcript": "without captions",
    "unavailable": "unavailable (private/removed/members-only)", "blocked": "blocked by YouTube (will retry)",
    "error": "failed (will retry)", "left_for_next_run": "left for the next run",
    "po_token": "need a YouTube token (retried on a schedule)",
    "stopped_blocked": "run stopped early: YouTube blocking", "stopped_errors": "run stopped early: repeated errors",
    "interrupted": "run interrupted", "stopped_data_limit": "run stopped: proxy data limit reached",
}


def summarize_stats(stats) -> str:
    parts = []
    for k, n in stats.most_common():
        label = _STAT_LABELS.get(k, k.replace("_", " "))
        parts.append(label if k.startswith(("stopped", "interrupted")) else f"{n} {label}")
    return ", ".join(parts)


def cmd_selfupdate(if_older_than_days: float = 0, runner=None) -> int:
    """pip-upgrade the YouTube libraries (YouTube changes often; new yt-dlp releases follow within days)."""
    import subprocess
    import time

    stamp = PROJECT_DIR / ".last_update"
    try:
        age_days = (time.time() - stamp.stat().st_mtime) / 86400
    except OSError:
        age_days = float("inf")
    if if_older_than_days and age_days < if_older_than_days:
        print(f"Libraries were updated {age_days:.1f} days ago - nothing to do.")
        return 0
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--quiet", "-r", str(PROJECT_DIR / "requirements.txt")]
    print("Updating yt-dlp and youtube-transcript-api ...")
    rc = (runner or subprocess.call)(cmd)
    if rc == 0:
        stamp.write_text(time.strftime("%Y-%m-%d %H:%M"), encoding="utf-8")
        print("Up to date.")
    else:
        print("Update failed (no internet?) - the run continues with the installed versions.")
    return 0 if rc == 0 else 1


def _load_list_args(items) -> tuple[list | None, str]:
    """Videos from list files and/or URLs/IDs given on the command line (or one path from the window)."""
    from .models import Video
    from .writers import _extract_id, read_video_list

    items = [items] if isinstance(items, (str, Path)) else list(items)
    split: list[str] = []
    for item in items:  # get_transcript.bat passes all pasted links as one argument
        item = str(item).strip()
        split += [item] if Path(item).exists() or _rel(item).exists() else item.split()
    items = split
    videos, seen, labels = [], set(), []
    for item in items:
        item = str(item).strip()
        p = Path(item) if Path(item).exists() else _rel(item)
        if p.is_file():
            got = read_video_list(p)
            for v in got:  # so transcripts land in a folder named after the list
                v.keyword = v.keyword or p.stem
            log.info("Loaded %d videos from %s", len(got), p)
            labels.append(str(p))
        elif _extract_id(item):
            got = [Video(video_id=_extract_id(item), source="command-line", keyword="single videos")]
            labels.append(item)
        else:
            log.error("%r is neither a list file that exists nor a YouTube link/ID.", item)
            return None, item
        for v in got:
            if v.video_id not in seen:
                seen.add(v.video_id)
                videos.append(v)
    return videos, ", ".join(labels)


def cmd_run(s: Settings, transcripts_only_list: str | None = None, should_stop=None,
            channels: list[str] | None = None) -> int:
    label = "transcripts" if transcripts_only_list else "channels" if channels else "run"
    with metered(s, label):
        return _cmd_run(s, transcripts_only_list, should_stop, channels)


def _cmd_run(s: Settings, transcripts_only_list: str | None = None, should_stop=None,
             channels: list[str] | None = None) -> int:
    from .pipeline import download_all
    from .writers import write_video_list

    if transcripts_only_list:
        videos, label = _load_list_args(transcripts_only_list)
        if videos is None:
            return 1
        from .pipeline import apply_manifest

        for v in videos:  # a saved list's transcript columns may be stale: the manifest is the record
            v.transcript_status = v.transcript_language = v.transcript_kind = v.transcript_file = ""
            v.keyword_mentions = None
        apply_manifest(videos, s)
        stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
        if not videos:
            log.error("No videos found in %s", label)
            return 1
        bad = [p for p in s.validate() if not p.startswith("No keywords")]
        if bad:
            for pr in bad:
                log.error(pr)
            return 2
    else:
        videos, stamp = cmd_search(s, should_stop=should_stop, channels=channels)
        if videos is None:
            return 2
        if not videos:
            if channels:
                log.warning("No videos matched on those channels. Try channel_within = \"any\", a lower "
                            "channel_min_views, or other channel_tabs.")
            else:
                log.warning("No videos matched. In config.toml (or the window) try a lower min_views, a wider "
                            "within, or a bigger scan_per_keyword.")
            return 0
    if not s.download_transcripts and not transcripts_only_list:  # asking for transcripts overrides the setting
        if s.open_list_when_done and not transcripts_only_list:
            _open_file(LAST_LIST_HTML or Path(s.output_dir) / f"{LAST_STEM}.html")
        return 0
    if should_stop and should_stop():
        return 130
    stats = download_all(videos, s, run_stamp=stamp, should_stop=should_stop)
    out = Path(s.output_dir)
    # update the lists with transcript status / file paths
    if transcripts_only_list:
        write_video_list(videos, out / "lists", f"{stamp}_transcripts_list")
    else:
        from .report import search_summary
        from .search import sort_for_list

        videos = sort_for_list(videos, s.list_sort)  # exact dates learned while fetching may change the order
        summary = search_summary(s, channels)
        stem = "channel_list" if channels else "video_list"
        write_video_list(videos, out / "lists", f"{stamp}_{stem}", summary)
        html = write_video_list(videos, out, stem, summary)["html"]
    lib = _library(s, out)
    summary = summarize_stats(stats)
    log.info("Done: %s", summary or "nothing to do")
    if lib:
        log.info("Every video so far (all runs): %s", lib.resolve())
    log.info("Transcripts folder: %s", (out / "transcripts").resolve())
    if s.open_list_when_done and not transcripts_only_list:
        _open_file(html)
    return 0


def _open_file(path: Path) -> None:
    import os
    import webbrowser

    try:
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            webbrowser.open(path.resolve().as_uri())
    except Exception as e:
        log.debug("could not open %s: %s", path, e)


def _safe_console() -> None:
    """Titles contain emoji and every script; never crash when the console can't show them."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")  # type: ignore[union-attr]
        except Exception:
            pass


def cmd_find(s: Settings, phrase: str, max_hits: int = 200, out=None) -> int:
    """Search the .json transcripts (they keep timings) and print timestamped links."""
    import json
    import re

    import builtins

    print = out or builtins.print  # noqa: A001 - lets the window interface capture the output
    from .utils import format_ts

    root = Path(s.output_dir) / "transcripts"
    files = sorted(root.rglob("*.json")) if root.exists() else []
    if not files:
        print("No .json transcripts found - keep \"json\" in formats to make transcripts searchable.")
        return 1
    words = phrase.lower().split()
    pattern = re.compile(r"\s+".join(re.escape(w) for w in words), re.I)
    hits = videos = 0
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        segs = data.get("transcript", {}).get("segments", [])
        video = data.get("video", {})
        found_here = []
        # look across neighbouring segments so phrases split over two caption lines still match
        for i, seg in enumerate(segs):
            window = " ".join(x["text"] for x in segs[i:i + 2])
            m = pattern.search(window)
            if m and (m.start() < len(seg["text"]) or i == len(segs) - 1):
                found_here.append(seg)
        if not found_here:
            continue
        videos += 1
        print(f"\n{video.get('title', f.stem)}  -  {video.get('channel', '')}")
        for seg in found_here:
            hits += 1
            t = int(seg["start"])
            text = seg["text"]
            print(f"  [{format_ts(seg['start'])}] {text[:110]}")
            print(f"      https://youtu.be/{video.get('video_id', '')}?t={t}")
            if hits >= max_hits:
                print(f"\n(stopped after {max_hits} matches)")
                return 0
    print(f"\n{hits} match(es) in {videos} video(s) for {phrase!r}." if hits else f"No matches for {phrase!r}.")
    return 0


def cmd_export(s: Settings) -> int:
    """One JSON object per line (metadata + full text + segments) and a CSV with one row per video."""
    import csv
    import io
    import json

    root = Path(s.output_dir)
    files = sorted((root / "transcripts").rglob("*.json")) if (root / "transcripts").exists() else []
    if not files:
        print("No .json transcripts found - keep \"json\" in formats so they can be exported.")
        return 1
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    out_dir = root / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = out_dir / f"all_transcripts_{stamp}.jsonl"
    csv_path = out_dir / f"all_transcripts_{stamp}.csv"
    cols = ["video_id", "title", "channel", "published", "views", "duration_seconds", "keyword", "url",
            "language", "kind", "words", "text"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    n = 0
    with jsonl_path.open("w", encoding="utf-8") as jf:
        for f in files:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            v, t = data.get("video", {}), data.get("transcript", {})
            row = {**{k: v.get(k, "") for k in cols}, "language": t.get("language", ""), "kind": t.get("kind", ""),
                   "text": t.get("text", ""), "words": len(t.get("text", "").split())}
            jf.write(json.dumps({**row, "segments": t.get("segments", [])}, ensure_ascii=False) + "\n")
            w.writerow(row)
            n += 1
    csv_path.write_text(buf.getvalue(), encoding="utf-8-sig")
    print(f"Exported {n} transcripts:\n  {jsonl_path.resolve()}\n  {csv_path.resolve()}")
    return 0


def cmd_status(s: Settings) -> int:
    import json
    from collections import Counter

    out = Path(s.output_dir)
    mf = out / "manifest.json"
    if not mf.exists():
        print(f"Nothing downloaded yet (looked in {out}).")
        from .netmeter import usage_report

        for line in usage_report(out, s):
            print(line)
        return 0
    data = json.loads(mf.read_text(encoding="utf-8"))
    counts = Counter(rec.get("status", "?") for rec in data.values())
    labels = {"ok": "transcripts saved", "no_transcript": "videos without captions",
              "unavailable": "unavailable videos", "error": "failed (will retry next run)",
              "blocked": "blocked by YouTube (will retry next run)",
              "po_token": "need a YouTube token (retried on a schedule: 6 h, 1 day, 3 days, weekly)"}
    print(f"\nOutput folder: {out.resolve()}")
    for key, n in counts.most_common():
        print(f"  {n:6d}  {labels.get(key, key)}")
    runs = sorted({rec.get("run", "") for rec in data.values() if rec.get("run")})
    if runs:
        last = runs[-1]
        if len(last) == 15 and last[10] == "_":  # 2026-10-29_0003 -> 2026-10-29 00:03
            last = f"{last[:10]} {last[11:13]}:{last[13:]}"
        print(f"  last run: {last}")
    retry = [rec for rec in data.values() if rec.get("status") in ("error", "blocked", "po_token")]
    for rec in retry[:5]:
        print(f"    to retry: {rec.get('title', '')[:60]}  ({rec.get('error', '')[:70]})")
    from .netmeter import usage_report

    usage = usage_report(out, s)
    if usage:
        print()
        for line in usage:
            print(line)
    print()
    return 0


def main(argv: list[str] | None = None) -> int:
    _safe_console()
    parser = build_parser()
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        argv = ["run"]
    args = parser.parse_args(argv)

    if args.command == "init":
        from .doctor import init_config

        return init_config(PROJECT_DIR)
    if args.command == "selfupdate":
        return cmd_selfupdate(args.if_older_than)

    from .config import ConfigError

    try:
        s = settings_from_args(args)
    except ConfigError as e:
        if args.command == "gui":  # the window reports the problem itself and starts with defaults
            from .gui import launch

            return launch(args.config)
        print(f"\n{e}\n\nFix the file in Notepad and try again.", file=sys.stderr)
        return 2
    lock = None
    try:
        Path(s.output_dir).mkdir(parents=True, exist_ok=True)
        # only real runs replace last_run.log - doctor/status/find/gui must not erase the details of a failed run
        runs = args.command in ("run", "search", "transcripts", "channel")
        if runs:  # take the lock BEFORE touching last_run.log, so a busy run's log is never wiped
            from .utils import RunLock

            lock = RunLock(s.output_dir)
            if not lock.acquire():
                setup_logging(bool(s.verbose), None)
                log.error("Another run is already using %s - wait for it to finish (or close the other window).",
                          Path(s.output_dir).resolve())
                return 3
        setup_logging(bool(s.verbose), str(Path(s.output_dir) / "last_run.log") if runs else None)
    except OSError as e:
        if args.command == "gui":  # the window lets the user pick another folder
            from .gui import launch

            return launch(args.config)
        print(f"\nCan't use the output folder {s.output_dir}: {e.strerror or e}\n"
              "Is the drive connected? Change output_dir in config.toml (or plug the drive in) and try again.",
              file=sys.stderr)
        return 2

    try:
        if args.command == "doctor":
            from .doctor import run_doctor

            return run_doctor(s, args.video)
        if args.command == "status":
            return cmd_status(s)
        if args.command == "export":
            return cmd_export(s)
        if args.command == "find":
            return cmd_find(s, args.phrase, args.max_hits)
        if args.command == "related":
            from .related import cmd_related

            return cmd_related(s, args.seeds or s.all_keywords(), max_items=args.related_max,
                               use_titles=args.related_titles, add=args.related_add,
                               config_path=args.config or DEFAULT_CONFIG)
        if args.command == "gui":
            from .gui import launch

            return launch(args.config)
        try:
            if args.command == "search":
                videos, _ = cmd_search(s)
                return 0 if videos is not None else 2
            if args.command == "transcripts":
                return cmd_run(s, transcripts_only_list=args.list_file)
            if args.command == "channel":
                specs = list(args.channel_specs or s.channels)
                if not specs:
                    log.error("Which channel? e.g.  yt.py channel @mkbhd   (or list them under `channels` in "
                              "config.toml)")
                    return 2
                if args.list_only:
                    s.download_transcripts = False
                return cmd_run(s, channels=specs)
            return cmd_run(s)
        finally:
            if lock:
                lock.release()
    except KeyboardInterrupt:
        log.warning("Cancelled.")
        return 130
    except Exception as e:  # show a readable message; the full traceback goes to last_run.log
        log.debug("Unexpected error", exc_info=True)
        log.error("Stopped because of an error: %s", e)
        if args.command in ("run", "search", "transcripts", "channel"):
            log.error("Details are in %s. If YouTube changed something, running update.bat usually fixes it.",
                      Path(s.output_dir) / "last_run.log")
        return 1
