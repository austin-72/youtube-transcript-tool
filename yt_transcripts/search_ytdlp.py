"""Keyword search without an API key, using yt-dlp's YouTube search extractor.

YouTube removed "sort by upload date" from search in 2025, so "newest videos"
is done in two steps:

1. Ask YouTube for videos inside an upload-date window (today / this week /
   this month / this year), once ordered by Popularity and once by Relevance,
   scanning up to ``scan_per_keyword`` results each, and merge them.
2. Sort the merged set ourselves by publish date (newest first) and keep the
   ones above the view threshold.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from typing import Callable, Iterable
from urllib.parse import quote, quote_plus

from .config import Settings
from .models import Video, clean_chapters, clean_tags
from .sp_params import build_sp
from .utils import iso_utc, parse_count

MAX_DESCRIPTION = 5000  # characters of a video's description kept for its transcript files

log = logging.getLogger("yt_transcripts")

VIDEO_ID_LEN = 11


class SearchFailed(RuntimeError):
    """Every search request for a keyword failed (network trouble, or YouTube blocking us)."""


def search_url(keyword: str, sort: str, within: str | None, content_type: str = "video",
               subtitles_only: bool = False) -> str:
    sp = build_sp(sort=sort, upload_date=within, content_type=content_type,
                  subtitles_only=subtitles_only)
    return f"https://www.youtube.com/results?search_query={quote_plus(keyword)}&sp={quote(sp, safe='')}"


def entry_to_video(entry: dict, keyword: str, now: dt.datetime | None = None) -> Video | None:
    """Convert one flat yt-dlp search entry into a Video (None for non-videos/ads)."""
    if not isinstance(entry, dict):
        return None
    vid = entry.get("id") or ""
    if not isinstance(vid, str) or len(vid) != VIDEO_ID_LEN or entry.get("ie_key") not in (None, "Youtube"):
        return None
    url = entry.get("url") if isinstance(entry.get("url"), str) else ""
    if not url.startswith("http"):
        url = f"https://www.youtube.com/watch?v={vid}"
    views = _int_or_none(entry.get("view_count"))
    if views is None and entry.get("concurrent_view_count") is None:
        views = parse_count(str(entry.get("view_count_text") or ""))
    published, exact = "", False
    ts = entry.get("timestamp")
    try:
        if ts:
            published = iso_utc(dt.datetime.fromtimestamp(float(ts), dt.timezone.utc))
        elif isinstance(entry.get("upload_date"), str) and re.fullmatch(r"\d{8}", entry["upload_date"]):
            d = entry["upload_date"]
            published, exact = f"{d[:4]}-{d[4:6]}-{d[6:8]}", True
    except (TypeError, ValueError, OverflowError, OSError):
        published, exact = "", False
    dur = _int_or_none(entry.get("duration"))
    return Video(
        video_id=vid,
        title=str(entry.get("title") or ""),
        channel=str(entry.get("channel") or entry.get("uploader") or ""),
        channel_id=str(entry.get("channel_id") or ""),
        channel_handle=str(entry.get("uploader_id") or ""),
        url=url,
        views=views,
        published=published,
        published_exact=exact,
        duration_seconds=dur if dur and dur > 0 else None,
        is_short="/shorts/" in url,
        live_status=str(entry.get("live_status") or ""),
        keyword=keyword,
        source="youtube-search",
        description=str(entry.get("description") or "")[:500],
    )


def _int_or_none(value) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError, OverflowError):
        return None


def _iter_search(url: str, limit: int, settings: Settings, ydl_factory: Callable | None) -> Iterable[dict]:
    from .ytdlp_common import make_ydl

    factory = ydl_factory or (lambda **kw: make_ydl(settings, **kw))
    with factory(extract_flat="in_playlist", playlistend=limit, lazy_playlist=True) as ydl:
        info = ydl.extract_info(url, download=False, process=False)
        for i, entry in enumerate(info.get("entries") or []):
            if i >= limit:
                break
            if entry:
                yield entry


WINDOW_ORDER = ["today", "week", "month", "year"]


def search_plan(settings: Settings) -> list[tuple[str, str | None]]:
    """(sort, upload-date window) pairs to search. Every requested sort runs over the full window;
    with cascade_windows, Popularity also runs over each narrower window, because in a month-wide
    scan a video uploaded today is outranked by older ones with more views and could be cut off."""
    within = None if settings.within in ("any", "") else settings.within
    if within == "day":
        within = "today"
    plan: list[tuple[str, str | None]] = [(sort, within) for sort in dict.fromkeys(settings.sorts)]
    if settings.cascade_windows:
        narrower = WINDOW_ORDER[: WINDOW_ORDER.index(within)] if within in WINDOW_ORDER else (
            WINDOW_ORDER if within is None else [])
        for w in reversed(narrower):
            if ("popularity", w) not in plan:
                plan.append(("popularity", w))
    return plan


def search_keyword(keyword: str, settings: Settings, ydl_factory: Callable | None = None,
                   should_stop: Callable[[], bool] | None = None) -> list[Video]:
    types = ["video"] + (["shorts"] if settings.include_shorts else [])
    found: dict[str, Video] = {}
    attempts = failures = 0
    last_error = ""
    for sort, within in search_plan(settings):
        for ctype in types:
            if should_stop and should_stop():
                return list(found.values())
            url = search_url(keyword, sort, within, ctype, settings.subtitles_only)
            log.info("  searching %-11s %-6s %s", sort, ctype, "(" + (within or "any time") + ")")
            log.debug("  %s", url)
            n = 0
            attempts += 1
            try:
                for entry in _iter_search(url, settings.scan_per_keyword, settings, ydl_factory):
                    if should_stop and should_stop():
                        break
                    n += 1
                    try:
                        v = entry_to_video(entry, keyword)
                    except Exception as exc:  # one odd result must not throw away the whole search
                        log.debug("  skipped an unreadable search result: %s", exc)
                        continue
                    if v is None:
                        continue
                    if ctype == "shorts":
                        v.is_short = True
                    if v.video_id in found:
                        found[v.video_id].merge(v)
                    else:
                        found[v.video_id] = v
            except Exception as exc:  # network problems shouldn't kill other sorts/keywords
                failures += 1
                last_error = _short_err(exc)
                log.warning("  search failed (%s): %s", sort, last_error)
            log.debug("  %d results scanned", n)
    if attempts and failures == attempts and not found:
        raise SearchFailed(last_error)
    return list(found.values())


def enrich_exact(videos: list[Video], settings: Settings, ydl_factory: Callable | None = None) -> None:
    """Replace approximate dates/views with exact values: from the channel feeds first (one small
    request per channel), then from each remaining video's page (slow)."""
    from .feeds import fill_dates
    from .utils import polite_sleep
    from .ytdlp_common import make_ydl

    fill_dates(videos, settings, views=True)
    videos = [v for v in videos if not v.published_exact or v.views is None]
    if not videos:
        return

    factory = ydl_factory or (lambda **kw: make_ydl(settings, **kw))
    with factory() as ydl:
        for i, v in enumerate(videos, 1):
            try:
                info = ydl.extract_info(v.url, download=False, process=False)
            except Exception as exc:
                log.warning("  could not look up %s: %s", v.video_id, _short_err(exc))
                continue
            apply_full_info(v, info)
            log.debug("  exact date %d/%d %s -> %s", i, len(videos), v.video_id, v.published)
            polite_sleep(settings.delay_seconds / 2)


