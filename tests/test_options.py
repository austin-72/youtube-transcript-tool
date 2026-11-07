"""Smaller options: filler words, min transcript length, file names, month folders, list order, view and
date ranges, and their validation."""

import datetime as dt

import pytest

from yt_transcripts import search
from yt_transcripts import transcripts as tr
from yt_transcripts.config import build_settings
from yt_transcripts.models import Segment, Transcript, Video
from yt_transcripts.writers import transcript_basename, transcript_folder


def S(**kw):
    return build_settings({"keywords": ["x"], **kw})


def test_filler_words_go_but_real_words_stay():
    t = Transcript("x", "en", segments=[Segment(0, 1, "Um, so uh I think, erm, the umbrella hums."),
                                        Segment(1, 1, "uh"), Segment(2, 1, "Hmm. okay"),
                                        Segment(3, 1, "Use a 5 mm drill at the UM campus")])
    tr.remove_filler_words(t)
    assert [s.text for s in t.segments] == ["So I think, the umbrella hums.", "Okay",
                                           "Use a 5 mm drill at the UM campus"]


def test_min_transcript_words_and_filler_through_the_pipeline(tmp_path, monkeypatch):
    from yt_transcripts import pipeline

    class F:
        name, last_info = "ytdlp", None

        def fetch(self, v):
            words = 3 if v.video_id.endswith("1") else 50
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp",
                              [Segment(0, 1, "um " + " ".join(["word"] * words))])
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [F()])
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt"],
                        "min_transcript_words": 10, "remove_filler_words": True})
    vids = [Video(f"vid0000000{i}", title=f"T{i}", keyword="k") for i in (1, 2)]
    stats = pipeline.download_all(vids, s)
    assert stats["ok"] == 1 and stats["no_transcript"] == 1
    assert vids[0].transcript_status == "no_transcript"
    txt = next((tmp_path / "transcripts" / "k").glob("*.txt")).read_text(encoding="utf-8")
    assert "um " not in txt and "word word" in txt


def test_file_name_template():
    v = Video("abcdefghijk", title="My: Title?", channel="Chan", published="2026-10-27T10:00:00Z", views=1234,
              keyword="ai agents; x")
    assert transcript_basename(v) == "2026-10-27 - Chan - My Title [abcdefghijk]"
    assert transcript_basename(v, template="{title}") == "My Title [abcdefghijk]"
    assert transcript_basename(v, template="{keyword}/{views} {title} ({id})") == "ai agents 1234 My Title (abcdefghijk)"
    long = Video("abcdefghijk", title="T" * 300, channel="C" * 80, published="2026-10-27")
    for n in (45, 60, 120):
        name = transcript_basename(long, n)
        assert len(name) <= n and name.endswith("[abcdefghijk]")


def test_month_folders(tmp_path):
    v = Video("abcdefghijk", published="2026-10-27T10:00:00Z")
    assert transcript_folder(tmp_path, v, "month") == tmp_path / "2026-10"
    assert transcript_folder(tmp_path, Video("abcdefghijk"), "month") == tmp_path / "unknown month"


def test_list_sort():
    vids = [Video("a" * 11, views=10, published="2026-10-27"), Video("b" * 11, views=500, published="2026-01-01"),
            Video("c" * 11, views=100, published="2026-10-28")]
    assert [v.video_id[0] for v in search.sort_for_list(vids, "newest")] == ["c", "a", "b"]
    assert [v.video_id[0] for v in search.sort_for_list(vids, "views")] == ["b", "c", "a"]
    assert search.sort_for_list(vids, "views_per_day")[0].video_id[0] == "c"


def test_max_views_and_date_range():
    now = dt.datetime(2026, 11, 4, 12, tzinfo=dt.timezone.utc)
    s = S(min_views=0, within="any", max_views=1000, published_after="2026-10-01", published_before="2026-10-31")
    ok = Video("a" * 11, views=500, published="2026-10-15", published_exact=True)
    assert search.reject_reason(ok, s, now) is None
    assert search.reject_reason(Video("a" * 11, views=5000, published="2026-10-15"), s, now) == "above max_views"
    assert search.reject_reason(Video("a" * 11, views=5, published="2026-09-20", published_exact=True), s, now) \
        == "before published_after"
    assert search.reject_reason(Video("a" * 11, views=5, published="2026-11-02", published_exact=True), s, now) \
        == "after published_before"
    # an approximate date a day off still counts
    assert search.reject_reason(Video("a" * 11, views=5, published="2026-09-30"), s, now) is None
    assert search.reject_reason(Video("a" * 11, views=5), s, now) == "upload date unknown"


