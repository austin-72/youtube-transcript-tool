"""Run the search for every keyword, then filter by views/age/etc. and rank newest first."""

from __future__ import annotations

import datetime as dt
import logging
from collections import Counter
from typing import Callable

from . import netmeter
from .config import Settings
from .models import Video

log = logging.getLogger("yt_transcripts")

MAX_VIEW_LOOKUPS = 60  # per keyword, when search results lack view counts
APPROX_SLACK_DAYS = 1.0  # "2d ago" may really be 2.9 days


def _rising(v: Video, s: Settings, now: dt.datetime) -> bool:
    """Is the video gaining at least rising_views_per_day? For approximate dates ("1 day ago" can mean up to
    2 days) assume the older end, so day-old videos aren't overrated; hour-level labels are precise enough."""
    age = v.age_days(now)
    if v.views is None or age is None:
        return False
    if not v.published_exact and age >= 0.5:
        age += APPROX_SLACK_DAYS
    return v.views / max(age, 0.5) >= s.rising_views_per_day


def reject_reason(v: Video, s: Settings, now: dt.datetime) -> str | None:
    """Return why a video is filtered out, or None if it passes."""
    if v.live_status in ("is_live", "is_upcoming") and s.exclude_live:
        return "live/upcoming"
    if v.is_short and not s.include_shorts:
        return "short"
    if s.max_views and v.views is not None and v.views > s.max_views:
        return "above max_views"
    if s.published_after or s.published_before:
        r = _date_range_reason(v, s)
        if r:
            return r
    if s.min_views > 0:
        if v.views is None:
            return "views unknown"
        if v.views < s.min_views:
            if not (s.rising_views_per_day > 0 and _rising(v, s, now)):
                return "below view threshold"
    if v.duration_seconds is not None:
        if s.min_duration and v.duration_seconds < s.min_duration:
            return "too short"
        if s.max_duration and v.duration_seconds > s.max_duration:
            return "too long"
    max_age = s.effective_max_age_days() if s.within != "any" else s.max_age_days
    age = v.age_days(now)
    if s.max_age_days and age is None:
        return "upload date unknown"  # an explicit age limit can't be checked
    if max_age and age is not None:
        slack = 0 if v.published_exact else APPROX_SLACK_DAYS
        if age > max_age + slack:
            return "too old"
    title = v.title.lower()
    if s.title_must_contain and not any(w.lower() in title for w in s.title_must_contain):
        return "title missing required word"
    if s.exclude_words and any(w.lower() in title for w in s.exclude_words):
        return "title has excluded word"
    ch = {v.channel.lower(), v.channel_id.lower(), v.channel_handle.lower().lstrip("@")} - {""}
    if s.exclude_channels and any(x.lower().strip().lstrip("@") in ch for x in s.exclude_channels):
        return "excluded channel"
    if s.only_channels and not any(x.lower().strip().lstrip("@") in ch for x in s.only_channels):
        return "not one of only_channels"
    return None


def _date_range_reason(v: Video, s: Settings) -> str | None:
    from .config import parse_day

    pub = v.published_dt
    if pub is None:
        return "upload date unknown"
    day = pub.date()
    slack = dt.timedelta(days=0 if v.published_exact else APPROX_SLACK_DAYS)
    after, before = parse_day(s.published_after), parse_day(s.published_before)
    if after and day + slack < after:
        return "before published_after"
    if before and day - slack > before:
        return "after published_before"
    return None


def rank_newest(videos: list[Video]) -> list[Video]:
    """Newest first; unknown dates last; ties broken by more views."""
    def key(v: Video):
        p = v.published_dt
        return (p is not None, p or dt.datetime.min.replace(tzinfo=dt.timezone.utc), v.views or 0)
    return sorted(videos, key=key, reverse=True)


def sort_for_list(videos: list[Video], how: str = "newest") -> list[Video]:
    """The order of the saved list (and of the downloads): list_sort = newest | views | views_per_day."""
    if how == "views":
        return sorted(videos, key=lambda v: v.views if v.views is not None else -1, reverse=True)
    if how == "views_per_day":
        return sorted(videos, key=lambda v: v.views_per_day() or -1.0, reverse=True)
    return rank_newest(videos)