def apply_full_info(v: Video, info: dict) -> None:
    """Update a Video from a full (non-flat) yt-dlp info dict."""
    ts = info.get("timestamp") or info.get("release_timestamp")
    if ts:
        v.published, v.published_exact = iso_utc(dt.datetime.fromtimestamp(ts, dt.timezone.utc)), True
    elif info.get("upload_date"):
        d = info["upload_date"]
        v.published, v.published_exact = f"{d[:4]}-{d[4:6]}-{d[6:8]}", True
    if info.get("view_count") is not None:
        v.views = int(info["view_count"])
    if info.get("duration"):
        v.duration_seconds = int(info["duration"])
    v.title = info.get("title") or v.title
    v.channel = info.get("channel") or info.get("uploader") or v.channel
    v.channel_id = info.get("channel_id") or v.channel_id
    v.channel_handle = info.get("uploader_id") or v.channel_handle
    desc = info.get("description")
    if isinstance(desc, str) and len(desc) > len(v.description):
        v.description = desc[:MAX_DESCRIPTION]  # the full text (a search result only has a snippet)
    if info.get("tags"):
        v.tags = clean_tags(info["tags"])
    if info.get("chapters"):
        v.chapters = clean_chapters(info["chapters"])
    if info.get("live_status"):
        v.live_status = info["live_status"]


def _short_err(exc: Exception) -> str:
    from .utils import short_error

    return short_error(exc)
