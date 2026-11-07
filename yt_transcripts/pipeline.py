"""Download transcripts for a list of videos, with resume, skip and back-off."""

from __future__ import annotations

import datetime as dt
import json
import logging
import os
import time
from collections import Counter
from pathlib import Path
from typing import Callable

from . import transcripts as tr
from .config import Settings
from .models import Segment, Transcript, Video
from .utils import replace_file
from .writers import transcript_folder, write_combined, write_transcript

log = logging.getLogger("yt_transcripts")

BACKOFF_SECONDS = [60, 180, 420]
MAX_CONSECUTIVE_ERRORS = 6  # e.g. the internet connection dropped: stop instead of failing every video


class Manifest:
    """Remembers what happened to every video so re-runs skip finished work."""

    def __init__(self, path: Path):
        self.path = path
        self.data: dict[str, dict] = {}
        if path.exists():
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                log.warning("manifest %s is damaged - starting a new one", path)
                path.replace(path.with_suffix(".damaged.json"))

    def get(self, vid: str) -> dict:
        return self.data.get(vid, {})

    def update(self, vid: str, **fields) -> None:
        rec = self.data.setdefault(vid, {"attempts": 0})
        rec.update(fields)
        rec["updated"] = dt.datetime.now().isoformat(timespec="seconds")

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps(self.data, indent=1, ensure_ascii=False), encoding="utf-8")
        replace_file(tmp, self.path)


FRESH_DAYS = 3  # YouTube adds auto-captions a while after upload; keep retrying "no captions" until then


def _resolve(p: str, root: Path) -> Path:
    """Manifest paths are stored relative to the output folder (older runs: absolute)."""
    path = Path(p)
    return path if path.is_absolute() else root / path


def _relative(p: Path, root: Path) -> str:
    try:
        return os.path.relpath(p, root)
    except ValueError:  # different drive on Windows
        return str(p)


def should_skip(rec: dict, s: Settings, now: dt.datetime | None = None) -> str | None:
    status = rec.get("status")
    if status == tr.OK:
        files = rec.get("files", {})
        root = Path(s.output_dir)
        if files and all(_resolve(p, root).exists() for p in files.values()):
            if set(s.formats) <= set(files):
                if _render_changed(rec, s) and "json" in files:
                    return None  # text settings changed: rebuild the files from the saved .json
                return "already downloaded"
    elif status == tr.PO_TOKEN and not s.retry_failed:
        when = parse_retry_time(rec.get("next_retry", ""))
        if when and (now or dt.datetime.now(dt.timezone.utc)) < when:
            return f"needs a YouTube token - next try after {when.astimezone().strftime('%Y-%m-%d %H:%M')}"
    elif status in tr.PERMANENT and not s.retry_failed:
        if status == tr.NO_TRANSCRIPT and _is_fresh(rec.get("published", ""), now):
            return None  # captions may simply not be generated yet
        return f"skipped earlier: {status}"
    return None


PO_TOKEN_RETRY_HOURS = (6, 24, 72, 168)  # then weekly


def next_retry_time(attempts: int, now: dt.datetime | None = None) -> str:
    """When a video that hit YouTube's PO-token wall is worth trying again: 6 h, 1 d, 3 d, then weekly."""
    hours = PO_TOKEN_RETRY_HOURS[min(max(attempts, 1), len(PO_TOKEN_RETRY_HOURS)) - 1]
    return ((now or dt.datetime.now(dt.timezone.utc)) + dt.timedelta(hours=hours)).isoformat(timespec="seconds")


def parse_retry_time(value: str) -> dt.datetime | None:
    try:
        t = dt.datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)


def _is_fresh(published: str, now: dt.datetime | None = None) -> bool:
    from .models import parse_iso

    p = parse_iso(published)
    if p is None:
        return False
    now = now or dt.datetime.now(dt.timezone.utc)
    return (now - p).total_seconds() < FRESH_DAYS * 86400


def build_fetchers(s: Settings, ydl_factory: Callable | None = None) -> list:
    fetchers = []
    for m in s.transcript_methods:
        try:
            if m == "api":
                fetchers.append(tr.ApiFetcher(s))
            elif m == "ytdlp":
                fetchers.append(tr.YtDlpFetcher(s, ydl_factory))
        except ImportError as e:
            log.warning("transcript method %r unavailable (%s) - skipping it", m, e)
    if not fetchers:
        raise RuntimeError("No transcript method is available. Run setup.bat (or pip install -r requirements.txt).")
    return fetchers