def _norm_title(t: str) -> str:
    """Comparable form of a title; "" for titles too generic to say two videos are the same
    (hashtags only, "Untitled", one or two words)."""
    import re

    text = re.sub(r"#\w+", " ", (t or "").lower())
    words = re.sub(r"[\W_]+", " ", text).split()
    return " ".join(words) if len(words) >= 3 else ""


def drop_reuploads(videos: list[Video], eligible=None) -> tuple[list[Video], int]:
    """Drop copies of the same video re-uploaded by other channels: identical title, a different channel and
    the same length. Only the most-viewed copy is kept (its transcript is the same)."""
    keep: list[Video] = []
    by_title: dict[str, list[Video]] = {}
    dropped = 0
    for v in sorted(videos, key=lambda x: x.views or 0, reverse=True):
        key = _norm_title(v.title) if (eligible is None or eligible(v)) else ""
        dup = None
        if key and v.duration_seconds:
            for other in by_title.get(key, []):
                same_len = other.duration_seconds and abs(other.duration_seconds - v.duration_seconds) <= max(
                    10, 0.03 * other.duration_seconds)
                different_channel = (other.channel_id or other.channel) != (v.channel_id or v.channel)
                if same_len and different_channel:
                    dup = other
                    break
        if dup is not None:
            dropped += 1
            for k in v.keyword.split("; "):  # the kept copy now also stands for this keyword
                if k and k not in dup.keyword.split("; "):
                    dup.keyword = f"{dup.keyword}; {k}" if dup.keyword else k
            continue
        keep.append(v)
        by_title.setdefault(key, []).append(v)
    order = {id(v): i for i, v in enumerate(videos)}
    keep.sort(key=lambda v: order[id(v)])
    return keep, dropped


def filter_and_rank(videos: list[Video], s: Settings, now: dt.datetime | None = None) -> tuple[list[Video], Counter]:
    now = now or dt.datetime.now(dt.timezone.utc)
    kept, reasons = [], Counter()
    for v in videos:
        r = reject_reason(v, s, now)
        if r:
            reasons[r] += 1
        else:
            kept.append(v)
    if s.drop_reuploads:
        kept, n = drop_reuploads(kept)
        if n:
            reasons["re-upload of another video"] += n
    kept = rank_newest(kept)
    if s.max_results and len(kept) > s.max_results:
        reasons["beyond max_results"] += len(kept) - s.max_results
        kept = kept[: s.max_results]
    return kept, reasons


