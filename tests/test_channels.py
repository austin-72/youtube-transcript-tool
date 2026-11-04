"""Whole channels: link parsing, newest-first listing with early stop, filters, the `channel` command."""

import datetime as dt

import pytest

from yt_transcripts import channels
from yt_transcripts.config import build_settings


@pytest.mark.parametrize("spec,url,pl", [
    ("@mkbhd", "https://www.youtube.com/@mkbhd", False),
    ("mkbhd", "https://www.youtube.com/@mkbhd", False),
    ("https://www.youtube.com/@mkbhd/videos", "https://www.youtube.com/@mkbhd", False),
    ("youtube.com/@mkbhd/shorts?view=0", "https://www.youtube.com/@mkbhd", False),
    ("UCBJycsmduvYEL83R_U4JriQ", "https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ", False),
    ("https://m.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ/featured",
     "https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ", False),
    ("https://www.youtube.com/c/SomeName", "https://www.youtube.com/c/SomeName", False),
    ("https://www.youtube.com/user/oldname/", "https://www.youtube.com/user/oldname", False),
    ("https://www.youtube.com/playlist?list=PLabcdefghijklmnop", "https://www.youtube.com/playlist?list=PLabcdefghijklmnop", True),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLzzzzzzzzzzzz", "https://www.youtube.com/playlist?list=PLzzzzzzzzzzzz", True),
    ("PLabcdefghijklmnop", "https://www.youtube.com/playlist?list=PLabcdefghijklmnop", True),
])
def test_channel_url(spec, url, pl):
    assert channels.channel_url(spec) == (url, pl)


@pytest.mark.parametrize("bad", ["", "two words", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                                 "https://example.com/@x"])
def test_bad_channel_specs(bad):
    with pytest.raises(channels.ChannelError):
        channels.channel_url(bad)


def _entry(i, days_old, views=1000, dur=600, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    return {"id": f"vid{i:08d}", "ie_key": "Youtube", "url": f"https://www.youtube.com/watch?v=vid{i:08d}",
            "title": f"Upload {i}", "view_count": views, "duration": dur,
            "timestamp": (now - dt.timedelta(days=days_old)).timestamp()}


class FakeTabYdl:
    """Pretends to be yt-dlp listing channel tabs; counts how many entries were consumed."""

    def __init__(self, tabs, consumed, urls):
        self.tabs, self.consumed, self.urls = tabs, consumed, urls

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def extract_info(self, url, download=False, process=False):
        self.urls.append(url)
        tab = url.rsplit("/", 1)[1]
        if tab not in self.tabs:
            raise Exception(f"ERROR: [youtube:tab] @chan: This channel does not have a {tab} tab")

        def gen():
            for e in self.tabs[tab]:
                self.consumed.append(e["id"])
                yield e
        return {"channel": "The Channel", "uploader_id": "@chan", "channel_id": "UC" + "x" * 22,
                "title": "The Channel - Videos", "entries": gen()}


def _factory(tabs):
    consumed, urls = [], []
    return (lambda **kw: FakeTabYdl(tabs, consumed, urls)), consumed, urls


def S(**kw):
    return build_settings({"keywords": ["x"], **kw})


def test_lists_every_video_and_fills_channel_details():
    vids = [_entry(i, i) for i in range(30)]
    f, consumed, urls = _factory({"videos": vids})
    out, label = channels.list_channel("@chan", S(), ydl_factory=f)
    assert label == "@chan" and len(out) == 30 and len(consumed) == 30
    v = out[0]
    assert (v.channel, v.channel_handle, v.keyword, v.source) == ("The Channel", "@chan", "@chan", "channel")
    assert urls == ["https://www.youtube.com/@chan/videos"]


def test_stops_paging_once_uploads_are_too_old():
    vids = [_entry(i, i * 3) for i in range(200)]  # one every 3 days
    f, consumed, _ = _factory({"videos": vids})
    out, _ = channels.list_channel("@chan", S(channel_within="month"), ydl_factory=f)
    assert 9 <= len(out) <= 11
    assert len(consumed) < 20  # stopped early instead of reading all 200


def test_newest_n_stops_early_and_respects_filters():
    vids = [_entry(i, i, views=500 if i % 2 else 5000) for i in range(300)]
    f, consumed, _ = _factory({"videos": vids})
    out, _ = channels.list_channel("@chan", S(channel_max_videos=5, channel_min_views=1000), ydl_factory=f)
    assert [v.video_id for v in out] == [f"vid{i:08d}" for i in (0, 2, 4, 6, 8)]
    assert len(consumed) <= 10


def test_missing_tab_is_fine_and_shorts_are_marked():
    f, _, urls = _factory({"videos": [_entry(1, 1)], "shorts": [_entry(2, 2, dur=30)]})
    out, _ = channels.list_channel("@chan", S(channel_tabs=["videos", "shorts", "streams"]), ydl_factory=f)
    assert {v.video_id: v.is_short for v in out} == {"vid00000001": False, "vid00000002": True}
    assert len(urls) == 3


def test_keyword_filters_dont_apply_but_length_and_dates_do():
    now = dt.datetime.now(dt.timezone.utc)
    vids = [_entry(1, 2, dur=60), _entry(2, 3), _entry(3, 40)]
    f, _, _ = _factory({"videos": vids})
    after = (now - dt.timedelta(days=10)).date().isoformat()
    s = S(title_must_contain=["nothing matches this"], min_duration=120, published_after=after, min_views=10**9)
    out, _ = channels.list_channel("@chan", s, ydl_factory=f)
    assert [v.video_id for v in out] == ["vid00000002"]


def test_run_channels_through_the_command(tmp_path, monkeypatch):
    from yt_transcripts import cli, pipeline
    from yt_transcripts import transcripts as tr
    from yt_transcripts.models import Segment, Transcript

    vids = [_entry(i, i) for i in range(4)]
    f, _, _ = _factory({"videos": vids})
    real = channels.list_channel
    monkeypatch.setattr(channels, "list_channel", lambda spec, s, **kw: real(spec, s, ydl_factory=f))

    class Fetch:
        name, last_info = "ytdlp", None

        def fetch(self, v):
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp", [Segment(0, 2, f"text {v.video_id} mkbhd")])
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [Fetch()])
    out = tmp_path / "out"
    cfg = tmp_path / "c.toml"
    cfg.write_text('delay_seconds = 0\nformats = ["txt", "json"]\n', encoding="utf-8")
    assert cli.main(["channel", "@chan", "-c", str(cfg), "-o", str(out)]) == 0
    files = sorted(p.name for p in (out / "transcripts" / "@chan").glob("*.txt"))
    assert len(files) == 4
    assert (out / "channel_list.csv").exists() and not (out / "video_list.csv").exists()
    html = (out / "channel_list.html").read_text(encoding="utf-8")
    assert "Channel @chan" in html
    import json

    rows = json.loads((out / "channel_list.json").read_text(encoding="utf-8"))
    assert all(r["keyword_mentions"] is None for r in rows)
    assert cli.main(["channel", "-c", str(cfg), "-o", str(out)]) == 2  # no channel given or configured
    assert tr.OK == "ok"


