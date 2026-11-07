import datetime as dt
import json

import pytest

from yt_transcripts import pipeline
from yt_transcripts import transcripts as tr
from yt_transcripts.config import build_settings
from yt_transcripts.models import Segment, Transcript, Video
from yt_transcripts.writers import read_video_list, write_video_list


class ScriptedFetcher:
    """Returns pre-programmed outcomes per video id, in order."""

    def __init__(self, name, script):
        self.name, self.script, self.calls = name, script, []

    def fetch(self, video):
        self.calls.append(video.video_id)
        outcomes = self.script.get(video.video_id, [tr.FetchError(tr.NO_TRANSCRIPT, "none")])
        out = outcomes.pop(0) if len(outcomes) > 1 else outcomes[0]
        if isinstance(out, Exception):
            raise out
        return out


def _t(vid, lang="en"):
    segs = [Segment(i * 10.0, 10.0, f"Sentence number {i}.") for i in range(12)]
    return Transcript(video_id=vid, language=lang, language_name="English", kind="auto", method="fake", segments=segs)


def _videos():
    return [
        Video(video_id="aaaaaaaaaaa", title="First: video?", channel="Chan/One", views=50_000,
              published="2026-10-27T00:00:00+00:00", keyword="ai agents"),
        Video(video_id="bbbbbbbbbbb", title="Second", channel="Chan", views=20_000, published="2026-10-26", keyword="ai agents"),
        Video(video_id="ccccccccccc", title="Third", channel="Chan", views=20_000, published="2026-10-25", keyword="other"),
    ]


@pytest.fixture
def settings(tmp_path):
    return build_settings({"keywords": ["x"], "output_dir": str(tmp_path / "out"), "delay_seconds": 0,
                           "formats": ["txt", "json", "srt", "md", "vtt"]})


def _install(monkeypatch, *fetchers):
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: list(fetchers))


def test_download_all_writes_files_and_manifest(settings, monkeypatch, tmp_path):
    api = ScriptedFetcher("api", {
        "aaaaaaaaaaa": [_t("aaaaaaaaaaa")],
        "bbbbbbbbbbb": [tr.FetchError(tr.ERROR, "PO token")],
        "ccccccccccc": [tr.FetchError(tr.NO_TRANSCRIPT, "disabled")],
    })
    ytdlp = ScriptedFetcher("ytdlp", {
        "bbbbbbbbbbb": [_t("bbbbbbbbbbb")],
        "ccccccccccc": [tr.FetchError(tr.NO_TRANSCRIPT, "video has no captions")],
    })
    _install(monkeypatch, api, ytdlp)
    vids = _videos()
    stats = pipeline.download_all(vids, settings, sleep=lambda s: None)
    assert stats["ok"] == 2 and stats[tr.NO_TRANSCRIPT] == 1
    assert ytdlp.calls == ["bbbbbbbbbbb", "ccccccccccc"]  # fallback only when needed

    root = tmp_path / "out"
    folder = root / "transcripts" / "ai agents"
    files = sorted(p.name for p in folder.iterdir())
    assert "2026-10-27 - Chan One - First video [aaaaaaaaaaa].txt" in files
    assert len([f for f in files if f.startswith("2026-10-27")]) == 5  # txt json srt md vtt
    txt = (folder / "2026-10-27 - Chan One - First video [aaaaaaaaaaa].txt").read_text(encoding="utf-8")
    assert "Title: First: video?" in txt and "Views: 50,000" in txt and "Sentence number 11." in txt
    data = json.loads((folder / "2026-10-27 - Chan One - First video [aaaaaaaaaaa].json").read_text(encoding="utf-8"))
    assert len(data["transcript"]["segments"]) == 12
    srt = (folder / "2026-10-27 - Chan One - First video [aaaaaaaaaaa].srt").read_text(encoding="utf-8")
    assert srt.startswith("1\n00:00:00,000 --> 00:00:10,000\nSentence number 0.")

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["aaaaaaaaaaa"]["status"] == "ok"
    assert manifest["bbbbbbbbbbb"]["method"] == "ytdlp"
    assert manifest["ccccccccccc"]["status"] == tr.NO_TRANSCRIPT
    assert "video has no captions" in manifest["ccccccccccc"]["error"]
    assert vids[0].transcript_status == "ok" and vids[0].transcript_file.endswith(".txt")
    combined = list((root / "combined").glob("*.md"))
    assert len(combined) == 1 and "Sentence number 5." in combined[0].read_text(encoding="utf-8")


