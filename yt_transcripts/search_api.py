"""Keyword search through the official YouTube Data API v3 (needs a free API key).

Advantages over the key-less backend: real "newest first" ordering, exact publish
times and exact view counts.  Cost: search.list = 100 quota units per page of 50,
videos.list = 1 unit per 50 videos; the free daily quota is 10,000 units.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from typing import Any

from .config import Settings
from .models import Video
from .utils import iso_utc

log = logging.getLogger("yt_transcripts")

API = "https://www.googleapis.com/youtube/v3"
ORDER_FOR_SORT = {"popularity": "viewCount", "views": "viewCount", "relevance": "relevance"}


class ApiError(RuntimeError):
    def __init__(self, message: str, reason: str = "", status: int = 0):
        super().__init__(message)
        self.reason = reason
        self.status = status

    @property
    def quota_exceeded(self) -> bool:
        return self.reason in ("quotaExceeded", "dailyLimitExceeded", "rateLimitExceeded")


_ISO_DUR = re.compile(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def parse_iso_duration(s: str) -> int | None:
    m = _ISO_DUR.fullmatch(s or "")
    if not m or not any(m.groups()):
        return None
    d, h, mi, se = (int(x) if x else 0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


class YouTubeApi:
    def __init__(self, key: str, session=None, proxy: str = ""):
        import requests

        self.key = key
        self.session = session or requests.Session()
        if proxy:
            self.session.trust_env = False  # otherwise HTTPS_PROXY / the Windows proxy would win over ours
            self.session.proxies.update({"http": proxy, "https": proxy})
        self.quota_used = 0

    def _get(self, endpoint: str, params: dict[str, Any], cost: int) -> dict:
        params = {**params, "key": self.key}
        import requests

        try:
            r = self.session.get(f"{API}/{endpoint}", params=params, timeout=30)
        except requests.RequestException as e:
            raise ApiError(f"could not reach the YouTube API ({e.__class__.__name__})", "network", 0) from e
        self.quota_used += cost
        try:
            data = r.json()
        except ValueError:
            data = {}
        if r.status_code != 200 or "error" in data:
            err = data.get("error", {}) if isinstance(data, dict) else {}
            reason = ""
            if err.get("errors"):
                reason = err["errors"][0].get("reason", "")
            msg = err.get("message") or f"HTTP {r.status_code}"
            raise ApiError(f"YouTube API error: {msg} ({reason or r.status_code})", reason, r.status_code)
        return data

    def search_ids(self, query: str, order: str, published_after: dt.datetime | None,
                   limit: int, captions_only: bool = False, language: str = "") -> list[str]:
        ids: list[str] = []
        token = None
        while len(ids) < limit:
            params: dict[str, Any] = {
                "part": "id",
                "q": query,
                "type": "video",
                "order": order,
                "maxResults": min(50, limit - len(ids)),
            }
            if published_after:
                params["publishedAfter"] = iso_utc(published_after).replace("+00:00", "Z")
            if captions_only:
                params["videoCaption"] = "closedCaption"
            if language:
                params["relevanceLanguage"] = language
            if token:
                params["pageToken"] = token
            data = self._get("search", params, cost=100)
            for item in data.get("items", []):
                vid = item.get("id", {}).get("videoId")
                if vid and vid not in ids:
                    ids.append(vid)
            token = data.get("nextPageToken")
            if not token or not data.get("items"):
                break
        return ids

    def videos(self, ids: list[str]) -> list[dict]:
        out = []
        for i in range(0, len(ids), 50):
            chunk = ids[i:i + 50]
            data = self._get("videos", {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(chunk),
                "maxResults": 50,
            }, cost=1)
            out.extend(data.get("items", []))
        return out


def item_to_video(item: dict, keyword: str) -> Video:
    sn = item.get("snippet", {})
    st = item.get("statistics", {})
    cd = item.get("contentDetails", {})
    dur = parse_iso_duration(cd.get("duration", ""))
    text = (sn.get("title", "") + " " + sn.get("description", "")).lower()
    is_short = dur is not None and (dur <= 60 or (dur <= 180 and "#short" in text))
    live = sn.get("liveBroadcastContent", "none")
    return Video(
        video_id=item["id"],
        title=sn.get("title", ""),
        channel=sn.get("channelTitle", ""),
        channel_id=sn.get("channelId", ""),
        views=int(st["viewCount"]) if st.get("viewCount") is not None else None,
        published=sn.get("publishedAt", ""),
        published_exact=bool(sn.get("publishedAt")),
        duration_seconds=dur,
        is_short=is_short,
        live_status={"live": "is_live", "upcoming": "is_upcoming"}.get(live, ""),
        keyword=keyword,
        source="youtube-data-api",
        description=sn.get("description", "")[:500],
    )


def search_keyword(keyword: str, settings: Settings, api: YouTubeApi | None = None) -> list[Video]:
    api = api or YouTubeApi(settings.resolved_api_key(), proxy=settings.proxy)
    max_age = settings.effective_max_age_days() if settings.within != "any" else settings.max_age_days
    after = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=max_age) if max_age else None
    orders = ["date"] + [ORDER_FOR_SORT[s] for s in settings.sorts if ORDER_FOR_SORT.get(s) not in (None, "relevance")]
    ids: list[str] = []
    for order in dict.fromkeys(orders):
        log.info("  searching (API, order=%s)", order)
        for vid in api.search_ids(keyword, order, after, settings.scan_per_keyword,
                                  captions_only=settings.subtitles_only,
                                  language=settings.search_language):
            if vid not in ids:
                ids.append(vid)
    videos = [item_to_video(it, keyword) for it in api.videos(ids)]
    log.debug("  API quota used so far: %d units", api.quota_used)
    return videos
