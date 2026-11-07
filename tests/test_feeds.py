import datetime as dt
import json
import threading

from yt_transcripts import feeds, pipeline
from yt_transcripts.config import build_settings
from yt_transcripts.models import Segment, Transcript, Video

CID = "UC" + "a" * 22


def _feed(*entries):
    body = "".join(
        f"<entry><id>yt:video:{vid}</id><yt:videoId>{vid}</yt:videoId><yt:channelId>{CID}</yt:channelId>"
        f"<title>T &amp; more</title><published>{pub}</published><updated>2026-11-05T00:00:00+00:00</updated>"
        f'<media:group><media:community><media:starRating count="5"/><media:statistics views="{views}"/>'
        f"</media:community></media:group></entry>"
        for vid, pub, views in entries)
    return ('<?xml version="1.0" encoding="UTF-8"?><feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" '
            f'xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">{body}</feed>')


def test_parse_feed_reads_exact_dates_and_views():
    out = feeds.parse_feed(_feed(("vid00000001", "2026-11-03T15:04:05+00:00", 1234),
                                 ("vid00000002", "2026-11-02T08:00:00-05:00", 0),
                                 ("vid00000003", "not a date", 5)))
    assert out == {"vid00000001": ("2026-11-03T15:04:05+00:00", 1234),
                   "vid00000002": ("2026-11-02T13:00:00+00:00", 0)}
    assert feeds.parse_feed("") == {} and feeds.parse_feed("<html>error</html>") == {}


def test_each_channel_feed_is_downloaded_once_even_from_several_workers():
    calls = []
    gate = threading.Event()

    def get(url, params):
        calls.append(params["channel_id"])
        gate.wait(1)
        return _feed(("vid00000001", "2026-11-03T15:04:05+00:00", 7))
    fd = feeds.FeedDates(build_settings({}), get=get)
    out = []
    ts = [threading.Thread(target=lambda: out.append(fd.lookup("vid00000001", CID))) for _ in range(6)]
    for t in ts:
        t.start()
    gate.set()
    for t in ts:
        t.join()
    assert calls == [CID] and out == [("2026-11-03T15:04:05+00:00", 7)] * 6
    assert fd.lookup("vid00000009", CID) is None and calls == [CID]  # not in the feed: no new request
    assert fd.lookup("vid00000001", "not-a-channel") is None and calls == [CID]


def test_a_failed_feed_leaves_the_date_alone():
    def boom(url, params):
        raise OSError("down")
    fd = feeds.FeedDates(build_settings({}), get=boom)
    v = Video("vid00000001", channel_id=CID, published="2026-11-01", published_exact=False)
    assert feeds.fill_dates([v], build_settings({}), feeds=fd) == [v]
    assert v.published == "2026-11-01" and not v.published_exact


def test_the_feed_follows_the_search_route():
    import requests

    direct = feeds.FeedDates(build_settings({}))._session()
    assert not direct.proxies
    proxied = feeds.FeedDates(build_settings({"proxy": "http://u:p@h:1", "proxy_for_search": True}))._session()
    assert proxied.proxies["https"] == "http://u:p@h:1" and proxied.trust_env is False
    own = feeds.FeedDates(build_settings({"proxy": "http://u:p@h:1", "proxy_for_search": False}))._session()
    assert not own.proxies and isinstance(own, requests.Session)


def test_downloads_get_exact_dates_from_the_feed(tmp_path, monkeypatch):
    class F:
        name, last_info, last_comments = "ytdlp", None, []

        def fetch(self, v):
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp", [Segment(0, 1, "hello there")])
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [F()])
    asked = []

    def download(self, cid):
        asked.append(cid)
        return feeds.parse_feed(_feed(("vid00000001", "2026-11-03T15:04:05+00:00", 9)))
    monkeypatch.setattr(feeds.FeedDates, "_download", download)
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt", "json"]})
    a = Video("vid00000001", title="A", keyword="k", channel_id=CID, published="2026-11-02", published_exact=False)
    b = Video("vid00000002", title="B", keyword="k", channel_id=CID, published="2026-10-01", published_exact=False)
    c = Video("vid00000003", title="C", keyword="k", channel_id=CID, published="2026-11-04T10:00:00+00:00",
              published_exact=True)
    pipeline.download_all([a, b, c], s)
    assert asked == [CID]  # one request for the channel; the video with an exact date needs none
    assert a.published == "2026-11-03T15:04:05+00:00" and a.published_exact
    assert not b.published_exact  # older than the feed reaches: stays approximate
    m = json.loads((tmp_path / "manifest.json").read_text())
    assert m["vid00000001"]["published_exact"] is True
    assert "2026-11-03" in next(p.name for p in (tmp_path / "transcripts" / "k").glob("*vid00000001*.txt"))
    asked.clear()
    s2 = build_settings({"keywords": ["k"], "output_dir": str(tmp_path / "o2"), "delay_seconds": 0,
                         "feed_dates": False})
    pipeline.download_all([Video("vid00000004", title="D", keyword="k", channel_id=CID)], s2)
    assert asked == []


def test_exact_dates_search_option_uses_the_feed_before_video_pages(monkeypatch):
    from yt_transcripts.search_ytdlp import enrich_exact

    monkeypatch.setattr(feeds.FeedDates, "_download",
                        lambda self, cid: feeds.parse_feed(_feed(("vid00000001", "2026-11-03T15:04:05+00:00", 42))))
    looked = []

    class YDL:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def extract_info(self, url, download=False, process=False):
            looked.append(url)
            return {"timestamp": int(dt.datetime(2025, 1, 2, tzinfo=dt.timezone.utc).timestamp()), "view_count": 5}
    a = Video("vid00000001", channel_id=CID, published="2026-11-02", views=None)
    b = Video("vid00000002", channel_id=CID, published="2025-01-01", views=None)
    enrich_exact([a, b], build_settings({"delay_seconds": 0}), ydl_factory=lambda **k: YDL())
    assert a.published_exact and a.views == 42 and a.published.startswith("2026-11-03")
    assert looked == ["https://www.youtube.com/watch?v=vid00000002"] and b.views == 5  # only the one not in the feed