class MethodBreaker:
    """Stop using a transcript method that keeps failing while a later method succeeds,
    e.g. youtube-transcript-api hitting YouTube's PO-token wall on every video."""

    LIMIT = 3

    def __init__(self) -> None:
        import threading

        self.misses: dict[str, int] = {}
        self.announced: set[str] = set()
        self.lock = threading.Lock()  # shared by all workers: a library-wide wall isn't per proxy

    def record(self, failed: list[str], succeeded: str | None) -> None:
        if succeeded is None:
            return  # nothing worked - not the method's fault specifically
        with self.lock:
            for name in failed:
                self.misses[name] = self.misses.get(name, 0) + 1
            self.misses[succeeded] = 0

    def prune(self, fetchers: list) -> list:
        if len(fetchers) < 2:
            return fetchers
        with self.lock:
            keep = [f for f in fetchers if self.misses.get(f.name, 0) < self.LIMIT]
            for f in fetchers:
                if f not in keep and f.name not in self.announced:
                    self.announced.add(f.name)
                    log.info("Skipping the %r transcript method for the rest of this run "
                             "(it failed %d times in a row while another method worked).", f.name, self.LIMIT)
        return keep or fetchers


def fetch_one(v: Video, fetchers: list, breaker: MethodBreaker | None = None
              ) -> tuple[Transcript | None, str, str, str]:
    """Try each method in order. Returns (transcript, status, message, method)."""
    errors: list[tuple[str, tr.FetchError]] = []
    for f in fetchers:
        try:
            t = f.fetch(v)
            _absorb_info(v, f)
            if breaker is not None:
                breaker.record([n for n, e in errors if e.status in (tr.ERROR, tr.BLOCKED)], f.name)
            return t, tr.OK, "", f.name
        except tr.FetchError as e:
            _absorb_info(v, f)
            errors.append((f.name, e))
            log.debug("    %s: %s (%s)", f.name, e.status, e)
            if e.status == tr.UNAVAILABLE and f.name == "ytdlp":
                break  # yt-dlp's verdict is reliable; the other library also says this when it's blocked
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # a bug or a library crash: fail this video, not the whole run
            from .utils import short_error

            log.debug("    %s crashed on %s", f.name, v.video_id, exc_info=True)
            errors.append((f.name, tr.FetchError(tr.ERROR, f"{f.name} failed unexpectedly: {short_error(exc)}")))
    ytdlp_status = next((e.status for n, e in errors if n == "ytdlp"), None)
    if ytdlp_status not in (None, tr.UNAVAILABLE):
        # yt-dlp saw the video: the other library's "unavailable" is its way of saying "blocked"
        errors = [(n, e) for n, e in errors if not (e.status == tr.UNAVAILABLE and n != "ytdlp")]
    statuses = [e.status for _, e in errors]
    order = [tr.UNAVAILABLE, tr.NO_TRANSCRIPT, tr.BLOCKED]
    if ytdlp_status == tr.PO_TOKEN or set(statuses) == {tr.PO_TOKEN}:
        order.append(tr.PO_TOKEN)  # a token wall, not a passing glitch: retry on a schedule
    for wanted in order:
        if wanted in statuses:
            name, err = errors[statuses.index(wanted)]
            # prefer the most specific message (yt-dlp's comes last)
            for n, fe in reversed(errors):
                if fe.status == wanted:
                    name, err = n, fe
                    break
            return None, wanted, str(err), name
    if not errors:
        return None, tr.ERROR, "no transcript method is enabled (check transcript_methods)", ""
    # a plain failure (network, glitch) beats one library's token wall: it's retried at the next run
    plain = [x for x in errors if x[1].status != tr.PO_TOKEN]
    name, err = plain[-1] if plain else errors[-1]
    return None, err.status, str(err), name


_FILLER = {
    "a", "an", "the", "how", "to", "for", "of", "in", "on", "and", "or", "with", "vs", "is", "are", "what", "why",
    "tutorial", "tutorials", "guide", "beginners", "beginner", "course", "explained", "review", "reviews", "tips",
    "best", "new", "full", "complete", "step", "by", "easy", "learn", "intro", "introduction", "video",
}


def count_mentions(text: str, keywords: str) -> int:
    """How often a video's keyword(s) ("a; b") come up in its transcript.

    Generic words ("tutorial", "how to", ...) are ignored; for each keyword the score is the count of its
    least-mentioned main word, so "claude code tutorial" scores how often both "claude" and "code" are said.
    Multiple keywords are added up."""
    import re

    words_in_text: dict[str, int] = {}
    for w in re.findall(r"[a-z0-9][a-z0-9'+#.-]*", text.lower()):
        w = w.strip(".'-")
        words_in_text[w] = words_in_text.get(w, 0) + 1
    total = 0
    for kw in [k.strip().lower() for k in keywords.split(";") if k.strip()]:
        core = [w.strip(".'-") for w in re.findall(r"[a-z0-9][a-z0-9'+#.-]*", kw)]
        core = [w for w in core if w and w not in _FILLER] or core
        if core:
            total += min(words_in_text.get(w, 0) for w in core)
    return total