def run_search(s: Settings, *, ydl_factory: Callable | None = None, api=None,
               should_stop: Callable[[], bool] | None = None) -> list[Video]:
    """Search every keyword (in parallel through proxies when there are several workers) and merge the
    results in keyword order, so the list is the same whichever search finishes first."""
    import threading

    from .proxies import ProxyPool
    from .search_api import ApiError

    backend = s.resolved_backend()
    log.info("Search backend: %s", "YouTube Data API" if backend == "api" else "yt-dlp (no API key)")
    keywords = s.all_keywords()
    # the API's quota belongs to the key, not the IP: no point in parallel API searches
    n_workers = min(s.resolved_workers("search"), len(keywords)) if backend == "ytdlp" else 1
    proxies = s.stage_proxies("search")
    if s.proxy and not proxies and s.proxy_for_transcripts:
        log.info("Searching over your own connection (proxies are used for the transcripts only).")
    from .pipeline import _rotating_setting

    pool = ProxyPool(proxies, per_proxy=int(s.workers_per_proxy or 1), direct_capacity=max(1, n_workers),
                     rotating=_rotating_setting(s))
    n_workers = max(1, min(n_workers, pool.total_capacity()))  # more would only wait for a free proxy
    outcomes: dict[int, tuple[list[Video] | None, Exception | None]] = {}
    first = s.proxy if proxies else ""
    last_ok_proxy = [first]
    next_kw = [0]
    lock = threading.Lock()

    def stopping() -> bool:
        return bool(should_stop and should_stop())

    def worker(prefer_url: str) -> None:
        prefer = next((x for x in pool.slots if x.url == prefer_url), None) if prefer_url else None
        while not stopping():
            with lock:
                i = next_kw[0]
                next_kw[0] += 1
            if i >= len(keywords):
                return
            kept, exc = _keyword_with_retries(i, keywords, s, pool, prefer, backend, ydl_factory, api,
                                              should_stop, last_ok_proxy, tag=n_workers > 1)
            prefer = None
            with lock:
                outcomes[i] = (kept, exc)

    if n_workers <= 1:
        worker(first)
    else:
        threads = [threading.Thread(target=worker, args=(first if k == 0 else "",), name=f"search{k + 1}",
                                    daemon=True) for k in range(n_workers)]
        for th in threads:
            th.start()
        for th in threads:
            while th.is_alive():
                th.join(timeout=0.2)
    if stopping():
        log.warning("Search stopped.")
    if proxies and s.proxy != last_ok_proxy[0] and last_ok_proxy[0]:
        s.proxy = last_ok_proxy[0]  # downloads start with a proxy that just worked

    combined: dict[str, Video] = {}
    failed, last_exc = [], None
    for i in range(len(keywords)):  # keyword order, whatever order the searches finished in
        kept, exc = outcomes.get(i, (None, None))
        if exc is not None:
            failed.append(keywords[i])
            last_exc = exc
        for v in kept or []:
            if v.video_id in combined:
                combined[v.video_id].merge(v)
            else:
                combined[v.video_id] = v
    if failed and len(failed) == len(keywords):
        if isinstance(last_exc, ApiError) and last_exc.quota_exceeded:
            raise RuntimeError("The YouTube API daily quota is used up - try again tomorrow, or set "
                               "backend = \"auto\" so the key-less search takes over.")
        if "cookies" in str(last_exc):
            raise RuntimeError(f"every YouTube search failed: {last_exc}.")
        raise RuntimeError(f"every YouTube search failed - last error: {last_exc}. Check your internet "
                           "connection; if it works, YouTube may be limiting you, so wait a while and try again.")
    result = list(combined.values())
    if len(keywords) > 1:  # the same re-upload can be found under two keywords

        def eligible(v: Video) -> bool:
            return all(s.for_keyword(k).drop_reuploads for k in v.keyword.split("; ") if k)

        result, n = drop_reuploads(result, eligible)
        if n:
            log.info("Dropped %d re-uploaded cop%s found under another keyword.", n, "y" if n == 1 else "ies")
    return rank_newest(result)


def _keyword_with_retries(i, keywords, s: Settings, pool, prefer, backend, ydl_factory, api, should_stop,
                          last_ok_proxy, tag: bool) -> tuple[list[Video] | None, Exception | None]:
    """Search one keyword through a leased slot; on failure retry once through every other free slot."""
    import copy

    from .pipeline import _looks_offline
    from .search_api import ApiError
    from .search_ytdlp import SearchFailed

    kw = keywords[i]
    ks = s.for_keyword(kw)
    extra = "" if ks is s else f"  (own settings: {ks.min_views:,}+ views, {ks.within})"
    log.info("[%d/%d] Keyword: %r%s", i + 1, len(keywords), kw, extra)
    tried = 0
    last_exc: Exception | None = None
    while tried < min(len(pool.slots), 10):  # a long list: try at most 10 proxies for one keyword
        slot = _lease_for_search(pool, prefer, should_stop)
        if slot is None:
            break
        prefer = None
        tried += 1
        if slot.url and _data_limit_hit():
            pool.release(slot)
            return None, SearchFailed(_data_limit_hit())
        ws = copy.copy(ks)  # this keyword's own copy: never shares a proxy setting with another search
        ws.proxy = netmeter.route(slot.url)  # through the data meter's relay (counts the bytes)
        try:
            raw = _search_one(kw, ws, backend, ydl_factory, api, should_stop)
        except (SearchFailed, ApiError) as exc:
            last_exc = exc
            if getattr(exc, "quota_exceeded", False) or len(pool.slots) == 1:
                pool.release(slot)
                break
            pool.trouble(slot, dead=_looks_offline(str(exc)))
            pool.release(slot)
            log.warning("  searching through %s failed (%s) - retrying with another proxy", slot.label, exc)
            continue
        pool.ok(slot)
        pool.release(slot)
        if slot.url:
            last_ok_proxy[0] = slot.url
        if ws.backend == "ytdlp" and s.backend != "ytdlp":  # the API fell back: keep it for later keywords
            s.backend = "ytdlp"
        return _finish_keyword(kw, raw, ws, s.resolved_backend(), ydl_factory, tag), None
    log.error("  every search for %r failed: %s", kw, last_exc)
    return None, last_exc or SearchFailed("no proxy was free")