def test_rerun_skips_done_and_permanent_failures(settings, monkeypatch):
    f = ScriptedFetcher("api", {"aaaaaaaaaaa": [_t("aaaaaaaaaaa")], "bbbbbbbbbbb": [_t("bbbbbbbbbbb")]})
    _install(monkeypatch, f)
    pipeline.download_all(_videos(), settings, sleep=lambda s: None)
    f2 = ScriptedFetcher("api", {})
    _install(monkeypatch, f2)
    stats = pipeline.download_all(_videos(), settings, sleep=lambda s: None)
    assert f2.calls == [] and stats["skipped"] == 3
    settings.retry_failed = True
    f3 = ScriptedFetcher("api", {"ccccccccccc": [_t("ccccccccccc")]})
    _install(monkeypatch, f3)
    stats = pipeline.download_all(_videos(), settings, sleep=lambda s: None)
    assert f3.calls == ["ccccccccccc"] and stats["ok"] == 1


def test_new_format_requested_redownloads(settings, monkeypatch):
    settings.formats = ["txt"]
    _install(monkeypatch, ScriptedFetcher("api", {v.video_id: [_t(v.video_id)] for v in _videos()}))
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    settings.formats = ["txt", "srt"]
    f = ScriptedFetcher("api", {"aaaaaaaaaaa": [_t("aaaaaaaaaaa")]})
    _install(monkeypatch, f)
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    assert f.calls == ["aaaaaaaaaaa"]


def test_blocked_backs_off_then_recovers(settings, monkeypatch):
    blocked = tr.FetchError(tr.BLOCKED, "429")
    f = ScriptedFetcher("api", {"aaaaaaaaaaa": [blocked, blocked, _t("aaaaaaaaaaa")]})
    _install(monkeypatch, f)
    sleeps = []
    stats = pipeline.download_all(_videos()[:1], settings, sleep=sleeps.append)
    assert stats["ok"] == 1
    assert sleeps == pipeline.BACKOFF_SECONDS[:2]


def test_persistent_block_stops_cleanly(settings, monkeypatch):
    blocked = tr.FetchError(tr.BLOCKED, "bot check")
    f = ScriptedFetcher("api", {v.video_id: [blocked] for v in _videos()})
    _install(monkeypatch, f)
    stats = pipeline.download_all(_videos(), settings, sleep=lambda s: None)
    assert stats["stopped_blocked"] == 1
    assert f.calls == ["aaaaaaaaaaa"] * settings.max_consecutive_blocks


def test_unavailable_from_ytdlp_does_not_try_next_method(settings, monkeypatch):
    a = ScriptedFetcher("ytdlp", {"aaaaaaaaaaa": [tr.FetchError(tr.UNAVAILABLE, "private")]})
    b = ScriptedFetcher("api", {})
    _install(monkeypatch, a, b)
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    assert b.calls == []


def test_unavailable_from_the_other_library_still_lets_ytdlp_try(settings, monkeypatch):
    # youtube-transcript-api also says "unavailable" when the IP is blocked - yt-dlp decides
    a = ScriptedFetcher("api", {"aaaaaaaaaaa": [tr.FetchError(tr.UNAVAILABLE, "video is unavailable")]})
    b = ScriptedFetcher("ytdlp", {"aaaaaaaaaaa": [_t("aaaaaaaaaaa")]})
    _install(monkeypatch, a, b)
    stats = pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    assert b.calls == ["aaaaaaaaaaa"] and stats["ok"] == 1


def test_po_token_wall_is_retried_on_a_schedule(settings, monkeypatch):
    wall = tr.FetchError(tr.PO_TOKEN, "YouTube wants a PO token")
    _install(monkeypatch, ScriptedFetcher("ytdlp", {"aaaaaaaaaaa": [wall]}),
             ScriptedFetcher("api", {"aaaaaaaaaaa": [tr.FetchError(tr.PO_TOKEN, "needs a PO token")]}))
    stats = pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    assert stats["po_token"] == 1
    rec = json.loads((pipeline.Path(settings.output_dir) / "manifest.json").read_text(encoding="utf-8"))["aaaaaaaaaaa"]
    assert rec["status"] == "po_token" and rec["next_retry"]
    assert pipeline.should_skip(rec, settings).startswith("needs a YouTube token")  # not again today
    later = pipeline.parse_retry_time(rec["next_retry"]) + dt.timedelta(minutes=1)
    assert pipeline.should_skip(rec, settings, now=later) is None  # due again
    assert pipeline.next_retry_time(9, now=later) == (later + dt.timedelta(hours=168)).isoformat(timespec="seconds")


