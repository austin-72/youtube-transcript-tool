import csv
import json
from unittest import mock

import pytest
from conftest import FIXTURES

from yt_transcripts import cli, pipeline
from yt_transcripts import transcripts as tr
from yt_transcripts.config import load_config, update_config_file
from yt_transcripts.models import Segment, Transcript


def _empty(p):
    """An existing, empty settings file (a missing -c file is now an error)."""
    p.touch()
    return str(p)


@pytest.fixture
def replay_search():
    from yt_dlp.extractor.youtube._tab import YoutubeTabBaseInfoExtractor

    fixture = json.loads((FIXTURES / "search_python_week_popularity.json").read_text(encoding="utf-8"))

    def fake_response(self, item_id, query, **kw):
        if "continuation" in query:
            return {"onResponseReceivedCommands": [{"appendContinuationItemsAction": {"continuationItems": []}}]}
        return fixture

    with mock.patch.object(YoutubeTabBaseInfoExtractor, "_extract_response", fake_response), \
         mock.patch.object(YoutubeTabBaseInfoExtractor, "_download_ytcfg", lambda *a, **k: {}):
        yield


class FakeFetcher:
    name = "ytdlp"

    def __init__(self):
        self.last_info = None

    def fetch(self, v):
        self.last_info = None
        if v.video_id == "zMajAKkmxws":
            raise tr.FetchError(tr.NO_TRANSCRIPT, "video has no captions")
        import datetime as dt

        # an exact date newer than every "x days ago" in the recorded search (relative to today)
        yesterday = (dt.date.today() - dt.timedelta(days=1)).strftime("%Y%m%d")
        self.last_info = {"upload_date": yesterday, "view_count": (v.views or 0) + 1}
        segs = [Segment(i * 5.0, 5.0, f"Line {i} of {v.video_id}.") for i in range(20)]
        return Transcript(v.video_id, "en", "English", "auto", "ytdlp", segs)


def test_run_command_end_to_end(tmp_path, replay_search, monkeypatch):
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [FakeFetcher()])
    out = tmp_path / "out"
    cfg = tmp_path / "config.toml"
    cfg.write_text((FIXTURES.parent.parent / "config.example.toml").read_text(encoding="utf-8"), encoding="utf-8")
    update_config_file(cfg, {"keywords": ["python tutorial"], "min_views": 2000, "within": "week",
                             "sorts": ["popularity"], "delay_seconds": 0, "min_duration": 120,
                             "formats": ["txt", "md"]})
    code = cli.main(["run", "-c", str(cfg), "-o", str(out)])
    assert code == 0

    rows = list(csv.DictReader((out / "video_list.csv").read_text(encoding="utf-8-sig").splitlines()))
    # re-ranked with the exact dates learned during transcript download
    assert [r["video_id"] for r in rows] == ["zZgF8mvvORg", "Pfd916_a_cs", "zMajAKkmxws"]
    status = {r["video_id"]: r["transcript_status"] for r in rows}
    assert status == {"Pfd916_a_cs": "ok", "zZgF8mvvORg": "ok", "zMajAKkmxws": "no_transcript"}
    # exact date learned while fetching the transcript replaces the "15h ago" estimate
    first = rows[1]
    import datetime as dt

    yesterday = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    assert first["published"] == yesterday and first["published_exact"] == "True"

    txts = list((out / "transcripts" / "python tutorial").glob("*.txt"))
    assert len(txts) == 2
    html = (out / "video_list.html").read_text(encoding="utf-8")
    assert "Pfd916_a_cs" in html and "transcripts/python%20tutorial/" in html
    assert list((out / "lists").glob("*_video_list.csv"))
    assert (out / "last_run.log").exists()
    assert list((out / "combined").glob("transcripts_* - python tutorial.md"))
    lib = (out / "library.html").read_text(encoding="utf-8")
    assert "Pfd916_a_cs" in lib and "Searched" in html

    # second run: everything already handled -> skipped, nothing re-fetched
    calls = []
    monkeypatch.setattr(pipeline, "build_fetchers",
                        lambda s, ydl_factory=None: [type("F", (), {"name": "x", "fetch": lambda self, v: calls.append(v)})()])
    assert cli.main(["run", "-c", str(cfg), "-o", str(out)]) == 0
    assert calls == []
    rows = list(csv.DictReader((out / "video_list.csv").read_text(encoding="utf-8-sig").splitlines()))
    assert {r["video_id"]: r["published_exact"] for r in rows}["Pfd916_a_cs"] == "True"  # remembered
    assert [r["video_id"] for r in rows] == ["zZgF8mvvORg", "Pfd916_a_cs", "zMajAKkmxws"]


