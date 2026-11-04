"""Every video of a channel (or a playlist): list them, newest first, ready for the transcript stage.

    @mkbhd   mkbhd   https://www.youtube.com/@mkbhd/videos   UCBJycsmduvYEL83R_U4JriQ
    https://www.youtube.com/channel/UC...   https://www.youtube.com/c/Name   https://www.youtube.com/user/name
    https://www.youtube.com/playlist?list=PL...   (any link with list=...)

The channel's tabs list the newest uploads first, so when an age limit is set (channel_within or
published_after) the listing stops as soon as it reaches older videos - no need to page through years
of uploads. Listing is part of the "search" step, so with proxy_for_search = false it uses your own
connection and costs no proxy data.
"""

from __future__ import annotations

import copy
import datetime as dt
import logging
import re
from typing import Callable
from urllib.parse import parse_qs, urlsplit

from .config import Settings
from .models import Video

log = logging.getLogger("yt_transcripts")

TABS = ("videos", "shorts", "streams")
OLDER_STREAK_STOP = 6  # this many uploads in a row older than the cut-off: the rest are older too
_TAB_SUFFIX = re.compile(r"/(videos|shorts|streams|featured|about|playlists|community|posts|releases|"
                         r"podcasts|courses|store|search|live)/?$", re.I)


class ChannelError(ValueError):
    pass


def channel_url(spec: str) -> tuple[str, bool]:
    """(base URL, is_playlist) for anything people paste to mean a channel or playlist."""
    sp = (spec or "").strip().strip('"').strip("'")
    if not sp:
        raise ChannelError("empty channel name")
    if re.match(r"(?i)^(https?://)?((www|m|music)\.)?(youtube\.com|youtu\.be)/", sp):
        if not sp.lower().startswith("http"):
            sp = "https://" + sp
        u = urlsplit(sp)
        lst = parse_qs(u.query).get("list", [""])[0]
        if lst:
            return f"https://www.youtube.com/playlist?list={lst}", True
        path = _TAB_SUFFIX.sub("", u.path.rstrip("/"))
        m = re.match(r"^/(@[^/]+|channel/UC[\w-]{22}|c/[^/]+|user/[^/]+)$", path)
        if not m:
            raise ChannelError(f"{spec!r} is not a channel or playlist link")
        return f"https://www.youtube.com/{m.group(1)}", False
    if re.fullmatch(r"UC[\w-]{22}", sp):
        return f"https://www.youtube.com/channel/{sp}", False
    if re.fullmatch(r"(PL|UU|OL|FL|RD)[\w-]{10,}", sp):
        return f"https://www.youtube.com/playlist?list={sp}", True
    handle = sp if sp.startswith("@") else "@" + sp
    if re.search(r"[\s/?#&]", handle):
        raise ChannelError(f"{spec!r} doesn't look like a channel (try its link or @handle)")
    return f"https://www.youtube.com/{handle}", False


def channel_settings(s: Settings) -> Settings:
    """The filters for channel downloads: the channel_* settings, plus length, date-range, max_views and
    exclude_words from the main settings. Keyword-only filters don't apply."""
    cs = copy.copy(s)
    cs.min_views = s.channel_min_views
    cs.rising_views_per_day = 0
    cs.within = s.channel_within
    cs.max_age_days = None
    cs.max_results = s.channel_max_videos
    cs.include_shorts = "shorts" in s.channel_tabs
    cs.title_must_contain = []
    cs.only_channels, cs.exclude_channels = [], []
    cs.drop_reuploads = False
    return cs


def _cutoff_days(cs: Settings) -> float | None:
    """How old a video can be (days), from channel_within and published_after - None = no limit."""
    from .config import WINDOW_DAYS, parse_day

    limits = []
    if cs.within in WINDOW_DAYS:
        limits.append(float(WINDOW_DAYS[cs.within]))
    after = parse_day(cs.published_after)
    if after:
        limits.append((dt.date.today() - after).days + 1.0)
    return min(limits) if limits else None