def _absorb_info(v: Video, fetcher) -> None:
    info = getattr(fetcher, "last_info", None)
    if info:
        from .search_ytdlp import apply_full_info

        apply_full_info(v, info)
    comments = getattr(fetcher, "last_comments", None)
    if comments:
        v.comments = list(comments)


def _with_extras(s: Settings):
    """fetch_one plus the SponsorBlock lookup and the exact date from the channel feed (in the worker,
    so downloads run on while they answer)."""
    from .feeds import FeedDates

    cats = list(s.sponsorblock or [])
    feeds = FeedDates(s) if s.feed_dates else None

    def fetch(v: Video, fetchers: list, breaker=None):
        t, status, msg, method = fetch_one(v, fetchers, breaker)
        if t is not None and feeds is not None and not v.published_exact:
            # the data saver skipped the watch page (where the exact date is): ask the channel's feed
            hit = feeds.lookup(v.video_id, v.channel_id)
            if hit:
                v.published, v.published_exact = hit[0], True
        if t is not None and cats:
            from . import sponsorblock

            segs = sponsorblock.fetch_segments(v.video_id, cats, v.duration_seconds)
            t.skipped = segs or []
            t.sb_checked = segs is not None
        return t, status, msg, method
    return fetch


def download_all(videos: list[Video], s: Settings, *, ydl_factory: Callable | None = None,
                 sleep: Callable[[float], None] = time.sleep, run_stamp: str | None = None,
                 should_stop: Callable[[], bool] | None = None) -> Counter:
    """Fetch every video's transcript (skipping finished work), with one or more parallel workers."""
    from .proxies import ProxyPool, mask
    from .workers import Engine, Job

    root = Path(s.output_dir)
    run = _Run(s, root, run_stamp or dt.datetime.now().strftime("%Y-%m-%d_%H%M"), total=len(videos))
    log.info("Downloading transcripts for %d videos -> %s", len(videos), run.tdir.resolve())
    try:
        jobs = [Job(i, v, run.manifest.get(v.video_id)) for i, v in _plan(videos, s, run)]
        if jobs and not (should_stop and should_stop()):
            n_workers = s.resolved_workers()
            proxies = s.stage_proxies("transcripts")
            if s.proxy and not proxies:
                log.info("Downloading transcripts over your own connection (proxy_for_transcripts = false).")
            pool = ProxyPool(proxies, per_proxy=int(s.workers_per_proxy or 1),
                             direct_capacity=n_workers, rotating=_rotating_setting(s))
            n_workers = _cap_workers(n_workers, pool, len(jobs))
            tr.SAVER_HEALTH.reset()
            from . import netmeter

            if netmeter.active() is not None:
                netmeter.active().downloads_starting()
            if proxies and "ytdlp" in s.transcript_methods:
                import copy as _copy

                ps = _copy.copy(s)
                ps.proxy = ps.proxy or proxies[0]  # the workers' settings carry their proxy
                profile = tr.saver_profile(ps)
                if profile != "full":
                    log.info("Data saver %s: %s per video through the proxies (data_saver = \"off\" turns it off).",
                             profile, "two small requests" if profile == "max" else "fewer and smaller downloads")
            _announce(s, pool, n_workers, mask)
            if n_workers > 1:
                from .ytdlp_common import patch_relative_time_parsing

                patch_relative_time_parsing()  # once, before threads exist
            run.fetch_total = len(jobs)
            engine = Engine(jobs, s, pool, build_fetchers=build_fetchers, fetch_one=_with_extras(s),
                            breaker=MethodBreaker(), looks_offline=_looks_offline, backoff=BACKOFF_SECONDS,
                            on_result=run.apply, ydl_factory=ydl_factory, sleep=sleep, should_stop=should_stop)
            reason = engine.run(n_workers, prefer_url=s.proxy if proxies else "")
            run.finish(reason, pool)
        elif jobs:
            run.finish("interrupted", None)
    except KeyboardInterrupt:
        run.finish("interrupted", None)
    finally:
        run.manifest.save()

    if run.dupes is not None:
        run.dupes.save()
    if s.combine and run.done_now:
        done = [vt for _, vt in sorted(run.done_now, key=lambda x: x[0])]  # list order, not finishing order
        repeats = [vt for vt in done if vt[0].duplicate_of]
        if repeats and s.skip_duplicates:
            done = [vt for vt in done if not vt[0].duplicate_of]
            log.info("Left %d repeated transcript%s (clips / re-uploads) out of the combined file.",
                     len(repeats), "" if len(repeats) == 1 else "s")
        paths = write_combined(done, root / "combined", run.stamp, s.paragraph_seconds,
                               int(s.combine_max_words or 0), timestamps=s.timestamps,
                               chapters=s.chapters) if done else []
        if not paths:
            pass
        elif len(paths) == 1:
            log.info("Combined file (for reading or an AI): %s", paths[0].resolve())
        else:
            log.info("Combined files (for reading or an AI), %d in %s", len(paths), paths[0].parent.resolve())
            for pth in paths:
                log.info("    %s", pth.name)
    return run.stats