def test_search_only_command(tmp_path, replay_search):
    out = tmp_path / "o"
    code = cli.main(["search", "-c", _empty(tmp_path / "missing.toml"), "-o", str(out), "-k", "python tutorial",
                     "--min-views", "0", "--within", "week", "--min-duration", "0"])
    assert code == 0
    data = json.loads((out / "video_list.json").read_text(encoding="utf-8"))
    assert len(data) == 7
    assert not (out / "transcripts").exists()


def test_transcripts_command_from_url_list(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [FakeFetcher()])
    lst = tmp_path / "urls.txt"
    lst.write_text("https://youtu.be/Pfd916_a_cs\nhttps://www.youtube.com/watch?v=zMajAKkmxws\n", encoding="utf-8")
    out = tmp_path / "o"
    assert cli.main(["transcripts", str(lst), "-c", _empty(tmp_path / "none.toml"), "-o", str(out), "--delay", "0"]) == 0
    files = list((out / "transcripts").rglob("*.txt"))
    assert len(files) == 1 and "Pfd916_a_cs" in files[0].name


def test_missing_keywords_is_a_clear_error(tmp_path, capsys):
    assert cli.main(["search", "-c", _empty(tmp_path / "none.toml"), "-o", str(tmp_path / "o")]) == 2


def test_cli_overrides_config(tmp_path):
    cfg = tmp_path / "c.toml"
    cfg.write_text('[search]\nkeywords = ["a"]\nmin_views = 5\n[transcripts]\nformats = ["txt"]\n', encoding="utf-8")
    args = cli.build_parser().parse_args(["run", "-c", str(cfg), "-m", "100", "-f", "srt", "-f", "md",
                                          "--no-combine", "--methods", "ytdlp", "--translate"])
    s = cli.settings_from_args(args)
    assert s.keywords == ["a"] and s.min_views == 100 and s.formats == ["srt", "md"]
    assert s.combine is False and s.transcript_methods == ["ytdlp"] and s.translate is True
    assert load_config(cfg)["min_views"] == 5  # file untouched


def test_emoji_titles_do_not_crash_an_ascii_console(tmp_path, replay_search, monkeypatch):
    import io
    import sys

    buf = io.BytesIO()
    fake_out = io.TextIOWrapper(buf, encoding="ascii")
    monkeypatch.setattr(sys, "stdout", fake_out)
    code = cli.main(["search", "-c", _empty(tmp_path / "x.toml"), "-o", str(tmp_path / "o"), "-k", "python tutorial",
                     "--min-views", "0", "--within", "week", "--min-duration", "0"])
    fake_out.flush()
    assert code == 0
    assert b"Video Editing Using Claude AI ? Step-by-Step" in buf.getvalue()


def test_update_config_file_keeps_comments_and_tables(tmp_path):
    cfg = tmp_path / "c.toml"
    cfg.write_text('[search]\nkeywords = ["a"]  # my words\nmin_views = 5\n\n[[keyword_settings]]\n'
                   'keyword = "b"\nmin_views = 1\n', encoding="utf-8")
    update_config_file(cfg, {"min_views": 77, "keywords": ["x", 'y "q"'], "brand_new": True})
    update_config_file(cfg, {"another": 3})
    text = cfg.read_text(encoding="utf-8")
    c = load_config(cfg)
    assert "# my words" in text and c["min_views"] == 77 and c["keywords"] == ["x", 'y "q"']
    assert c["keyword_settings"] == [{"keyword": "b", "min_views": 1}]
    assert c["brand_new"] is True and c["another"] == 3