def test_run_includes_configured_channels(tmp_path, monkeypatch):
    from yt_transcripts import cli, search

    f, _, _ = _factory({"videos": [_entry(1, 1), _entry(2, 2)]})
    real = channels.list_channel
    monkeypatch.setattr(channels, "list_channel", lambda spec, s, **kw: real(spec, s, ydl_factory=f))
    called = []
    monkeypatch.setattr(search, "run_search", lambda s, **kw: called.append(1) or [])
    cfg = tmp_path / "c.toml"
    cfg.write_text('channels = ["@chan"]\ndownload_transcripts = false\n', encoding="utf-8")
    assert cli.main(["search", "-c", str(cfg), "-o", str(tmp_path / "o")]) == 0
    assert called == []  # no keywords: no keyword search
    import csv

    rows = list(csv.DictReader((tmp_path / "o" / "video_list.csv").read_text(encoding="utf-8-sig").splitlines()))
    assert {r["video_id"] for r in rows} == {"vid00000001", "vid00000002"}


def test_playlists_are_read_in_full_for_newest_n():
    # an oldest-first playlist: the newest videos are at the END
    vids = [_entry(i, 400 - i) for i in range(200)]
    f, consumed, _ = _factory({"": vids})

    class PlFactory:
        def __call__(self, **kw):
            y = f(**kw)
            real = y.extract_info

            def extract(url, download=False, process=False):
                info = real(url.replace("playlist?list=PLabcdefghijkl", "x/"), download, process)
                info["title"] = "My list"
                return info
            y.extract_info = extract
            return y
    out, label = channels.list_channel("https://www.youtube.com/playlist?list=PLabcdefghijkl",
                                       S(channel_max_videos=10), ydl_factory=PlFactory())
    assert len(consumed) == 200 and label == "playlist My list"
    assert out[0].video_id == "vid00000199" and len(out) == 10
    assert all(v.source == "playlist" for v in out)