def test_network_error_from_ytdlp_is_not_mistaken_for_a_token_wall(settings, monkeypatch):
    _install(monkeypatch, ScriptedFetcher("ytdlp", {"aaaaaaaaaaa": [tr.FetchError(tr.ERROR, "no connection")]}),
             ScriptedFetcher("api", {"aaaaaaaaaaa": [tr.FetchError(tr.PO_TOKEN, "needs a PO token")]}))
    assert pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)["po_token"] == 0


def test_organize_by_channel_and_flat(settings, monkeypatch, tmp_path):
    settings.formats = ["txt"]
    for mode, expected in (("channel", "Chan One"), ("flat", None)):
        settings.organize_by = mode
        settings.output_dir = str(tmp_path / mode)
        _install(monkeypatch, ScriptedFetcher("api", {"aaaaaaaaaaa": [_t("aaaaaaaaaaa")]}))
        pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
        base = tmp_path / mode / "transcripts"
        target = base / expected if expected else base
        assert any(p.suffix == ".txt" for p in target.iterdir())


def test_video_list_roundtrip(tmp_path):
    vids = _videos()
    vids[0].duration_seconds = 3725
    paths = write_video_list(vids, tmp_path)
    for p in (paths["csv"], paths["json"]):
        back = read_video_list(p)
        assert [v.video_id for v in back] == [v.video_id for v in vids]
        assert back[0].views == 50_000 and back[0].title == "First: video?"
        assert back[0].duration_seconds == 3725 and back[0].published == vids[0].published
    assert paths["csv"].read_bytes().startswith(b"\xef\xbb\xbf")  # Excel-friendly BOM


def test_read_plain_url_list(tmp_path):
    p = tmp_path / "urls.txt"
    p.write_text("# my list\nhttps://www.youtube.com/watch?v=zZgF8mvvORg&t=3s\nhttps://youtu.be/Pfd916_a_cs\n"
                 "https://www.youtube.com/shorts/x1YMNSNKUZ0\nrnati8sE0Js\nnot a url\n", encoding="utf-8")
    assert [v.video_id for v in read_video_list(p)] == ["zZgF8mvvORg", "Pfd916_a_cs", "x1YMNSNKUZ0", "rnati8sE0Js"]


def test_filenames_fit_windows_path_limit(tmp_path):
    from yt_transcripts.writers import MAX_PATH, transcript_basename, write_transcript

    deep = tmp_path / ("d" * 40) / ("e" * 40)
    v = Video(video_id="aaaaaaaaaaa", title="T" * 200, channel="C" * 100, published="2026-10-27")
    files = write_transcript(v, _t("aaaaaaaaaaa"), deep, ["txt", "json"])
    for p in files.values():
        assert len(str(p.resolve())) <= MAX_PATH
        assert p.name.endswith("[aaaaaaaaaaa]" + p.suffix) and p.name.startswith("2026-10-27 - C")
    very_deep = tmp_path / ("x" * 90) / ("y" * 90)
    files = write_transcript(v, _t("aaaaaaaaaaa"), very_deep, ["txt"])
    assert files["txt"].name == "aaaaaaaaaaa.txt"
    short = transcript_basename(Video(video_id="aaaaaaaaaaa", title="Hi", channel="Me", published="2026-01-02"))
    assert short == "2026-01-02 - Me - Hi [aaaaaaaaaaa]"


def test_mark_new_across_runs(tmp_path):
    from yt_transcripts.writers import mark_new

    first = _videos()[:2]
    assert mark_new(first, tmp_path) == 0 and not any(v.is_new for v in first)  # first run: baseline
    second = _videos()
    assert mark_new(second, tmp_path) == 1
    assert [v.is_new for v in second] == [False, False, True]
    assert second[0].first_seen == first[0].first_seen