def test_status_command(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [FakeFetcher()])
    lst = tmp_path / "urls.txt"
    lst.write_text("Pfd916_a_cs\nzMajAKkmxws\n", encoding="utf-8")
    out = tmp_path / "o"
    cli.main(["transcripts", str(lst), "-c", _empty(tmp_path / "n.toml"), "-o", str(out), "--delay", "0"])
    capsys.readouterr()
    assert cli.main(["status", "-c", _empty(tmp_path / "n.toml"), "-o", str(out)]) == 0
    text = capsys.readouterr().out
    assert "1  transcripts saved" in text and "1  videos without captions" in text


def test_find_command(tmp_path, capsys, monkeypatch):
    class Talker(FakeFetcher):
        def fetch(self, v):
            self.last_info = None
            segs = [Segment(0, 5, "Welcome back to the channel."), Segment(5, 5, "Today we talk about the context"),
                    Segment(10, 5, "window and why it matters."), Segment(15, 5, "The Context Window is big.")]
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp", segs)

    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [Talker()])
    lst = tmp_path / "urls.txt"
    lst.write_text("Pfd916_a_cs\n", encoding="utf-8")
    out = tmp_path / "o"
    cli.main(["transcripts", str(lst), "-c", _empty(tmp_path / "n.toml"), "-o", str(out), "--delay", "0"])
    capsys.readouterr()
    assert cli.main(["find", "context window", "-c", _empty(tmp_path / "n.toml"), "-o", str(out)]) == 0
    text = capsys.readouterr().out
    assert "[00:05] Today we talk about the context" in text  # phrase split across two lines
    assert "[00:15] The Context Window is big." in text
    assert "https://youtu.be/Pfd916_a_cs?t=15" in text and "2 match(es) in 1 video(s)" in text


def test_export_command(tmp_path, capsys, monkeypatch):
    import csv as _csv

    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [FakeFetcher()])
    lst = tmp_path / "urls.txt"
    lst.write_text("Pfd916_a_cs\nrnati8sE0Js\n", encoding="utf-8")
    out = tmp_path / "o"
    cli.main(["transcripts", str(lst), "-c", _empty(tmp_path / "n.toml"), "-o", str(out), "--delay", "0"])
    assert cli.main(["export", "-c", _empty(tmp_path / "n.toml"), "-o", str(out)]) == 0
    jl = list((out / "exports").glob("*.jsonl"))[0].read_text(encoding="utf-8").splitlines()
    assert len(jl) == 2 and json.loads(jl[0])["segments"]
    rows = list(_csv.DictReader(list((out / "exports").glob("*.csv"))[0].read_text(encoding="utf-8-sig").splitlines()))
    assert {r["video_id"] for r in rows} == {"Pfd916_a_cs", "rnati8sE0Js"} and int(rows[0]["words"]) > 0


def test_save_never_edits_keyword_overrides(tmp_path):
    cfg = tmp_path / "c.toml"
    cfg.write_text('min_views = 1\n[[keyword_settings]]\nkeyword = "x"\ninclude_shorts = true\nmin_views = 5\n'
                   '[search]\ninclude_shorts = false\n', encoding="utf-8")
    update_config_file(cfg, {"include_shorts": True, "min_views": 9})
    c = load_config(cfg)
    assert c["keyword_settings"] == [{"keyword": "x", "include_shorts": True, "min_views": 5}]
    assert c["include_shorts"] is True and c["min_views"] == 9


def test_bad_keyword_override_is_a_validation_error():
    from yt_transcripts.config import build_settings

    s = build_settings({"keywords": ["a"], "keyword_settings": [{"keyword": "a", "within": "weekly",
                                                                 "min_views": "5,000"}]})
    problems = s.validate()
    assert any("weekly" in p for p in problems)
    assert s.for_keyword("a").min_views == 5000


