import datetime as dt
import json
from unittest import mock

import pytest
from conftest import FIXTURES

from yt_transcripts import search_ytdlp
from yt_transcripts.config import build_settings
from yt_transcripts.models import Video
from yt_transcripts.search import filter_and_rank, rank_newest, reject_reason, run_search
from yt_transcripts.sp_params import build_sp

NOW = dt.datetime(2026, 10, 29, 3, 40, tzinfo=dt.timezone.utc)


# ---- sp parameter: values copied from the live YouTube filter menu (2026-10-28) ----
@pytest.mark.parametrize("args,expected", [
    (("relevance", None), "CAASAhAB"),
    (("popularity", None), "CAMSAhAB"),
    (("popularity", "week"), "CAMSBAgDEAE="),
    (("relevance", "today"), "CAASBAgCEAE="),
    (("relevance", "month"), "CAASBAgEEAE="),
    (("relevance", "year"), "CAASBAgFEAE="),
])
def test_build_sp_matches_live_values(args, expected):
    assert build_sp(*args) == expected


def test_build_sp_subtitles_filter():
    # live: "Subtitles/CC" chip = CAISBBABKAE= (with sort field 2); ours uses sort 0
    assert build_sp("relevance", None, subtitles_only=True) == "CAASBBABKAE="


def test_build_sp_rejects_unknown():
    with pytest.raises(ValueError):
        build_sp("newest")
    with pytest.raises(ValueError):
        build_sp("relevance", "decade")


def test_search_url_encoding():
    url = search_ytdlp.search_url("ai agents & tools", "popularity", "week")
    assert "search_query=ai+agents+%26+tools" in url
    assert url.endswith("sp=CAMSBAgDEAE%3D")


# ---- replay a real captured search response through yt-dlp's extractor ----
@pytest.fixture
def replay_search():
    from yt_dlp.extractor.youtube._tab import YoutubeTabBaseInfoExtractor

    fixture = json.loads((FIXTURES / "search_python_week_popularity.json").read_text(encoding="utf-8"))
    seen = []

    def fake_response(self, item_id, query, **kw):
        seen.append(dict(query))
        if "continuation" in query:
            return {"onResponseReceivedCommands": [{"appendContinuationItemsAction": {"continuationItems": []}}]}
        return fixture

    with mock.patch.object(YoutubeTabBaseInfoExtractor, "_extract_response", fake_response), \
         mock.patch.object(YoutubeTabBaseInfoExtractor, "_download_ytcfg", lambda *a, **k: {}):
        yield seen


def test_real_search_response_parsed(replay_search):
    s = build_settings({"keywords": ["python tutorial"], "sorts": ["popularity"], "within": "week",
                        "cascade_windows": False})
    vids = search_ytdlp.search_keyword("python tutorial", s)
    by_id = {v.video_id: v for v in vids}
    assert len(vids) == 7  # ad slots skipped
    assert replay_search[0]["params"] == "CAMSBAgDEAE="
    v = by_id["zZgF8mvvORg"]
    assert v.views == 163_850
    assert v.duration_seconds == 10 * 3600 + 46 * 60 + 27
    assert v.channel == "Satish Dhawale"
    assert v.channel_id == "UCRDhrUdd9yoVoFFQqadR4FQ"
    assert v.published and not v.published_exact
    assert v.url == "https://www.youtube.com/watch?v=zZgF8mvvORg"
    assert by_id["4_GePr-licU"].published  # "Streamed 4d ago"
    assert by_id["Pfd916_a_cs"].published > v.published  # "15h ago" newer than "2d ago"


def test_real_search_filter_and_rank(replay_search):
    s = build_settings({"keywords": ["python tutorial"], "sorts": ["popularity"], "within": "week",
                        "min_views": 2000, "min_duration": 120})
    vids = search_ytdlp.search_keyword("python tutorial", s)
    kept, reasons = filter_and_rank(vids, s)
    assert [v.video_id for v in kept] == ["Pfd916_a_cs", "zZgF8mvvORg", "zMajAKkmxws"]
    assert reasons["below view threshold"] == 3
    assert reasons["too short"] == 1