def _cap_workers(n_workers: int, pool, n_jobs: int) -> int:
    """No more workers than proxy slots (extra ones would only wait) or videos to fetch."""
    cap = pool.total_capacity()
    if n_workers > cap:
        log.info("%d parallel downloads asked for, but %d proxy slot%s - using %d. (Raise workers_per_proxy "
                 "for a rotating proxy service.)", n_workers, cap, "" if cap == 1 else "s", cap)
        n_workers = cap
    return max(1, min(n_workers, n_jobs))


def _rotating_setting(s: Settings):
    v = str(s.proxy_rotating).strip().lower()
    return "auto" if v == "auto" else v == "true"


def _announce(s: Settings, pool, n_workers: int, mask) -> None:
    proxies = [x.url for x in pool.slots if x.url]
    rotating = [x for x in pool.slots if x.rotating]
    if proxies:
        kind = f"{len(proxies)} prox{'y' if len(proxies) == 1 else 'ies'}"
        if rotating:
            kind += f" ({len(rotating)} rotating)"
        log.info("Using %s%s.", kind, f" with {n_workers} parallel downloads" if n_workers > 1 else
                 f": {mask(proxies[0])}" if len(proxies) == 1 else ", switching when YouTube blocks one")
        from .workers import switch_after

        n = switch_after(s, pool)
        if n:
            log.info("Taking turns through the list: %d videos per proxy, then the one that has rested longest "
                     "(proxy_switch_after).", n)
    elif n_workers > 1:
        log.warning("Running %d downloads at once WITHOUT proxies - they all share your IP, so YouTube's "
                    "hourly limit is reached sooner. Proxies are the safe way to go faster.", n_workers)
    if (s.cookies_file or s.cookies_from_browser) and str(s.workers).lower() not in ("auto", "1"):
        log.info("Cookies are set, so downloads run one at a time (one account from several IPs risks a ban).")


def _plan(videos: list[Video], s: Settings, run: "_Run") -> list[tuple[int, Video]]:
    """The local part: skip finished videos, rebuild files from saved .json copies, apply the per-run cap.
    Returns the videos that need YouTube, in list order."""
    todo: list[tuple[int, Video]] = []
    for i, v in enumerate(videos):
        rec = run.manifest.get(v.video_id)
        skip = should_skip(rec, s)
        if skip and run.sb_refresh_due(v, rec):
            saved = _transcript_from_saved_json(rec, run.root)
            if saved is not None:
                run.rebuild(v, rec, saved, refresh_sb=True)
                continue
        if skip:
            run.skip(v, rec, skip)
            continue
        saved = _transcript_from_saved_json(rec, run.root)
        if saved is not None:  # finished before, only a format/text setting changed: no YouTube request
            run.rebuild(v, rec, saved, refresh_sb=bool(rec) and run.sb_refresh_due(v, rec))
            continue
        todo.append((i, v))
    if s.max_transcripts_per_run and len(todo) > s.max_transcripts_per_run:
        left = len(todo) - s.max_transcripts_per_run
        run.stats["left_for_next_run"] += left
        log.info("Reached max_transcripts_per_run (%d) - %d video(s) left for the next run.",
                 s.max_transcripts_per_run, left)
        todo = todo[: s.max_transcripts_per_run]
    return todo