def list_channel(spec: str, s: Settings, *, ydl_factory: Callable | None = None,
                 should_stop: Callable[[], bool] | None = None) -> tuple[list[Video], str]:
    """All matching videos of one channel/playlist (newest first) and a label for it, e.g. "@mkbhd"."""
    from .search import filter_and_rank, reject_reason
    from .search_ytdlp import SearchFailed, entry_to_video
    from .ytdlp_common import make_ydl

    cs = channel_settings(s)
    base, is_playlist = channel_url(spec)
    tabs = [""] if is_playlist else [t for t in (cs.channel_tabs or ["videos"]) if t in TABS] or ["videos"]
    cutoff = _cutoff_days(cs)
    want = cs.max_results
    # channel tabs list the newest first, so "newest N" needs only the first pages; a playlist can be in
    # any order (often oldest first), so all of it is read
    scan_limit = max(want * 3, want + 60) if want and not is_playlist else None
    factory = ydl_factory or (lambda **kw: make_ydl(cs, **kw))
    now = dt.datetime.now(dt.timezone.utc)
    found: dict[str, Video] = {}
    label = ""
    failures, last_error = 0, ""
    for tab in tabs:
        url = f"{base}/{tab}" if tab else base
        log.info("  listing %s", url)
        try:
            with factory(extract_flat="in_playlist", playlistend=scan_limit, lazy_playlist=True) as ydl:
                info = ydl.extract_info(url, download=False, process=False) or {}
                name = str(info.get("channel") or info.get("uploader") or "")
                if not name:
                    name = re.sub(r"\s+-\s+(Videos|Shorts|Live|Home)$", "", str(info.get("title") or ""))
                handle = str(info.get("uploader_id") or "")
                cid = str(info.get("channel_id") or "")
                if not label:
                    label = handle if handle.startswith("@") else (name or spec.strip())
                    if is_playlist:
                        label = f"playlist {info.get('title') or spec.strip()}"
                older, passing, n = 0, 0, 0
                for entry in info.get("entries") or []:
                    if should_stop and should_stop():
                        break
                    if scan_limit and n >= scan_limit:
                        break
                    n += 1
                    try:
                        v = entry_to_video(entry, label)
                    except Exception as exc:  # one odd entry must not lose the channel
                        log.debug("  skipped an unreadable entry: %s", exc)
                        continue
                    if v is None:
                        continue
                    v.source = "playlist" if is_playlist else "channel"
                    if not is_playlist:
                        v.channel = v.channel or name
                        v.channel_id = v.channel_id or cid
                        v.channel_handle = v.channel_handle or handle
                    if tab == "shorts":
                        v.is_short = True
                    age = v.age_days(now)
                    if cutoff is not None and age is not None and not is_playlist:
                        if age > cutoff + 1.0:
                            older += 1
                            if older >= OLDER_STREAK_STOP:
                                log.debug("  reached uploads older than the cut-off - stopping this tab")
                                break
                            continue
                        older = 0
                    if v.video_id not in found:
                        found[v.video_id] = v
                        if want and not reject_reason(v, cs, now):
                            passing += 1
                            if passing >= want and not is_playlist:
                                break  # newest first: the rest of this tab can't make the cut
                log.info("    %d %s looked at", n, "entries" if is_playlist else f"{tab or 'videos'}")
        except Exception as exc:  # e.g. "This channel does not have a shorts tab"
            failures += 1
            from .utils import short_error

            last_error = short_error(exc)
            low = last_error.lower()
            if "does not have" in low or "no " + (tab or "videos") in low:
                log.info("    (no %s tab)", tab)
            else:
                log.warning("    could not list %s: %s", url, last_error)
    if failures == len(tabs) and not found:
        raise SearchFailed(last_error or f"could not list {spec}")
    kept, reasons = filter_and_rank(list(found.values()), cs, now)
    detail = ", ".join(f"{n} {r}" for r, n in reasons.most_common())
    log.info("  %s: %d found -> %d kept%s", label or spec, len(found), len(kept),
             f"  (dropped: {detail})" if detail else "")
    return kept, label or spec


def run_channels(s: Settings, specs: list[str] | None = None, *, ydl_factory: Callable | None = None,
                 should_stop: Callable[[], bool] | None = None) -> list[Video]:
    """List every channel in `specs` (default: s.channels), through the search proxies if any."""
    from . import netmeter
    from .search import rank_newest
    from .search_ytdlp import SearchFailed

    specs = [x for x in (specs if specs is not None else s.channels) if str(x).strip()]
    proxies = s.stage_proxies("search") or [""]
    out: dict[str, Video] = {}
    failed = []
    for i, spec in enumerate(specs, 1):
        if should_stop and should_stop():
            break
        log.info("[%d/%d] Channel: %s", i, len(specs), spec)
        last: Exception | None = None
        for proxy in proxies:  # a failed listing is retried through the next proxy
            sess = netmeter.active()
            if proxy and sess is not None and sess.limit_reached():
                last = SearchFailed(sess.limit_message())
                break
            cs = copy.copy(s)
            cs.proxy = netmeter.route(proxy)
            try:
                videos, _ = list_channel(spec, cs, ydl_factory=ydl_factory, should_stop=should_stop)
            except ChannelError as e:
                log.error("  %s", e)
                last = e
                break
            except SearchFailed as e:
                last = e
                continue
            for v in videos:
                if v.video_id in out:
                    out[v.video_id].merge(v)
                else:
                    out[v.video_id] = v
            last = None
            break
        if last is not None:
            failed.append(spec)
            log.error("  could not list %s: %s", spec, last)
    if failed and len(failed) == len(specs):
        raise RuntimeError(f"could not list any of the channels ({failed[0]}...). Check the names/links "
                           "and your internet connection.")
    return rank_newest(list(out.values()))