def _data_limit_hit() -> str:
    sess = netmeter.active()
    return sess.limit_message() if sess is not None and sess.limit_reached() else ""


def _lease_for_search(pool, prefer, should_stop):
    """A free slot; waits while another search is using one (it will hand it back soon). Gives up only
    when every slot is resting after a block or dead - then this keyword fails like a failed search."""
    while not (should_stop and should_stop()):
        slot = pool.try_lease(prefer)
        if slot is not None:
            return slot
        with pool.cond:
            if not any(x.leases for x in pool.slots if not x.retired):
                return None  # nobody will hand one back: all resting or dead
            pool.cond.wait(0.5)
    return None


def _finish_keyword(kw: str, raw: list[Video], ks: Settings, backend: str, ydl_factory, tag: bool) -> list[Video]:
    """View-count fallback, exact dates and filtering for one keyword's raw results."""
    pre_tag = f"  [{kw}]" if tag else " "
    missing = [v for v in raw if v.views is None and not v.is_short and v.live_status not in ("is_live", "is_upcoming")]
    if backend == "ytdlp" and ks.min_views > 0 and len(missing) >= max(3, len(raw) // 2):
        # YouTube changed its search page and stopped showing views: look them up one by one (slower)
        from .search_ytdlp import enrich_exact

        missing = rank_newest(missing)[:MAX_VIEW_LOOKUPS]
        log.warning("%s YouTube's search results came without view counts - looking up %d videos one by one "
                    "(slower; run update.bat later, a newer yt-dlp may fix this).", pre_tag, len(missing))
        enrich_exact(missing, ks, ydl_factory)
    if backend == "ytdlp" and ks.exact_dates and raw:
        from .search_ytdlp import enrich_exact

        # only look up candidates that could pass, to save time
        pre, _ = filter_and_rank(raw, _relaxed(ks))
        log.info("%s looking up exact dates for %d candidates...", pre_tag, len(pre))
        enrich_exact(pre, ks, ydl_factory)
    kept, reasons = filter_and_rank(raw, ks)
    detail = ", ".join(f"{n} {r}" for r, n in reasons.most_common())
    log.info("%s %d found -> %d kept%s", pre_tag, len(raw), len(kept), f"  (dropped: {detail})" if detail else "")
    return kept


def _search_one(kw: str, s: Settings, backend: str, ydl_factory, api, should_stop=None) -> list[Video]:
    if backend == "api":
        from .search_api import ApiError, search_keyword

        try:
            return search_keyword(kw, s, api=api)
        except ApiError as exc:
            if s.backend == "auto":
                why = "API quota exhausted" if exc.quota_exceeded else f"API problem ({exc})"
                log.warning("  %s - using key-less search for the rest of the run.", why)
                s.backend = "ytdlp"
                return _search_one(kw, s, "ytdlp", ydl_factory, api, should_stop)
            raise
    from .search_ytdlp import search_keyword

    return search_keyword(kw, s, ydl_factory=ydl_factory, should_stop=should_stop)


def _relaxed(s: Settings) -> Settings:
    """Copy of settings with the result cap removed (used before exact-date lookups)."""
    import copy

    r = copy.copy(s)
    r.max_results = max(s.max_results * 2, 0) if s.max_results else 0
    return r