@pytest.mark.parametrize("kw,needle", [
    ({"published_after": "last week"}, "published_after"),
    ({"max_views": 5, "min_views": 10}, "max_views"),
    ({"channel_tabs": ["videos", "clips"]}, "channel_tabs"),
    ({"organize_by": "year"}, "organize_by"),
    ({"file_name": "{date} {nope}"}, "file_name"),
    ({"data_saver": "turbo"}, "data_saver"),
    ({"proxy_limit_run_mb": -1}, "proxy_limit"),
    ({"list_sort": "random"}, "list_sort"),
])
def test_validation(kw, needle):
    assert any(needle in p for p in S(**kw).validate())


def test_defaults_are_valid_and_dates_parse_in_several_forms():
    from yt_transcripts.config import parse_day

    assert S().validate() == []
    assert parse_day("2026/10/01") == parse_day("20261001") == dt.date(2026, 10, 1)
    assert S(keywords=[], channels=["@x"]).validate() == []


def test_json_keeps_the_original_text_when_cleaning(tmp_path, monkeypatch):
    import json

    from yt_transcripts import pipeline

    class F:
        name, last_info = "ytdlp", None

        def fetch(self, v):
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp",
                              [Segment(0, 1, "[Music] um hello there"), Segment(1, 1, "and more words here")])
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [F()])
    base = {"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt", "json"]}
    s = build_settings({**base, "strip_sound_tags": True, "remove_filler_words": True})
    pipeline.download_all([Video("vid00000001", title="T", keyword="k")], s)
    folder = tmp_path / "transcripts" / "k"
    js = json.loads(next(folder.glob("*.json")).read_text(encoding="utf-8"))
    assert js["transcript"]["segments"][0]["text"] == "[Music] um hello there"
    assert "[Music]" not in next(folder.glob("*.txt")).read_text(encoding="utf-8")
    # cleaning switched off later: the files are rebuilt with the original text back
    s2 = build_settings(base)
    pipeline.download_all([Video("vid00000001", title="T", keyword="k")], s2)
    assert "[Music] um hello there" in next(folder.glob("*.txt")).read_text(encoding="utf-8")


def test_schedule_command_for_exe_and_scripts(tmp_path):
    from pathlib import Path

    from yt_transcripts import cli

    exe = r"C:\Tools\YT's\YouTubeTranscriptTool.exe"
    cmd = cli.schedule_command("7:05", True, Path(r"C:\Tools\YT's"), exe)
    ps = cmd[-1]
    assert cmd[0] == "powershell" and "-Execute '\"C:\\Tools\\YT''s\\YouTubeTranscriptTool.exe\"' -Argument 'run'" in ps
    curly = cli.schedule_command("08:00", True, Path("C:/x"), "C:\\Bob\u2019s tools\\a.exe")[-1]
    assert "Bob\u2019\u2019s" in curly
    assert "-At '07:05'" in ps and "StartWhenAvailable" in ps
    assert "run_scheduled.bat" in cli.schedule_command("23:59", False, tmp_path, "python")[-1]
    assert cli.schedule_command("25:00", True, tmp_path, exe) is None
    assert cli.schedule_command("noon", True, tmp_path, exe) is None
    assert "Unregister-ScheduledTask" in cli.schedule_command(None, True, tmp_path, exe)[-1]
    calls = []
    assert cli.cmd_schedule("08:00", runner=lambda c: calls.append(c) or 0) == 0 and calls


def test_description_and_chapter_flags_reach_the_settings(tmp_path):
    from yt_transcripts import cli

    cfg = tmp_path / "c.toml"
    cfg.write_text("", encoding="utf-8")
    s = cli.settings_from_args(cli.build_parser().parse_args(["run", "-c", str(cfg), "--description", "--chapters",
                                                              "--timestamps"]))
    assert (s.include_description, s.chapters, s.timestamps) == (True, True, True)
    s = cli.settings_from_args(cli.build_parser().parse_args(["run", "-c", str(cfg)]))
    assert (s.include_description, s.chapters, s.timestamps) == (False, False, False)