def test_two_sorts_are_merged_not_duplicated(replay_search):
    s = build_settings({"keywords": ["python tutorial"], "sorts": ["popularity", "relevance"], "within": "week"})
    vids = search_ytdlp.search_keyword("python tutorial", s)
    assert len(vids) == 7
    # week window by popularity + relevance, plus today by popularity (cascade)
    assert {q["params"] for q in replay_search} == {"CAMSBAgDEAE=", "CAASBAgDEAE=", "CAMSBAgCEAE="}


@pytest.mark.parametrize("within,cascade,expected", [
    ("month", True, [("popularity", "month"), ("relevance", "month"), ("popularity", "week"), ("popularity", "today")]),
    ("month", False, [("popularity", "month"), ("relevance", "month")]),
    ("today", True, [("popularity", "today"), ("relevance", "today")]),
    ("any", True, [("popularity", None), ("relevance", None), ("popularity", "year"), ("popularity", "month"),
                   ("popularity", "week"), ("popularity", "today")]),
])
def test_search_plan(within, cascade, expected):
    s = build_settings({"keywords": ["x"], "within": within, "cascade_windows": cascade})
    assert search_ytdlp.search_plan(s) == expected


def test_run_search_across_keywords_merges_keywords(replay_search):
    s = build_settings({"keywords": ["python tutorial", "learn python"], "sorts": ["popularity"],
                        "within": "week", "min_views": 5000, "min_duration": 0})
    vids = run_search(s)
    assert {v.keyword for v in vids} == {"python tutorial; learn python"}


def test_real_today_search_hours_ago_ranked_newest_first():
    """Captured live 'uploaded today' search: '2h ago' labels must parse and rank newest first; live streams dropped."""
    from yt_dlp.extractor.youtube._tab import YoutubeTabBaseInfoExtractor

    fixture = json.loads((FIXTURES / "search_news_today.json").read_text(encoding="utf-8"))

    def fake_response(self, item_id, query, **kw):
        if "continuation" in query:
            return {"onResponseReceivedCommands": [{"appendContinuationItemsAction": {"continuationItems": []}}]}
        return fixture

    s = build_settings({"keywords": ["news"], "sorts": ["relevance"], "within": "today",
                        "min_views": 50_000, "min_duration": 0})
    with mock.patch.object(YoutubeTabBaseInfoExtractor, "_extract_response", fake_response), \
         mock.patch.object(YoutubeTabBaseInfoExtractor, "_download_ytcfg", lambda *a, **k: {}):
        vids = search_ytdlp.search_keyword("news", s)
    by_id = {v.video_id: v for v in vids}
    assert len(vids) == 9  # the inserted 'Top news' shelf is tolerated (yt-dlp does not expand horizontal shelves)
    for vid in ("S8iPg96AMu0", "0Wko0S-ast4", "3XqBtruTq5k", "Coa4aueiz94"):
        assert by_id[vid].published, vid
    two_h = dt.datetime.fromisoformat(by_id["S8iPg96AMu0"].published)
    sixteen_h = dt.datetime.fromisoformat(by_id["3XqBtruTq5k"].published)
    assert dt.timedelta(hours=13) <= two_h - sixteen_h <= dt.timedelta(hours=15)
    assert by_id["S8iPg96AMu0"].channel_handle == "@NBCNews"
    kept, reasons = filter_and_rank(vids, s)
    ids = [v.video_id for v in kept]
    assert ids[0] == "S8iPg96AMu0"  # 2h ago, 61K views: newest that passes 50K
    assert "ns9RC-PntuQ" not in ids  # live now
    assert "oy97Z9AyN_4" not in ids  # 3h ago but only 7.9K views
    published = [v.published for v in kept]
    assert published == sorted(published, reverse=True)


# ---- filtering rules ----
def _v(**kw):
    base = dict(video_id="abcdefghijk", title="A video", views=50_000,
                published=(NOW - dt.timedelta(days=2)).isoformat(), published_exact=True, duration_seconds=600)
    base.update(kw)
    return Video(**base)