def test_failing_first_method_is_dropped_after_three_misses(settings, monkeypatch):
    vids = [Video(video_id=f"v{i:010d}", title=f"T{i}", views=50_000, published="2026-10-27", keyword="k")
            for i in range(6)]
    po = tr.FetchError(tr.ERROR, "needs a PO token")
    api = ScriptedFetcher("api", {v.video_id: [po] for v in vids})
    ytdlp = ScriptedFetcher("ytdlp", {v.video_id: [_t(v.video_id)] for v in vids})
    _install(monkeypatch, api, ytdlp)
    settings.formats = ["txt"]
    stats = pipeline.download_all(vids, settings, sleep=lambda s: None)
    assert stats["ok"] == 6
    assert len(api.calls) == 3 and len(ytdlp.calls) == 6


def test_breaker_ignores_videos_where_nothing_worked(settings, monkeypatch):
    vids = [Video(video_id=f"v{i:010d}", title=f"T{i}", views=50_000, published="2026-10-27", keyword="k")
            for i in range(5)]
    none = tr.FetchError(tr.NO_TRANSCRIPT, "no captions")
    api = ScriptedFetcher("api", {v.video_id: [none] for v in vids})
    ytdlp = ScriptedFetcher("ytdlp", {v.video_id: [none] for v in vids})
    _install(monkeypatch, api, ytdlp)
    pipeline.download_all(vids, settings, sleep=lambda s: None)
    assert len(api.calls) == 5


def test_header_language_name_not_doubled():
    from yt_transcripts.writers import render_txt

    t = _t("aaaaaaaaaaa")
    t.language_name = "English (auto-generated)"
    assert "Transcript: English (auto-generated), via fake" in render_txt(_videos()[0], t)


def test_no_captions_on_fresh_video_is_retried_later():
    from yt_transcripts.pipeline import should_skip

    now = dt.datetime(2026, 10, 29, tzinfo=dt.timezone.utc)
    s = build_settings({"keywords": ["x"]})
    fresh = {"status": "no_transcript", "published": "2026-10-28T20:00:00+00:00"}
    old = {"status": "no_transcript", "published": "2026-10-01"}
    unknown = {"status": "no_transcript"}
    assert should_skip(fresh, s, now) is None
    assert should_skip(old, s, now) == "skipped earlier: no_transcript"
    assert should_skip(unknown, s, now) == "skipped earlier: no_transcript"
    assert should_skip({"status": "unavailable", "published": "2026-10-28"}, s, now).startswith("skipped")


def test_max_transcripts_per_run(settings, monkeypatch):
    settings.max_transcripts_per_run = 2
    f = ScriptedFetcher("api", {v.video_id: [_t(v.video_id)] for v in _videos()})
    _install(monkeypatch, f)
    stats = pipeline.download_all(_videos(), settings, sleep=lambda s: None)
    assert stats["ok"] == 2 and stats["left_for_next_run"] == 1
    stats = pipeline.download_all(_videos(), settings, sleep=lambda s: None)
    assert stats["ok"] == 1 and stats["skipped"] == 2


def test_moving_the_output_folder_keeps_finished_work(settings, monkeypatch, tmp_path):
    import shutil

    settings.formats = ["txt"]
    _install(monkeypatch, ScriptedFetcher("api", {"aaaaaaaaaaa": [_t("aaaaaaaaaaa")]}))
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    moved = tmp_path / "moved"
    shutil.move(settings.output_dir, moved)
    settings.output_dir = str(moved)
    f = ScriptedFetcher("api", {})
    _install(monkeypatch, f)
    vids = _videos()[:1]
    stats = pipeline.download_all(vids, settings, sleep=lambda s: None)
    assert stats["skipped"] == 1 and f.calls == []
    assert vids[0].transcript_file.startswith(str(moved))


def test_count_mentions():
    from yt_transcripts.pipeline import count_mentions

    text = "AI agents are great. ai   agents again! Not agentsy. Claude Code rocks; claude code. Code code."
    assert count_mentions(text, "ai agents") == 2
    assert count_mentions(text, "claude code tutorial") == 2  # 'tutorial' ignored; claude=2, code=4
    assert count_mentions(text, "ai agents; claude code") == 4
    assert count_mentions(text, "how to") == 0 and count_mentions(text, "") == 0
    assert count_mentions("I love C++ and c# too", "c++ tutorial") == 1