def test_transcripts_for_urls_given_directly(tmp_path):
    from yt_transcripts.cli import _load_list_args

    lst = tmp_path / "mine.txt"
    lst.write_text("https://youtu.be/aaaaaaaaaaa\n", encoding="utf-8")
    vids, label = _load_list_args([str(lst), "https://www.youtube.com/watch?v=bbbbbbbbbbb&t=5",
                                   "aaaaaaaaaaa", "https://youtube.com/shorts/ccccccccccc"])
    assert [v.video_id for v in vids] == ["aaaaaaaaaaa", "bbbbbbbbbbb", "ccccccccccc"]
    assert vids[0].keyword == "mine" and vids[1].keyword == "single videos"
    assert _load_list_args(["no-such-file.csv"])[0] is None
    assert [v.video_id for v in _load_list_args(str(lst))[0]] == ["aaaaaaaaaaa"]  # one path, as the window passes


def test_pasted_links_in_one_argument(tmp_path):
    from yt_transcripts.cli import _load_list_args

    vids, _ = _load_list_args(["https://www.youtube.com/watch?v=aaaaaaaaaaa&t=5s  https://youtu.be/bbbbbbbbbbb"])
    assert [v.video_id for v in vids] == ["aaaaaaaaaaa", "bbbbbbbbbbb"]
    spaced = tmp_path / "my lists" / "a list.txt"
    spaced.parent.mkdir()
    spaced.write_text("ccccccccccc\n", encoding="utf-8")
    assert [v.video_id for v in _load_list_args([str(spaced)])[0]] == ["ccccccccccc"]


def test_selfupdate_respects_interval(tmp_path, monkeypatch):
    from yt_transcripts import cli

    monkeypatch.setattr(cli, "PROJECT_DIR", tmp_path)
    calls = []
    assert cli.cmd_selfupdate(7, runner=lambda cmd: calls.append(cmd) or 0) == 0
    assert len(calls) == 1 and "--upgrade" in calls[0] and (tmp_path / ".last_update").exists()
    assert cli.cmd_selfupdate(7, runner=lambda cmd: calls.append(cmd) or 0) == 0
    assert len(calls) == 1  # updated moments ago: skipped
    assert cli.cmd_selfupdate(0, runner=lambda cmd: calls.append(cmd) or 1) == 1  # forced; pip failed


def test_saving_keeps_comments_with_apostrophes_inside_arrays(tmp_path):
    from conftest import ROOT

    cfg = tmp_path / "config.toml"
    text = (ROOT / "config.example.toml").read_text(encoding="utf-8").replace(
        '"claude code tutorial",', '"claude code tutorial",   # Anthropic\'s CLI', 1)
    cfg.write_text(text, encoding="utf-8")
    before = load_config(cfg)
    update_config_file(cfg, {"keywords": ["x", "y"], "min_views": 5})
    after = load_config(cfg)
    assert after["keywords"] == ["x", "y"] and after["min_views"] == 5
    assert set(before) == set(after) and after.get("keyword_settings") == before.get("keyword_settings")
    assert len(cfg.read_text(encoding="utf-8").splitlines()) >= len(text.splitlines()) - 3


def test_missing_config_given_with_c_is_an_error(tmp_path):
    assert cli.main(["status", "-c", str(tmp_path / "typo.toml"), "-o", str(tmp_path / "o")]) == 2


def test_saving_twice_keeps_a_notepad_crlf_file_valid(tmp_path):
    from conftest import ROOT

    cfg = tmp_path / "config.toml"
    cfg.write_bytes((ROOT / "config.example.toml").read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))
    for n in (5, 6):
        update_config_file(cfg, {"min_views": n, "new_setting_from_window": True})
        raw = cfg.read_bytes()
        assert b"\r\r\n" not in raw and raw.count(b"\r\n") == raw.count(b"\n")
        assert load_config(cfg)["min_views"] == n