@pytest.mark.parametrize("video,settings,reason", [
    (_v(views=None), {}, "views unknown"),
    (_v(views=9_999), {}, "below view threshold"),
    (_v(is_short=True), {}, "short"),
    (_v(live_status="is_upcoming"), {}, "live/upcoming"),
    (_v(published=(NOW - dt.timedelta(days=40)).isoformat()), {"within": "month"}, "too old"),
    (_v(published=(NOW - dt.timedelta(days=5)).isoformat()), {"max_age_days": 3}, "too old"),
    (_v(duration_seconds=30), {"min_duration": 60}, "too short"),
    (_v(duration_seconds=7200), {"max_duration": 3600}, "too long"),
    (_v(title="Reaction video"), {"exclude_words": ["reaction"]}, "title has excluded word"),
    (_v(title="Something"), {"title_must_contain": ["tutorial", "guide"]}, "title missing required word"),
    (_v(channel="Spam TV"), {"exclude_channels": ["spam tv"]}, "excluded channel"),
    (_v(channel="Other"), {"only_channels": ["Real Python", "UCabc"]}, "not one of only_channels"),
])
def test_reject_reasons(video, settings, reason):
    s = build_settings({"keywords": ["x"], "min_views": 10_000, **settings})
    assert reject_reason(video, s, NOW) == reason


def test_passes_and_approx_slack():
    s = build_settings({"keywords": ["x"], "within": "week"})
    assert reject_reason(_v(), s, NOW) is None
    # approximate "7d ago" may be up to a day older than the window - keep it
    approx = _v(published=(NOW - dt.timedelta(days=7.5)).isoformat(), published_exact=False)
    assert reject_reason(approx, s, NOW) is None
    exact = _v(published=(NOW - dt.timedelta(days=7.5)).isoformat(), published_exact=True)
    assert reject_reason(exact, s, NOW) == "too old"


def test_within_any_has_no_age_limit():
    s = build_settings({"keywords": ["x"], "within": "any"})
    assert reject_reason(_v(published="2010-01-01"), s, NOW) is None


def test_rank_newest_and_max_results():
    vids = [_v(video_id=f"id{i:09d}", published=(NOW - dt.timedelta(days=i)).isoformat()) for i in range(5)]
    vids.append(_v(video_id="nodate00000", published=""))
    ranked = rank_newest(list(reversed(vids)))
    assert ranked[0].video_id == "id000000000" and ranked[-1].video_id == "nodate00000"
    s = build_settings({"keywords": ["x"], "max_results": 2, "within": "any"})
    kept, reasons = filter_and_rank(vids, s, NOW)
    assert [v.video_id for v in kept] == ["id000000000", "id000000001"]
    assert reasons["beyond max_results"] == 4


def test_keyword_settings_override_per_keyword(replay_search):
    s = build_settings({"keywords": ["python tutorial"], "sorts": ["popularity"], "within": "week",
                        "min_views": 100_000, "min_duration": 0,
                        "keyword_settings": [{"keyword": "learn python", "min_views": 2000, "max_results": 2},
                                             {"keyword": "python tutorial", "min_views": 30_000}]})
    assert s.all_keywords() == ["python tutorial", "learn python"]
    assert s.for_keyword("Learn Python").min_views == 2000 and s.for_keyword("other") is s
    vids = run_search(s)
    by_id = {v.video_id: v for v in vids}
    # "python tutorial" (30k+): zZgF8mvvORg, zMajAKkmxws ; "learn python" (2k+, newest 2): Pfd916_a_cs, zZgF8mvvORg
    assert set(by_id) == {"zZgF8mvvORg", "zMajAKkmxws", "Pfd916_a_cs"}
    assert by_id["zZgF8mvvORg"].keyword == "python tutorial; learn python"
    assert s.validate() == []


def test_keyword_settings_alone_count_as_keywords():
    s = build_settings({"keyword_settings": [{"keyword": "solo", "min_views": 1}]})
    assert s.validate() == [] and s.all_keywords() == ["solo"]


def test_only_channels_by_name_or_id():
    s = build_settings({"keywords": ["x"], "only_channels": ["real python", "UCabc"]})
    assert reject_reason(_v(channel="Real Python"), s, NOW) is None
    assert reject_reason(_v(channel="Someone", channel_id="UCabc"), s, NOW) is None


def test_total_search_failure_is_reported_not_silent(monkeypatch):
    from yt_dlp.extractor.youtube._tab import YoutubeTabBaseInfoExtractor

    def boom(self, *a, **k):
        raise Exception("ERROR: Unable to download API page: HTTP Error 429: Too Many Requests")

    s = build_settings({"keywords": ["a", "b"], "within": "week", "cascade_windows": False})
    with mock.patch.object(YoutubeTabBaseInfoExtractor, "_extract_response", boom), \
         mock.patch.object(YoutubeTabBaseInfoExtractor, "_download_ytcfg", lambda *a, **k: {}):
        with pytest.raises(search_ytdlp.SearchFailed):
            search_ytdlp.search_keyword("a", s)
        with pytest.raises(RuntimeError, match="every YouTube search failed"):
            run_search(s)