class _Run:
    """Everything that writes: files, manifest, statistics and the progress log. Only ever used from one
    thread (the coordinator), so it needs no locks."""

    def __init__(self, s: Settings, root: Path, stamp: str, total: int):
        self.s, self.root, self.stamp, self.total = s, root, stamp, total
        self.tdir = root / "transcripts"
        self.manifest = Manifest(root / "manifest.json")
        self.stats: Counter = Counter()
        self.done_now: list[tuple[int, tuple[Video, Transcript]]] = []
        self.progress = 0  # lines logged as [progress/total] - never goes backwards, even with workers
        self.fetch_total = 0
        self.fetched = 0
        self.started = time.monotonic()
        self.offline_in_a_row = 0
        self.dupes = None
        if s.skip_duplicates:
            from .dupes import DuplicateIndex

            self.dupes = DuplicateIndex(root)  # loads its file only when the first video needs checking
        self.sb_refreshed = 0
        self.raw_by_id: dict[str, Transcript] = {}
        self.base_by_id: dict[str, tuple[Path, str]] = {}

    def _saved_text(self, vid: str) -> str:
        """Another video's transcript text, from its saved .json (for the duplicate check)."""
        rec = self.manifest.get(vid)
        js = rec.get("files", {}).get("json") if rec else None
        if not js:
            return ""
        try:
            data = json.loads(_resolve(js, self.root).read_text(encoding="utf-8"))
            return " ".join(str(x.get("text", "")) for x in data["transcript"]["segments"])
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            return ""

    def _check_repeat(self, v: Video, raw) -> tuple[list[str], list[str]]:
        """Sets v.duplicate_of if this text repeats an earlier video. Returns (log notes, earlier videos of
        this run whose text is inside this one)."""
        if self.dupes is None or "json" not in (self.s.formats or []):
            return [], []  # the exact check reads the saved .json files

        def names_me(other: str) -> bool:  # never let two videos point at each other
            return str(self.manifest.get(other).get("duplicate_of", "")).split(" ")[0] == v.video_id
        repeats, contained = self.dupes.check_and_add(v.video_id, v.title, raw.text, self._saved_text,
                                                      skip=names_me)
        notes = []
        if repeats:
            v.duplicate_of = f"{repeats[0]} {repeats[1]}".strip()
            notes.append(f"    (its text repeats \"{_short(repeats[1] or repeats[0])}\" - left out of the combined file)")
        return notes, contained

    def _mark_contained(self, v: Video, contained: list[str]) -> None:
        """Earlier videos of this run (clips) whose text turned out to be inside this one: mark them and
        rewrite their files, so their headers say so too."""
        this_run = {vt[0].video_id: vt for _, vt in self.done_now}
        for other in contained:
            pair = this_run.get(other)
            if pair is None or pair[0].duplicate_of or other == v.video_id:
                continue
            ov, ot = pair
            ov.duplicate_of = f"{v.video_id} {v.title}".strip()
            self.manifest.update(other, duplicate_of=ov.duplicate_of)
            where = self.base_by_id.get(other)
            if where is not None:
                s = self.s
                write_transcript(ov, ot, where[0], s.formats, s.timestamps, s.paragraph_seconds, base=where[1],
                                 raw=self.raw_by_id.get(other), **_keep(s))
            log.info("    (\"%s\" is part of this one - left out of the combined file)", _short(ov.title))

    def _tick(self) -> int:
        self.progress += 1
        return self.progress

    def skip(self, v: Video, rec: dict, why: str) -> None:
        s, root = self.s, self.root
        self.stats["skipped"] += 1
        if rec.get("published_exact") and not v.published_exact:
            v.published, v.published_exact = rec.get("published", v.published), True
        v.transcript_status = rec.get("status", "")
        v.transcript_language = rec.get("language", "")
        v.transcript_kind = rec.get("kind", "")
        v.keyword_mentions = rec.get("mentions")
        v.duplicate_of = v.duplicate_of or rec.get("duplicate_of", "")
        first = rec.get("files", {}).get(s.formats[0], "") if s.formats else ""
        v.transcript_file = str(_resolve(first, root)) if first else ""
        log.info("[%d/%d] skip  %s  (%s)", self._tick(), self.total, _short(v.title or v.video_id), why)

    SB_REFRESH_MAX = 150  # SponsorBlock re-checks per run (one small request each, own connection)

    def sb_refresh_due(self, v: Video, rec: dict) -> bool:
        """Ask SponsorBlock again for a finished video? When categories were added since it was asked, or
        when a new upload had no segments yet (people submit them over the first days)."""
        s = self.s
        sb = rec.get("sb") if rec.get("status") == tr.OK else None
        if not s.sponsorblock or not isinstance(sb, dict) or self.sb_refreshed >= self.SB_REFRESH_MAX:
            return False  # transcripts from before SponsorBlock support are left as they are
        if set(s.sponsorblock) - set(sb.get("asked") or []):
            return True
        if sb.get("found") or int(sb.get("tries", 1)) >= 3:
            return False
        checked = parse_retry_time(sb.get("checked", "")) if sb.get("checked") else None
        now = dt.datetime.now(dt.timezone.utc)
        young = _is_fresh(rec.get("published") or v.published, now)
        return young and (checked is None or (now - checked).total_seconds() > 12 * 3600)

    def _sb_record(self, vid: str, cats: list[str], ok: bool, found: int, rec: dict) -> None:
        old = rec.get("sb") if isinstance(rec.get("sb"), dict) else {}
        self.manifest.update(vid, sb={"asked": sorted(cats),
                                      "checked": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
                                      if ok else "", "found": found, "tries": int(old.get("tries", 0)) + 1})

    def rebuild(self, v: Video, rec: dict, saved, refresh_sb: bool = False) -> None:
        s, root = self.s, self.root
        t, saved_video, folder = saved
        sb_changed = False
        if refresh_sb:
            from . import sponsorblock

            self.sb_refreshed += 1
            segs = sponsorblock.fetch_segments(v.video_id, list(s.sponsorblock), v.duration_seconds
                                               or saved_video.get("duration_seconds"))
            if segs is not None:
                sb_changed = segs != t.skipped
                t.skipped = segs
            self._sb_record(v.video_id, list(s.sponsorblock), segs is not None, len(segs or []), rec)
        try:
            sv = Video.from_dict({**saved_video, "video_id": v.video_id})  # coerces hand-edited values
        except (TypeError, ValueError):
            sv = None
        for name in saved_video if sv is not None else ():
            # bare links have no title/date: take them from the save
            if hasattr(v, name) and not getattr(v, name) and getattr(sv, name):
                setattr(v, name, getattr(sv, name))
        if sv is not None and len(sv.description) > len(v.description):  # the full text, not a search snippet
            v.description = sv.description
        v.duplicate_of = v.duplicate_of or rec.get("duplicate_of", "")
        have = {k: _resolve(f, root) for k, f in rec.get("files", {}).items()}
        restyle = _render_changed(rec, s)  # e.g. "timestamps in .txt" was switched on
        todo = [f for f in s.formats if f not in have or not have[f].exists() or restyle or sb_changed]
        raw = t
        t = _clean_text(t, s)
        base = Path(rec["files"]["json"]).stem  # same name and folder as the files already there
        files = write_transcript(v, t, folder, todo, s.timestamps, s.paragraph_seconds, base=base, raw=raw,
                                 **_keep(s))
        all_files = {**{k: f for k, f in have.items() if f.exists()}, **files}
        v.transcript_status, v.transcript_language, v.transcript_kind = tr.OK, t.language, t.kind
        v.keyword_mentions = rec.get("mentions")
        first = all_files.get(s.formats[0]) if s.formats else None
        v.transcript_file = str(first) if first else ""
        self.manifest.update(v.video_id, files={k: _relative(f, root) for k, f in all_files.items()},
                             render=render_signature(s))
        self.manifest.save()
        self.stats["skipped"] += 1
        log.info("[%d/%d] skip  %s  (%s)", self._tick(), self.total, _short(v.title or v.video_id),
                 f"{'rebuilt' if restyle else 'added'} {', '.join(todo)} from the saved transcript"
                 if todo else "already downloaded")

    def apply(self, r) -> str | None:
        """Record one finished download. Returns a reason to stop the whole run, or None."""
        s, root, v, t, status, msg, method = self.s, self.root, r.job.video, r.transcript, r.status, r.message, r.method
        rec = self.manifest.get(v.video_id)
        attempts = rec.get("attempts", 0) + 1
        v.transcript_status = status
        if v.published_exact:
            self.manifest.update(v.video_id, published=v.published, published_exact=True)
        raw = t
        if t is not None:
            t = _clean_text(t, s)
            words = len(t.text.split())
            if s.min_transcript_words and words < s.min_transcript_words:
                t, status = None, tr.NO_TRANSCRIPT
                msg = f"only {words} words (min_transcript_words = {s.min_transcript_words})"
        via = f"  via {r.via}" if r.via and s.resolved_workers() > 1 else ""
        if t is not None:
            v.transcript_status = tr.OK
            v.transcript_language, v.transcript_kind = t.language, t.kind
            # "mentions" = how often the transcript says the search words; a channel name isn't one
            v.keyword_mentions = None if v.source in ("channel", "playlist") else count_mentions(t.text, v.keyword)
            v.duplicate_of = ""  # a fresh download is judged anew
            notes, contained = self._check_repeat(v, raw)  # before writing, so the files carry "Repeats:"
            folder = transcript_folder(self.tdir, v, s.organize_by)
            files = write_transcript(v, t, folder, s.formats, s.timestamps, s.paragraph_seconds,
                                     template=s.file_name, raw=raw, **_keep(s))
            v.transcript_file = str(files.get(s.formats[0], "")) if s.formats else ""
            self.manifest.update(v.video_id, status=tr.OK, method=method, language=t.language, kind=t.kind,
                                 files={k: _relative(p, root) for k, p in files.items()}, error="",
                                 attempts=attempts, mentions=v.keyword_mentions, next_retry="",
                                 title=v.title, run=self.stamp, render=render_signature(s),
                                 duplicate_of=v.duplicate_of)
            if s.sponsorblock and hasattr(raw, "sb_checked"):
                self._sb_record(v.video_id, list(s.sponsorblock), raw.sb_checked, len(raw.skipped), rec)
            if files:
                some = next(iter(files.values()))
                self.base_by_id[v.video_id] = (some.parent, some.stem)
            self.raw_by_id[v.video_id] = raw
            self.done_now.append((r.job.index, (v, t)))
            self.stats["ok"] += 1
            extra = f", {len(t.removed)} sponsor/promo part{'s' if len(t.removed) != 1 else ''} cut" if t.removed else ""
            log.info("[%d/%d] OK    %s  (%s, %s, %d words%s)%s", self._tick(), self.total, _short(v.title),
                     t.language, t.kind, len(t.text.split()), extra, via)
            for note in notes:
                log.info(note)
            self._mark_contained(v, contained)
        else:
            po_hits = rec.get("po_token_hits", 0) + 1 if status == tr.PO_TOKEN else 0
            self.manifest.update(v.video_id, status=status, method=method, error=msg, attempts=attempts,
                                 title=v.title, run=self.stamp, published=v.published, po_token_hits=po_hits,
                                 next_retry=next_retry_time(po_hits) if status == tr.PO_TOKEN else "")
            v.transcript_status = status
            self.stats[status] += 1
            log.info("[%d/%d] %-5s %s  (%s)%s", self._tick(), self.total, _label(status),
                     _short(v.title or v.video_id), msg, via)
        self.manifest.save()
        self.fetched += 1
        if self.fetched % 10 == 0 and self.fetched < self.fetch_total:
            per = (time.monotonic() - self.started) / self.fetched
            left = self.fetch_total - self.fetched
            from . import netmeter

            sess = netmeter.active()
            data = ""
            if sess is not None:
                sess.save()  # a crash or a closed window still leaves the count on disk
                pv = sess.per_video()
                if pv:
                    data = f" (proxy data: {netmeter.fmt_bytes(sess.meter.total)} so far, ~{netmeter.fmt_bytes(pv)} " \
                           f"per video, ~{netmeter.fmt_bytes(pv * left)} more)"
            log.info("    ...%d done this run, %s left for the remaining %d%s", self.fetched, _eta(per * left), left,
                     data)
        # the connection itself is down (no proxy to switch to): stop instead of failing every video
        self.offline_in_a_row = self.offline_in_a_row + 1 if status == tr.ERROR and _looks_offline(msg) else 0
        if self.offline_in_a_row >= MAX_CONSECUTIVE_ERRORS and self.fetched < self.fetch_total:
            self.last_error = msg
            return "errors"
        return None

    def finish(self, reason: str, pool) -> None:
        if reason == "blocked":
            self.stats["stopped_blocked"] += 1
            log.error("Stopping: YouTube keeps blocking requests%s.",
                      " through every proxy" if pool is not None and len(pool.slots) > 1 else "")
            log.error("Tips: wait an hour and run again (finished videos are skipped), lower "
                      "videos_per_hour_per_ip or raise delay_seconds, or add proxies.")
        elif reason == "dead":
            self.stats["stopped_errors"] += 1
            log.error("Stopping: none of the proxies could connect. Check the proxy addresses, user names and "
                      "passwords (run update.bat - it tests every proxy).")
        elif reason == "errors":
            self.stats["stopped_errors"] += 1
            log.error("Stopping: %d videos in a row failed to connect (last error: %s).", MAX_CONSECUTIVE_ERRORS,
                      getattr(self, "last_error", ""))
            log.error("Check your internet connection, or run update.bat if YouTube changed something. "
                      "Unfinished videos will be tried again on the next run.")
        elif reason == "data_limit":
            self.stats["stopped_data_limit"] += 1
            from . import netmeter

            sess = netmeter.active()
            log.warning("Stopping: %s. Unfinished videos will be fetched on the next run.",
                        sess.limit_message() if sess else "proxy data limit reached")
        elif reason == "interrupted":
            self.stats["interrupted"] += 1
            log.warning("Interrupted - progress saved. Run again to continue where you left off.")
        elif reason == "error":
            self.stats["interrupted"] += 1