def test_videos_without_metadata_try_ytdlp_first(settings, monkeypatch):
    api = ScriptedFetcher("api", {"zZgF8mvvORg": [_t("zZgF8mvvORg")]})
    ytdlp = ScriptedFetcher("ytdlp", {"zZgF8mvvORg": [_t("zZgF8mvvORg")]})
    _install(monkeypatch, api, ytdlp)
    pipeline.download_all([Video(video_id="zZgF8mvvORg")], settings, sleep=lambda s: None)
    assert ytdlp.calls == ["zZgF8mvvORg"] and api.calls == []


def test_list_open_in_excel_saves_a_copy(tmp_path, monkeypatch):
    import os

    from yt_transcripts import writers

    real_replace = os.replace

    def locked(src, dst):
        if str(dst).endswith("video_list.csv"):
            raise PermissionError(13, "The process cannot access the file because it is being used")
        return real_replace(src, dst)

    monkeypatch.setattr(writers.os, "replace", locked)
    paths = write_video_list([Video(video_id="abcdefghijk", title="T", views=5)], tmp_path)
    assert paths["csv"].name == "video_list (new).csv" and paths["csv"].exists()
    assert paths["json"].name == "video_list.json"
    assert not list(tmp_path.glob("*.tmp"))


def test_empty_formats_rejected():
    assert any("formats" in p for p in build_settings({"keywords": ["x"], "formats": []}).validate())


def test_many_errors_in_a_row_stop_the_run(settings, monkeypatch):
    vids = [Video(video_id=f"{i:011d}", title=f"V{i}", views=50_000, keyword="x") for i in range(10)]
    err = tr.FetchError(tr.ERROR, "ConnectionError: no internet")
    f = ScriptedFetcher("api", {v.video_id: [err] for v in vids})
    _install(monkeypatch, f)
    stats = pipeline.download_all(vids, settings, sleep=lambda s: None)
    assert stats["stopped_errors"] == 1
    assert len(f.calls) == pipeline.MAX_CONSECUTIVE_ERRORS
    # nothing was marked permanent, so the next run tries them again
    m = json.loads((pipeline.Path(settings.output_dir) / "manifest.json").read_text(encoding="utf-8"))
    assert {r["status"] for r in m.values()} == {tr.ERROR}


def test_po_token_errors_do_not_stop_the_run(settings, monkeypatch):
    vids = [Video(video_id=f"{i:011d}", title=f"V{i}", views=50_000, keyword="x") for i in range(9)]
    err = tr.FetchError(tr.ERROR, "this caption track needs a PO token")
    f = ScriptedFetcher("api", {v.video_id: [err] for v in vids})
    _install(monkeypatch, f)
    stats = pipeline.download_all(vids, settings, sleep=lambda s: None)
    assert stats["stopped_errors"] == 0 and len(f.calls) == 9


@pytest.mark.parametrize("fmt", ["txt", "json", "md", "srt", "vtt"])
def test_transcript_preview_in_every_format(tmp_path, fmt):
    from yt_transcripts.report import render_html, transcript_preview
    from yt_transcripts.writers import write_transcript

    v = _videos()[0]
    files = write_transcript(v, _t(v.video_id), tmp_path, [fmt], True, 30)
    text = transcript_preview(str(files[fmt]))
    assert text.startswith("Sentence number 0. Sentence number 1.") and "-->" not in text and "[00:" not in text
    v.transcript_file, v.transcript_status = str(files[fmt]), "ok"
    assert "<details" in render_html([v], tmp_path)


@pytest.mark.parametrize("enc,sep", [("cp1252", ","), ("utf-8-sig", ";"), ("utf-16", "\t"), ("utf-8", ",")])
def test_read_list_saved_by_excel(tmp_path, enc, sep):
    p = tmp_path / "list.csv"
    p.write_bytes(f"title{sep}url\r\nCafé tips{sep}https://youtu.be/aaaaaaaaaaa\r\nB{sep}https://www.youtube.com/watch?v=bbbbbbbbbbb\r\n"
                  .encode(enc))
    vids = read_video_list(p)
    assert [v.video_id for v in vids] == ["aaaaaaaaaaa", "bbbbbbbbbbb"] and vids[0].title == "Café tips"


