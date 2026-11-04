import datetime as dt

import pytest

from yt_transcripts import search as search_mod
from yt_transcripts.config import build_settings
from yt_transcripts.search_api import ApiError, YouTubeApi, item_to_video, parse_iso_duration, search_keyword


class FakeResp:
    def __init__(self, status, data):
        self.status_code, self._data = status, data

    def json(self):
        return self._data


class FakeSession:
    """Serves search pages and video details like the real API, and records every call."""

    def __init__(self, pages=None, quota_after=None):
        self.calls = []
        self.proxies = {}
        self.pages = pages or {}
        self.quota_after = quota_after

    def get(self, url, params=None, timeout=None):
        self.calls.append((url.rsplit("/", 1)[-1], dict(params)))
        if self.quota_after is not None and len(self.calls) > self.quota_after:
            return FakeResp(403, {"error": {"message": "quota", "errors": [{"reason": "quotaExceeded"}]}})
        if url.endswith("/search"):
            key = (params["order"], params.get("pageToken"))
            items, nxt = self.pages.get(key, ([], None))
            data = {"items": [{"id": {"videoId": i}} for i in items]}
            if nxt:
                data["nextPageToken"] = nxt
            return FakeResp(200, data)
        ids = params["id"].split(",")
        return FakeResp(200, {"items": [_item(i) for i in ids]})


def _item(vid, views=50_000, days=1, dur="PT12M3S", title="A tutorial", live="none"):
    pub = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"id": vid,
            "snippet": {"title": title, "description": "desc", "channelTitle": "Chan", "channelId": "UC123",
                        "publishedAt": pub, "liveBroadcastContent": live},
            "statistics": {"viewCount": str(views)},
            "contentDetails": {"duration": dur}}


@pytest.mark.parametrize("s,expected", [
    ("PT12M3S", 723), ("PT1H", 3600), ("PT45S", 45), ("P1DT2H", 93600), ("", None), ("P0D", 0),
])
def test_parse_iso_duration(s, expected):
    assert parse_iso_duration(s) == expected


def test_item_to_video():
    v = item_to_video(_item("abcdefghijk", dur="PT58S", title="Quick tip #shorts"), "kw")
    assert v.views == 50_000 and v.duration_seconds == 58 and v.is_short and v.published_exact
    assert v.source == "youtube-data-api" and v.keyword == "kw"
    assert item_to_video(_item("abcdefghijk", live="upcoming"), "kw").live_status == "is_upcoming"


def test_search_pages_and_orders():
    pages = {
        ("date", None): (["a" * 11, "b" * 11], "P2"),
        ("date", "P2"): (["c" * 11], None),
        ("viewCount", None): (["b" * 11, "d" * 11], None),
    }
    sess = FakeSession(pages)
    api = YouTubeApi("KEY", session=sess)
    s = build_settings({"keywords": ["k"], "within": "week", "scan_per_keyword": 100, "api_key": "KEY",
                        "sorts": ["popularity", "relevance"]})
    vids = search_keyword("k", s, api=api)
    assert sorted(v.video_id for v in vids) == ["a" * 11, "b" * 11, "c" * 11, "d" * 11]
    search_calls = [p for name, p in sess.calls if name == "search"]
    assert {p["order"] for p in search_calls} == {"date", "viewCount"}
    assert all(p["publishedAfter"].endswith("Z") and p["type"] == "video" for p in search_calls)
    assert api.quota_used == 3 * 100 + 1


def test_quota_error_is_reported():
    api = YouTubeApi("KEY", session=FakeSession(quota_after=0))
    with pytest.raises(ApiError) as ei:
        api.search_ids("k", "date", None, 10)
    assert ei.value.quota_exceeded


def test_auto_backend_falls_back_when_quota_runs_out(monkeypatch):
    s = build_settings({"keywords": ["k"], "api_key": "KEY", "backend": "auto"})
    calls = []

    def fake_api_search(kw, settings, api=None):
        raise ApiError("quota", "quotaExceeded", 403)

    def fake_ytdlp_search(kw, settings, ydl_factory=None, should_stop=None):
        calls.append(kw)
        return []

    monkeypatch.setattr("yt_transcripts.search_api.search_keyword", fake_api_search)
    monkeypatch.setattr("yt_transcripts.search_ytdlp.search_keyword", fake_ytdlp_search)
    assert search_mod.run_search(s) == []
    assert calls == ["k"] and s.backend == "ytdlp"


def test_explicit_api_backend_raises_on_quota(monkeypatch):
    s = build_settings({"keywords": ["k"], "api_key": "KEY", "backend": "api"})
    monkeypatch.setattr("yt_transcripts.search_api.search_keyword",
                        lambda kw, settings, api=None: (_ for _ in ()).throw(ApiError("q", "quotaExceeded")))
    with pytest.raises(RuntimeError, match="quota is used up"):
        search_mod.run_search(s)


def test_network_error_becomes_api_error_and_keyword_is_skipped():
    import requests

    from yt_transcripts.config import build_settings
    from yt_transcripts.search import run_search
    from yt_transcripts.search_api import YouTubeApi

    class DeadSession:
        def get(self, *a, **k):
            raise requests.ConnectionError("no route")

    api = YouTubeApi("KEY", session=DeadSession())
    s = build_settings({"keywords": ["a", "b"], "backend": "api", "api_key": "KEY"})
    import pytest

    with pytest.raises(RuntimeError, match="every YouTube search failed"):
        run_search(s, api=api)