def _clean_text(t, s: Settings):
    """A cleaned copy for the readable formats; the .json keeps the original text, so switching the
    cleaning off later rebuilds the files with nothing lost."""
    cats = set(s.sponsorblock or [])
    cut = [x for x in (t.skipped or []) if x.get("category") in cats]
    if not (s.strip_sound_tags or s.remove_filler_words or cut):
        return t
    import copy

    t = copy.copy(t)
    t.segments = list(t.segments)
    if cut:
        from . import sponsorblock

        sponsorblock.cut(t, cut)
        t.removed = cut
    if s.strip_sound_tags:
        tr.strip_sound_tags(t)
    if s.remove_filler_words:
        tr.remove_filler_words(t)
    return t


def _keep(s: Settings) -> dict:
    """What goes into the saved files besides the transcript (description, chapters)."""
    return {"description": bool(s.include_description), "chapters": bool(s.chapters)}


def render_signature(s: Settings) -> str:
    """The settings that shape the text of transcript files (not which video/track was fetched)."""
    sig = f"ts={int(bool(s.timestamps))};sound={int(bool(s.strip_sound_tags))};para={s.paragraph_seconds}"
    sig += f";desc={int(bool(s.include_description))};ch={int(bool(s.chapters))}"
    sig += ";filler=1" if s.remove_filler_words else ""
    from .config import Settings as _S

    if sorted(s.sponsorblock or []) != sorted(_S().sponsorblock):  # the default adds nothing: no mass rebuild
        sig += ";sb=" + ",".join(sorted(s.sponsorblock or []))
    return sig