def test_stop_interrupts_rate_limit_wait(settings, monkeypatch):
    import time

    blocked = tr.FetchError(tr.BLOCKED, "429")
    f = ScriptedFetcher("api", {v.video_id: [blocked] for v in _videos()})
    _install(monkeypatch, f)
    calls = []

    def should_stop():
        calls.append(1)
        return len(calls) >= 2  # Stop pressed right after the first block

    t0 = time.monotonic()
    stats = pipeline.download_all(_videos(), settings, should_stop=should_stop)  # real sleep function
    assert time.monotonic() - t0 < 5 and stats["interrupted"] == 1


def test_new_format_is_built_from_saved_json_without_refetching(settings, monkeypatch):
    settings.formats = ["txt", "json"]
    _install(monkeypatch, ScriptedFetcher("api", {v.video_id: [_t(v.video_id)] for v in _videos()}))
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    settings.formats = ["txt", "json", "srt"]
    f = ScriptedFetcher("api", {})
    _install(monkeypatch, f)
    stats = pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    assert f.calls == [] and stats["skipped"] == 1
    m = json.loads((pipeline.Path(settings.output_dir) / "manifest.json").read_text(encoding="utf-8"))
    files = m["aaaaaaaaaaa"]["files"]
    assert set(files) == {"txt", "json", "srt"}
    srt = (pipeline.Path(settings.output_dir) / files["srt"]).read_text(encoding="utf-8")
    assert "Sentence number 0." in srt and "-->" in srt
    # third run: everything is there, nothing to do
    assert pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)["skipped"] == 1 and f.calls == []


def test_list_roundtrip_with_quotes_and_odd_characters(tmp_path):
    vids = [Video(video_id="aaaaaaaaaaa", title='He said "hi"; then, left', views=5),
            Video(video_id="bbbbbbbbbbb", title="Line sep\x85and form\x0cfeed", views=6),
            Video(video_id="ccccccccccc", title="plain", views=7)]
    paths = write_video_list(vids, tmp_path)
    back = read_video_list(paths["csv"])
    assert [v.video_id for v in back] == ["aaaaaaaaaaa", "bbbbbbbbbbb", "ccccccccccc"]
    assert back[0].title == 'He said "hi"; then, left'
    short = tmp_path / "short.csv"
    short.write_text("title,url\nonly a title\n", encoding="utf-8")
    assert read_video_list(short) == []  # no crash on a short row


def test_added_format_matches_existing_files_even_for_bare_links(settings, monkeypatch):
    settings.formats = ["txt", "json"]
    _install(monkeypatch, ScriptedFetcher("api", {v.video_id: [_t(v.video_id)] for v in _videos()}))
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    out = pipeline.Path(settings.output_dir)
    m1 = json.loads((out / "manifest.json").read_text(encoding="utf-8"))["aaaaaaaaaaa"]["files"]
    settings.formats = ["txt", "json", "md"]
    settings.organize_by = "flat"  # changing the layout must not duplicate anything
    _install(monkeypatch, ScriptedFetcher("api", {}))
    bare = Video(video_id="aaaaaaaaaaa", source="list-file", keyword="single videos")
    pipeline.download_all([bare], settings, sleep=lambda s: None)
    m2 = json.loads((out / "manifest.json").read_text(encoding="utf-8"))["aaaaaaaaaaa"]["files"]
    assert m2["txt"] == m1["txt"] and m2["json"] == m1["json"]
    assert pipeline.Path(m2["md"]).parent == pipeline.Path(m1["json"]).parent
    assert pipeline.Path(m2["md"]).stem == pipeline.Path(m1["json"]).stem
    md = (out / m2["md"]).read_text(encoding="utf-8")
    assert "First: video?" in md  # title restored from the saved .json, not "unknown"
    assert len(list(out.rglob("*.txt"))) == 1


def test_csv_with_other_headers_or_excel_mangled_ids(tmp_path):
    p = tmp_path / "a.csv"
    p.write_text("Title,URL,Video_ID\nA,https://youtu.be/-aaaaaaaaaa,#NAME?\n", encoding="utf-8")
    assert [v.video_id for v in read_video_list(p)] == ["-aaaaaaaaaa"]
    p.write_text("My picks\nwatch this https://www.youtube.com/watch?v=bbbbbbbbbbb, and https://youtu.be/ccccccccccc\n",
                 encoding="utf-8")
    assert [v.video_id for v in read_video_list(p)] == ["bbbbbbbbbbb", "ccccccccccc"]


