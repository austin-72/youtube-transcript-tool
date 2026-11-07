"""Exact upload dates (and view counts) from YouTube's channel feeds.

Every channel has a small public feed - https://www.youtube.com/feeds/videos.xml?channel_id=UC... -
listing its 15 newest uploads with the exact publish time and view count, roughly 10 kB compressed.
The data saver skips the watch page, which is where yt-dlp finds exact dates; the feed fills them in
for far less: one request per channel per run, shared by all of that channel's videos. It goes the
way searches go (your own connection, unless proxy_for_search is on - then through the proxy, and the
few kB are counted like everything else).

Only videos among a channel's 15 newest are in its feed, which covers "newest videos" searches. Older
videos keep the approximate date from the search ("3 weeks ago"), marked with ~ as before.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
import threading
from typing import Callable

log = logging.getLogger("yt_transcripts")

FEED_URL = "https://www.youtube.com/feeds/videos.xml"
TIMEOUT = 10
MAX_CHANNELS = 500  # feed requests per run, at most
_CHANNEL_ID = re.compile(r"UC[\w-]{22}")
_ENTRY = re.compile(r"<entry>(.*?)</entry>", re.S)
_VIDEO_ID = re.compile(r"<yt:videoId>([\w-]{11})</yt:videoId>")
_PUBLISHED = re.compile(r"<published>([^<]{10,40})</published>")
_VIEWS = re.compile(r"<media:statistics\b[^>]*\bviews=\"(\d+)\"")


def parse_feed(text: str) -> dict[str, tuple[str, int | None]]:
    """{video_id: (published as UTC ISO time, views or None)} from a channel feed."""
    from .models import parse_iso
    from .utils import iso_utc

    out: dict[str, tuple[str, int | None]] = {}
    for m in _ENTRY.finditer(text or ""):
        entry = m.group(1)
        vid, pub = _VIDEO_ID.search(entry), _PUBLISHED.search(entry)
        if not vid or not pub:
            continue
        when = parse_iso(pub.group(1).strip())
        if when is None or when.year < 2005 or when > dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=2):
            continue
        views = _VIEWS.search(entry)
        out[vid.group(1)] = (iso_utc(when), int(views.group(1)) if views else None)
    return out


class FeedDates:
    """Looks up videos in their channel's feed; each feed is downloaded once per run. Thread-safe."""

    def __init__(self, s, *, get: Callable[[str, dict], str | None] | None = None):
        self.s = s
        self._get = get
        self._feeds: dict[str, dict | None] = {}
        self._locks: dict[str, threading.Lock] = {}
        self._lock = threading.Lock()
        self._local = threading.local()
        self.requests = 0
        self.found = 0

    def _session(self):
        sess = getattr(self._local, "session", None)
        if sess is None:
            import requests

            from . import netmeter

            sess = requests.Session()
            proxies = self.s.stage_proxies("search")
            if proxies:  # searches go through the proxy: so does this (counted by the data meter)
                url = netmeter.route(proxies[0])
                sess.trust_env = False
                sess.proxies = {"http": url, "https": url}
            sess.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
            self._local.session = sess
        return sess

    def _download(self, channel_id: str) -> dict | None:
        params = {"channel_id": channel_id}
        try:
            if self._get is not None:
                text = self._get(FEED_URL, params)
            else:
                r = self._session().get(FEED_URL, params=params, timeout=TIMEOUT)
                if r.status_code == 404:
                    return {}
                r.raise_for_status()
                text = r.text
        except Exception as e:  # noqa: BLE001 - a missing feed only means the date stays approximate
            log.debug("channel feed for %s not available: %s", channel_id, e)
            return None
        return parse_feed(text or "")

    def lookup(self, video_id: str, channel_id: str) -> tuple[str, int | None] | None:
        """(exact published time, views) if the video is in its channel's feed, else None."""
        if not video_id or not _CHANNEL_ID.fullmatch(channel_id or ""):
            return None
        with self._lock:
            lock = self._locks.setdefault(channel_id, threading.Lock())
        with lock:  # one download per channel, even with several workers asking at once
            if channel_id not in self._feeds:
                with self._lock:
                    if self.requests >= MAX_CHANNELS:
                        return None
                    self.requests += 1
                self._feeds[channel_id] = self._download(channel_id)
            feed = self._feeds[channel_id]
        hit = (feed or {}).get(video_id)
        if hit:
            with self._lock:
                self.found += 1
        return hit


def fill_dates(videos, s, *, feeds: FeedDates | None = None, views: bool = False) -> list:
    """Give videos with approximate dates their exact one from the feed. Returns the videos it couldn't."""
    if not getattr(s, "feed_dates", True):
        return [v for v in videos if not v.published_exact]
    feeds = feeds or FeedDates(s)
    rest = []
    for v in videos:
        if v.published_exact:
            continue
        hit = feeds.lookup(v.video_id, v.channel_id)
        if not hit:
            rest.append(v)
            continue
        v.published, v.published_exact = hit[0], True
        if views and hit[1] is not None:
            v.views = hit[1]
    return rest