def _render_changed(rec: dict, s: Settings) -> bool:
    return bool(rec.get("render")) and rec["render"] != render_signature(s)


def apply_manifest(videos: list[Video], s: Settings) -> None:
    """Fill transcript status/file/mentions from earlier runs, so lists written before (or without)
    downloading - search only, a stopped or capped run - still link to transcripts already on disk."""
    root = Path(s.output_dir)
    path = root / "manifest.json"
    if not path.exists():
        return
    manifest = Manifest(path)
    for v in videos:
        rec = manifest.get(v.video_id)
        if not rec or v.transcript_status:
            continue
        v.transcript_status = rec.get("status", "")
        v.transcript_language = rec.get("language", "")
        v.transcript_kind = rec.get("kind", "")
        v.keyword_mentions = rec.get("mentions")
        v.duplicate_of = v.duplicate_of or rec.get("duplicate_of", "")
        for fmt in (s.formats or []) + list(rec.get("files", {})):
            f = rec.get("files", {}).get(fmt)
            if f and _resolve(f, root).exists():
                v.transcript_file = str(_resolve(f, root))
                break
        if rec.get("published_exact") and not v.published_exact and rec.get("published"):
            v.published, v.published_exact = rec["published"], True


def _needs_fetch(rec: dict, s: Settings, root: Path) -> bool:
    """Will this video need a YouTube request (not skipped, and not just a format added from its .json)?"""
    if should_skip(rec, s):
        return False
    js = rec.get("files", {}).get("json") if rec.get("status") == tr.OK else None
    return not (js and _resolve(js, root).exists())