def test_minutes_ago_labels_get_a_date():
    from yt_dlp import YoutubeDL
    from yt_dlp.extractor.youtube._base import YoutubeBaseInfoExtractor as Base

    from yt_transcripts.ytdlp_common import patch_relative_time_parsing

    patch_relative_time_parsing()
    patch_relative_time_parsing()  # idempotent
    ie = Base(YoutubeDL({"quiet": True}))
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    ts = ie._parse_time_text("30m ago")
    assert ts is not None and abs((now - ts) - 1800) < 120
    assert ie._parse_time_text("2d ago") is not None  # yt-dlp's own parsing still used
    assert ie._parse_time_text("Premiere in progress") is None


def test_handles_and_unknown_dates():
    s = build_settings({"keywords": ["x"], "only_channels": ["@RealPython"]})
    assert reject_reason(_v(channel="Real Python", channel_handle="@realpython"), s, NOW) is None
    s2 = build_settings({"keywords": ["x"], "exclude_channels": ["@spam"]})
    assert reject_reason(_v(channel="Spam", channel_handle="@spam"), s2, NOW) == "excluded channel"
    s3 = build_settings({"keywords": ["x"], "max_age_days": 3})
    assert reject_reason(_v(published=""), s3, NOW) == "upload date unknown"
    assert reject_reason(_v(published=""), build_settings({"keywords": ["x"]}), NOW) is None


def test_handle_comes_from_search_results(replay_search):
    s = build_settings({"keywords": ["python tutorial"], "sorts": ["popularity"], "within": "week",
                        "cascade_windows": False})
    vids = {v.video_id: v for v in search_ytdlp.search_keyword("python tutorial", s)}
    assert vids["x1YMNSNKUZ0"].channel_handle == "@realpython"


def test_rising_views_per_day_keeps_fast_new_videos():
    fresh = _v(views=4_000, published=(NOW - dt.timedelta(hours=3)).isoformat())  # ~8,000/day
    old_slow = _v(views=4_000, published=(NOW - dt.timedelta(days=4)).isoformat())  # 1,000/day
    s = build_settings({"keywords": ["x"], "min_views": 10_000, "rising_views_per_day": 5_000})
    assert reject_reason(fresh, s, NOW) is None
    assert reject_reason(old_slow, s, NOW) == "below view threshold"
    off = build_settings({"keywords": ["x"], "min_views": 10_000})
    assert reject_reason(fresh, off, NOW) == "below view threshold"


def test_example_config_is_valid():
    from conftest import ROOT

    from yt_transcripts.config import load_config

    s = build_settings(load_config(ROOT / "config.example.toml"))
    assert s.validate() == [] and not getattr(s, "_unknown_keys", [])


def test_reuploads_by_other_channels_are_dropped():
    from yt_transcripts.search import drop_reuploads

    orig = _v(video_id="aaaaaaaaaaa", title="ABC World News Tonight - Oct. 28, 2026", channel="ABC News",
              channel_id="UC1", views=175_000, duration_seconds=1309)
    copy = _v(video_id="bbbbbbbbbbb", title="ABC World News Tonight – Oct 28, 2026", channel="Re-uploader",
              channel_id="UC2", views=400_000, duration_seconds=1300)
    series = _v(video_id="ccccccccccc", title="ABC World News Tonight - Oct. 28, 2026", channel="ABC News",
                channel_id="UC1", views=5_000, duration_seconds=1310)  # same channel: never treated as a copy
    other_len = _v(video_id="ddddddddddd", title="ABC World News Tonight - Oct. 28, 2026", channel="X",
                   channel_id="UC3", views=1_000, duration_seconds=300)
    kept, n = drop_reuploads([orig, copy, other_len])
    assert n == 1 and [v.video_id for v in kept] == ["bbbbbbbbbbb", "ddddddddddd"]
    assert drop_reuploads([orig, series]) == ([orig, series], 0)
    s = build_settings({"keywords": ["x"], "min_views": 0, "within": "any"})
    kept, reasons = filter_and_rank([orig, copy], s, NOW)
    assert len(kept) == 1 and reasons["re-upload of another video"] == 1
    off = build_settings({"keywords": ["x"], "min_views": 0, "within": "any", "drop_reuploads": False})
    assert len(filter_and_rank([orig, copy], off, NOW)[0]) == 2