def test_eta_ignores_videos_that_only_need_a_new_format(settings, monkeypatch, caplog):
    import logging

    ids = [f"v{n:010d}" for n in range(60)]
    mk = lambda sel: [Video(video_id=i, title=i, channel="c", published="2026-10-01", keyword="k") for i in sel]  # noqa: E731
    _install(monkeypatch, ScriptedFetcher("api", {i: [_t(i)] for i in ids}))
    settings.formats = ["txt", "json"]
    pipeline.download_all(mk(ids[10:40]), settings, sleep=lambda s: None)
    settings.formats = ["txt", "json", "srt"]
    caplog.clear()
    with caplog.at_level(logging.INFO, logger="yt_transcripts"):
        pipeline.download_all(mk(ids), settings, sleep=lambda s: None)
    remaining = [int(r.getMessage().rsplit(" ", 1)[1]) for r in caplog.records if "left for the remaining" in r.getMessage()]
    assert remaining == [20, 10]


def test_list_keeps_links_when_a_later_run_stops_early(settings, monkeypatch):
    from yt_transcripts.pipeline import apply_manifest

    _install(monkeypatch, ScriptedFetcher("api", {v.video_id: [_t(v.video_id)] for v in _videos()}))
    pipeline.download_all(_videos(), settings, sleep=lambda s: None)
    fresh = _videos()  # a new search finds the same videos (no status yet), and this run gets blocked
    apply_manifest(fresh, settings)
    assert all(v.transcript_status == "ok" and pipeline.Path(v.transcript_file).exists() for v in fresh)
    blocked = tr.FetchError(tr.BLOCKED, "429")
    new = Video(video_id="ddddddddddd", title="New", views=50_000, keyword="ai agents")
    _install(monkeypatch, ScriptedFetcher("api", {"ddddddddddd": [blocked]}))
    pipeline.download_all([new] + fresh, settings, sleep=lambda s: None)
    assert all(v.transcript_status == "ok" for v in fresh)


def test_changing_text_settings_rebuilds_files_without_refetching(settings, monkeypatch):
    settings.formats = ["txt", "json"]
    settings.timestamps = False
    _install(monkeypatch, ScriptedFetcher("api", {v.video_id: [_t(v.video_id)] for v in _videos()}))
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    out = pipeline.Path(settings.output_dir)
    rec = json.loads((out / "manifest.json").read_text(encoding="utf-8"))["aaaaaaaaaaa"]
    txt = out / rec["files"]["txt"]
    assert "[00:00]" not in txt.read_text(encoding="utf-8")
    settings.timestamps = True
    f = ScriptedFetcher("api", {})
    _install(monkeypatch, f)
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)
    assert f.calls == [] and "[00:00]" in txt.read_text(encoding="utf-8")
    pipeline.download_all(_videos()[:1], settings, sleep=lambda s: None)  # now in sync: plain skip
    assert f.calls == []


def test_switching_the_description_off_cleans_saved_files_without_refetching(settings, monkeypatch):
    settings.formats = ["txt", "json"]
    settings.include_description = True
    vids = _videos()[:1]
    vids[0].description = "Use my promo code SAVE10"
    _install(monkeypatch, ScriptedFetcher("api", {v.video_id: [_t(v.video_id)] for v in vids}))
    pipeline.download_all(vids, settings, sleep=lambda s: None)
    out = pipeline.Path(settings.output_dir)
    rec = json.loads((out / "manifest.json").read_text(encoding="utf-8"))["aaaaaaaaaaa"]
    txt, js = out / rec["files"]["txt"], out / rec["files"]["json"]
    assert "SAVE10" in txt.read_text(encoding="utf-8") and "SAVE10" in js.read_text(encoding="utf-8")
    settings.include_description = False
    f = ScriptedFetcher("api", {})
    _install(monkeypatch, f)
    again = _videos()[:1]
    again[0].description = "Use my promo code SAVE10"  # the search still sees it
    pipeline.download_all(again, settings, sleep=lambda s: None)
    assert f.calls == []
    assert "SAVE10" not in txt.read_text(encoding="utf-8") and "SAVE10" not in js.read_text(encoding="utf-8")
    assert "Sentence number 11." in txt.read_text(encoding="utf-8")