def _transcript_from_saved_json(rec: dict, root: Path) -> tuple[Transcript, dict, Path] | None:
    """Rebuild a finished transcript from its .json file (no YouTube request needed).
    Returns (transcript, the saved video details, the folder the files live in)."""
    if rec.get("status") != tr.OK or "json" not in rec.get("files", {}):
        return None
    p = _resolve(rec["files"]["json"], root)
    try:
        whole = json.loads(p.read_text(encoding="utf-8"))
        data = whole["transcript"]
        segs = [Segment(float(x["start"]), float(x["duration"]), str(x["text"])) for x in data["segments"]]
        video = whole.get("video") or {}
        vid = str(video.get("video_id", ""))
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None
    if not segs:
        return None
    skipped = [x for x in data.get("skipped") or [] if isinstance(x, dict) and {"start", "end", "category"} <= set(x)]
    t = Transcript(video_id=vid, language=data.get("language", ""), language_name=data.get("language_name", ""),
                   kind=data.get("kind", ""), method=data.get("method", ""), segments=segs, skipped=skipped)
    keep = ("title", "channel", "channel_id", "channel_handle", "published", "published_exact", "views",
            "duration_seconds", "keyword", "description", "tags", "chapters", "comments")
    return t, {k: video.get(k) for k in keep if k in video}, p.parent


class _Blocked(Exception):
    pass


class _TooManyErrors(Exception):
    pass


def _looks_offline(msg: str) -> bool:
    from .utils import _NETWORK_HINTS

    low = (msg or "").lower()
    return "no connection" in low or any(h in low for h in _NETWORK_HINTS + _WIN_NET_HINTS)


_WIN_NET_HINTS = ("winerror 10060", "winerror 10061", "winerror 10054", "winerror 10065", "winerror 11001",
                  "remote end closed connection", "connectionerror", "max retries exceeded")


def _eta(seconds: float) -> str:
    if seconds < 60:
        return "under a minute"
    if seconds < 90:
        return "about 1 minute"
    if seconds < 3600:
        return f"about {round(seconds / 60)} minutes"
    return f"about {seconds / 3600:.1f} hours"


def _short(text: str, n: int = 70) -> str:
    text = text or ""
    return text if len(text) <= n else text[: n - 1] + "…"


def _label(status: str) -> str:
    return {tr.NO_TRANSCRIPT: "NONE", tr.UNAVAILABLE: "UNAV", tr.BLOCKED: "BLOCK", tr.ERROR: "FAIL",
            tr.PO_TOKEN: "TOKEN"}.get(status, status)