def test_rising_is_conservative_for_day_old_approximate_dates():
    # "1 day ago" (approximate) with 15,000 views: could be ~2 days old -> ~6,000/day, not 15,000+
    v = _v(views=15_000, published=(NOW - dt.timedelta(days=1)).isoformat(), published_exact=False)
    s = build_settings({"keywords": ["x"], "min_views": 50_000, "rising_views_per_day": 10_000})
    assert reject_reason(v, s, NOW) == "below view threshold"
    v.published_exact = True  # exact: really 15,000/day
    assert reject_reason(v, s, NOW) is None


def test_generic_titles_are_never_treated_as_reuploads():
    from yt_transcripts.search import drop_reuploads

    a = _v(video_id="aaaaaaaaaaa", title="#shorts", channel="A", channel_id="UC1", duration_seconds=30)
    b = _v(video_id="bbbbbbbbbbb", title="#Shorts", channel="B", channel_id="UC2", duration_seconds=31)
    c = _v(video_id="ccccccccccc", title="Untitled", channel="C", channel_id="UC3", duration_seconds=30)
    assert drop_reuploads([a, b, c])[1] == 0


def test_cross_keyword_reupload_keeps_both_keywords():
    from yt_transcripts.search import drop_reuploads

    a = _v(video_id="aaaaaaaaaaa", title="Same long video title", channel="A", channel_id="UC1",
           views=900, duration_seconds=600, keyword="alpha")
    b = _v(video_id="bbbbbbbbbbb", title="Same long video title", channel="B", channel_id="UC2",
           views=100, duration_seconds=601, keyword="beta")
    kept, n = drop_reuploads([a, b])
    assert n == 1 and kept[0].keyword == "alpha; beta"
    kept, n = drop_reuploads([a, b], eligible=lambda v: False)
    assert n == 0


def test_commented_example_settings_are_valid_when_uncommented(tmp_path):
    import re
    from dataclasses import fields

    from conftest import ROOT

    from yt_transcripts.config import Settings, load_config

    names = {f.name for f in fields(Settings)} | {"keywords_file"}
    lines = []
    for line in (ROOT / "config.example.toml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"#\s*(\w+)\s*=", line)
        if m and m.group(1) in names and m.group(1) != "keywords_file":
            line = line.lstrip("# ")
            key = m.group(1)
            lines = [ln for ln in lines if not re.match(rf"{key}\s*=", ln)]  # replace the active value
        lines.append(line)
    cfg = tmp_path / "c.toml"
    cfg.write_text("\n".join(lines), encoding="utf-8")
    s = build_settings(load_config(cfg))
    assert s.validate() == [] and not getattr(s, "_unknown_keys", [])


def test_missing_view_counts_are_looked_up(monkeypatch):
    from yt_transcripts import search as search_mod
    from yt_transcripts import search_ytdlp as sy

    raw = [_v(video_id=f"{i:011d}", views=None) for i in range(6)]
    monkeypatch.setattr(sy, "search_keyword", lambda *a, **k: [Video(**{**v.__dict__}) for v in raw])
    looked = []

    def fake_enrich(videos, settings, factory=None):
        for v in videos:
            looked.append(v.video_id)
            v.views = 50_000

    monkeypatch.setattr(sy, "enrich_exact", fake_enrich)
    s = build_settings({"keywords": ["x"], "within": "any", "min_views": 10_000})
    vids = search_mod.run_search(s)
    assert len(looked) == 6 and len(vids) == 6


def test_odd_search_entries_are_tolerated():
    v = search_ytdlp.entry_to_video({"id": "abcdefghijk", "timestamp": 10**20, "duration": "12.5", "view_count": "x",
                                     "title": 5, "upload_date": "bad"}, "kw")
    assert v.video_id == "abcdefghijk" and v.published == "" and v.duration_seconds == 12 and v.title == "5"
    assert search_ytdlp.entry_to_video({"id": ["x"]}, "kw") is None