def test_missing_keys_never_land_in_a_keyword_block(tmp_path):
    cfg = tmp_path / "config.toml"
    cfg.write_text('min_views = 1\n# [saved_from_window]\n\n[[keyword_settings]]\nkeyword = "x"\n', encoding="utf-8")
    update_config_file(cfg, {"delay_seconds": 9.0})
    data = load_config(cfg)
    assert data["delay_seconds"] == 9.0 and "delay_seconds" not in data["keyword_settings"][0]
    cfg.write_text('[saved_from_window]\na = 1\n\n[[keyword_settings]]\nkeyword = "x"\n', encoding="utf-8")
    update_config_file(cfg, {"delay_seconds": 9.0})
    data = load_config(cfg)
    assert data["delay_seconds"] == 9.0 and "delay_seconds" not in data["keyword_settings"][0]


def test_key_present_in_two_sections_is_updated_everywhere(tmp_path):
    cfg = tmp_path / "config.toml"
    cfg.write_text('[search]\nmin_views = 1\n\n[saved_from_window]\nmin_views = 2\n', encoding="utf-8")
    update_config_file(cfg, {"min_views": 7})
    assert load_config(cfg)["min_views"] == 7 and cfg.read_text(encoding="utf-8").count("min_views = 7") == 2


def test_status_and_doctor_do_not_erase_last_run_log(tmp_path):
    out = tmp_path / "o"
    out.mkdir()
    (out / "last_run.log").write_text("details of the failed run", encoding="utf-8")
    assert cli.main(["status", "-c", _empty(tmp_path / "c.toml"), "-o", str(out)]) == 0
    cli.main(["find", "x", "-c", _empty(tmp_path / "c.toml"), "-o", str(out)])
    assert (out / "last_run.log").read_text(encoding="utf-8") == "details of the failed run"


def test_old_list_status_does_not_override_newer_results(tmp_path, monkeypatch):
    from yt_transcripts.config import build_settings
    from yt_transcripts.models import Video
    from yt_transcripts.writers import write_video_list

    out = tmp_path / "o"
    s = build_settings({"output_dir": str(out)})
    out.mkdir()
    (out / "transcripts").mkdir()
    f = out / "transcripts" / "a.txt"
    f.write_text("x", encoding="utf-8")
    (out / "manifest.json").write_text(
        '{"aaaaaaaaaaa": {"status": "ok", "files": {"txt": "transcripts/a.txt"}}}', encoding="utf-8")
    old = Video(video_id="aaaaaaaaaaa", title="T", transcript_status="error")
    lst = write_video_list([old], tmp_path / "lists")["csv"]
    seen = {}
    from collections import Counter

    monkeypatch.setattr(pipeline, "download_all", lambda videos, *a, **k: seen.setdefault("v", videos) and Counter())
    cli.cmd_run(s, transcripts_only_list=str(lst))
    assert seen["v"][0].transcript_status == "ok" and seen["v"][0].transcript_file.endswith("a.txt")


def test_second_run_does_not_wipe_a_busy_runs_log(tmp_path):
    from yt_transcripts.utils import RunLock

    out = tmp_path / "o"
    out.mkdir()
    (out / "last_run.log").write_text("the scheduled run is busy", encoding="utf-8")
    busy = RunLock(out)
    assert busy.acquire()
    try:
        assert cli.main(["search", "-c", _empty(tmp_path / "c.toml"), "-o", str(out), "-k", "x"]) == 3
        assert (out / "last_run.log").read_text(encoding="utf-8") == "the scheduled run is busy"
    finally:
        busy.release()


def test_export_cuts_sponsor_reads_like_the_readable_files(tmp_path):
    from yt_transcripts.config import build_settings

    t = {"text": "hi buy my thing bye", "skipped": [{"start": 10.0, "end": 20.0, "category": "sponsor"}],
         "segments": [{"start": 0, "duration": 5, "text": "hi"}, {"start": 11, "duration": 5, "text": "buy my thing"},
                      {"start": 25, "duration": 5, "text": "bye"}]}
    text, segs = cli._export_text(t, build_settings({}))
    assert text == "hi bye" and [x["text"] for x in segs] == ["hi", "bye"]
    text, _ = cli._export_text(t, build_settings({"sponsorblock": []}))
    assert "buy my thing" in text
    assert cli._export_text({"text": "x", "segments": [{"bad": 1}]}, build_settings({}))[0] == "x"
