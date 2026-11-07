"""Transcript file contents: description, chapters, tags, Markdown properties, AI-ready combined files."""

import json

from yt_transcripts import writers
from yt_transcripts.models import Segment, Transcript, Video
from yt_transcripts.search_ytdlp import apply_full_info


def _video(**kw):
    base = dict(video_id="abcdefghijk", title="A title", channel="Chan", views=1234,
                published="2026-10-27T10:00:00Z", published_exact=True, duration_seconds=300,
                keyword="python tutorial")
    base.update(kw)
    return Video(**base)


def _transcript(n=20, vid="abcdefghijk", step=10.0):
    return Transcript(vid, "en", "English (auto-generated)", "auto", "ytdlp",
                      [Segment(i * step, step, f"sentence {i}.") for i in range(n)])


def test_full_info_brings_description_tags_and_chapters():
    v = _video(description="short snippet")
    apply_full_info(v, {"description": "short snippet and the rest of the long description",
                        "tags": ["python", "", "python", "tutorial"],
                        "chapters": [{"start_time": 61, "end_time": 120, "title": "Main"},
                                     {"start_time": 0, "end_time": 61, "title": "Intro"},
                                     {"start_time": "x", "title": "broken"}, "junk"]})
    assert v.description.endswith("long description")
    assert v.tags == ["python", "tutorial"]
    assert v.chapters == [{"start": 0.0, "title": "Intro"}, {"start": 61.0, "title": "Main"}]
    # survives the saved .json (rebuilds) and tolerates junk there
    again = Video.from_dict(json.loads(json.dumps(v.to_dict())))
    assert again.chapters == v.chapters and again.tags == v.tags
    assert Video.from_dict({"video_id": "abcdefghijk", "chapters": None, "tags": None}).chapters == []
    assert Video.from_dict({"video_id": "abcdefghijk", "tags": "a; b"}).tags == ["a", "b"]


def test_merge_keeps_the_longer_description_and_chapters():
    a = _video(description="snippet")
    b = _video(description="snippet plus more", chapters=[{"start": 0.0, "title": "Intro"}], tags=["x"])
    a.merge(b)
    assert a.description == "snippet plus more" and a.chapters and a.tags == ["x"]


def test_chapters_start_new_paragraphs_with_headings():
    v = _video(chapters=[{"start": 0.0, "title": "Intro"}, {"start": 61.0, "title": "Main part"},
                         {"start": 500.0, "title": "After the captions"}])
    t = _transcript()
    txt = writers.render_txt(v, t, timestamps=True)
    assert "== Intro (00:00) ==" in txt and "== Main part (01:01) ==" in txt
    assert "After the captions" not in txt
    # the paragraph after the Main heading starts at the chapter, not mid-way through the previous one
    after = txt.split("== Main part (01:01) ==", 1)[1].strip()
    assert after.startswith("[01:00] sentence 6.")
    md = writers.render_md(v, t)
    assert "### Main part ([01:01](https://www.youtube.com/watch?v=abcdefghijk&t=61s))" in md
    # every sentence is still there exactly once
    for i in range(20):
        assert md.count(f"sentence {i}.") == 1


def test_description_in_txt_and_md_and_markdown_safe():
    v = _video(description="First line\n\n# not a heading\n- not a list")
    t = _transcript(3)
    txt = writers.render_txt(v, t)
    assert "Description:\nFirst line" in txt
    assert writers.render_txt(v, t, description=False).count("First line") == 0
    md = writers.render_md(v, t)
    assert "## Description" in md and "> \\# not a heading" in md and "> \\- not a list" in md
    assert "\n>\n" in md  # blank line kept inside the quote


def test_markdown_properties_are_valid_yaml():
    yaml = __import__("pytest").importorskip("yaml")
    v = _video(title='He said "hi": #1 — a b \\ c', channel="Chan: x",
               keyword="python tutorial; ai", tags=["t1", 'q"uote'])
    md = writers.render_md(v, _transcript(3))
    assert md.startswith("---\n")
    props = yaml.safe_load(md.split("---\n")[1])
    assert props["title"] == v.title and props["channel"] == "Chan: x"
    assert props["keywords"] == ["python tutorial", "ai"] and props["youtube_tags"] == ["t1", 'q"uote']
    assert props["views"] == 1234 and props["published"] == "2026-10-27"
    # the visible heading stays on one line
    assert "\n# He said \"hi\": #1 — a b \\ c\n" in md


def test_md_properties_without_yaml_library():
    v = _video(title="Plain")
    head = writers.render_md(v, _transcript(1)).split("---\n")[1]
    assert 'title: "Plain"' in head and "views: 1234" in head
    assert writers.render_md(v, _transcript(1), properties=False).startswith("# Plain")


def test_combined_files_one_per_keyword_and_split_by_words(tmp_path):
    entries = []
    for i in range(6):
        vid = f"vid{i:08d}"
        kw = "alpha" if i < 4 else "beta; alpha"
        entries.append((_video(video_id=vid, title=f"Video {i}", keyword=kw), _transcript(50, vid)))
    one = len(writers.render_md(*entries[0], properties=False, description=False, level=2).split())
    paths = writers.write_combined(entries, tmp_path, "2026-10-29_0300", max_words=one * 2 + 5)
    names = sorted(p.name for p in paths)
    assert names == ["transcripts_2026-10-29_0300 - alpha (part 1 of 2).md",
                     "transcripts_2026-10-29_0300 - alpha (part 2 of 2).md",
                     "transcripts_2026-10-29_0300 - beta.md"]
    part1 = (tmp_path / names[0]).read_text(encoding="utf-8")
    assert "# YouTube transcripts: alpha (part 1 of 2)" in part1
    assert "## Video 0" in part1 and "## Video 1" in part1 and "## Video 2" not in part1
    assert "---\ntitle:" not in part1 and "Description" not in part1  # lean: no per-video properties
    every = "".join(p.read_text(encoding="utf-8") for p in paths)
    for i in range(6):
        assert every.count(f"## Video {i}\n") == 1
    # no limit: one file per keyword
    paths = writers.write_combined(entries, tmp_path / "nolimit", "s", max_words=0)
    assert len(paths) == 2


def test_combined_huge_single_video_is_not_split(tmp_path):
    entries = [(_video(), _transcript(400))]
    paths = writers.write_combined(entries, tmp_path, "s", max_words=100)
    assert len(paths) == 1 and "(part" not in paths[0].name


def test_list_page_summary_keyword_filter_and_counts(tmp_path):
    from yt_transcripts.config import Settings
    from yt_transcripts.report import render_html, search_summary

    s = Settings(keywords=["ai agents", "python"], min_views=5000, within="week", rising_views_per_day=300)
    line = search_summary(s)
    assert "“ai agents”" in line and "5,000 views" in line and "300+ views/day" in line
    assert "in the last week" in line
    vids = [_video(video_id=f"vid{i:08d}", keyword=k, transcript_status=st)
            for i, (k, st) in enumerate([("ai agents", "ok"), ("python", "ok"), ("ai agents; python", "blocked")])]
    page = render_html(vids, tmp_path, summary=line)
    assert '<select id="kw">' in page and '<option value="ai agents">' in page
    assert 'data-kw="|ai agents|python|"' in page
    assert "2 with transcript" in page and "1 blocked" in page
    assert "Mentions</b>" in page and "Searched" in page
    single = render_html(vids[:1], tmp_path)  # one keyword: no dropdown
    assert '<select id="kw">' not in single


def test_preview_skips_description_and_chapter_headings(tmp_path):
    from yt_transcripts.report import transcript_preview

    v = _video(description="Promo\n" + "-" * 60 + "\nmore promo",
               chapters=[{"start": 0.0, "title": "Intro"}, {"start": 61.0, "title": "Main"}])
    t = _transcript(10)
    for fmt, content in (("txt", writers.render_txt(v, t)), ("md", writers.render_md(v, t))):
        p = tmp_path / f"x.{fmt}"
        p.write_text(content, encoding="utf-8")
        pv = transcript_preview(str(p))
        assert pv.startswith("sentence 0."), (fmt, pv)
        assert "Promo" not in pv and "Intro" not in pv and "Main" not in pv


def test_library_merges_every_saved_list_and_uses_the_manifest(tmp_path):
    from yt_transcripts.config import Settings

    s = Settings(keywords=["a"], output_dir=str(tmp_path))
    lists = tmp_path / "lists"
    old = [_video(video_id="aaaaaaaaaaa", title="Old", keyword="alpha", views=10, transcript_status="blocked"),
           _video(video_id="bbbbbbbbbbb", title="Both", keyword="alpha", views=100)]
    new = [_video(video_id="bbbbbbbbbbb", title="Both", keyword="beta", views=500,
                  description="x" * 3000)]
    writers.write_video_list(old, lists, "2026-10-01_0900_video_list")
    writers.write_video_list(new, lists, "2026-10-02_0900_video_list")
    js = json.loads((lists / "2026-10-02_0900_video_list.json").read_text(encoding="utf-8"))
    assert len(js[0]["description"]) == writers.LIST_DESCRIPTION_CHARS  # lists keep only a snippet
    tx = tmp_path / "transcripts" / "b.txt"
    tx.parent.mkdir(parents=True)
    tx.write_text("Title: x\n" + "-" * 60 + "\n\nhello there\n", encoding="utf-8")
    (tmp_path / "manifest.json").write_text(json.dumps(
        {"bbbbbbbbbbb": {"status": "ok", "files": {"txt": "transcripts/b.txt"}}}), encoding="utf-8")
    path = writers.write_library(tmp_path, s)
    page = path.read_text(encoding="utf-8")
    assert path.name == "library.html" and "All collected videos" in page
    assert page.count("<tr data-kw") == 2
    assert 'data-kw="|beta|alpha|"' in page and "500" in page  # keywords from both lists, newest views
    assert "hello there" in page  # transcript preview via the manifest
    assert "Blocked" not in page  # a stale status saved in an old list is not shown
    assert writers.write_library(tmp_path / "empty", s) is None


def test_combined_names_never_collide_or_lose_the_part_number(tmp_path):
    long_kw = "a very long keyword " * 5
    entries = [(_video(video_id=f"vid{i:08d}", title=f"V{i}", keyword=k), _transcript(30, f"vid{i:08d}"))
               for i, k in enumerate([long_kw, long_kw, long_kw, "AI: news", "AI news", "Python", "python"])]
    one = len(writers.render_md(*entries[0], properties=False, description=False, level=2).split())
    paths = writers.write_combined(entries, tmp_path, "s", max_words=one + 5)
    names = [p.name.lower() for p in paths]
    assert len(names) == len(set(names)) == 7  # 3 parts + 4 keywords, none overwritten (case-insensitive)
    assert sum("(part" in n for n in names) == 3 and all(len(n) < 120 for n in names)
    assert len(list(tmp_path.iterdir())) == 7


def test_yaml_escapes_characters_beyond_the_basic_plane():
    yaml = __import__("pytest").importorskip("yaml")
    flag = "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F"
    v = _video(title=f"Go {flag} team")
    props = yaml.safe_load(writers.render_md(v, _transcript(1)).split("---\n")[1])
    assert props["title"] == v.title


def test_summary_shows_the_cut_off_actually_used(tmp_path):
    from yt_transcripts.config import Settings
    from yt_transcripts.report import search_summary, transcript_preview

    assert "last 7 days" in search_summary(Settings(keywords=["x"], within="week", max_age_days=30))
    assert "last 3 days" in search_summary(Settings(keywords=["x"], within="week", max_age_days=3))
    t = Transcript("abcdefghijk", "en", "English", "auto", "ytdlp", [Segment(0, 5, "# one - two")])
    p = tmp_path / "x.md"
    p.write_text(writers.render_md(_video(), t), encoding="utf-8")
    assert transcript_preview(str(p)) == "# one - two"


# ---- description / chapters / timestamps are optional -------------------------------------------------
def _rich_video():
    return Video(video_id="abcdefghijk", title="T", channel="C", published="2026-11-01", views=10,
                 description="Links in my bio! 0:00 intro 1:00 main", tags=["x"],
                 chapters=[{"start": 0.0, "end": 60.0, "title": "Intro"}, {"start": 60.0, "end": 120.0, "title": "Main"}])


def _rich_transcript():
    return Transcript("abcdefghijk", "en", "English", "auto", "ytdlp",
                      [Segment(0, 30, "hello there."), Segment(61, 30, "the main part.")])


def test_description_chapters_and_timestamps_are_left_out_unless_asked(tmp_path):
    files = writers.write_transcript(_rich_video(), _rich_transcript(), tmp_path, ["txt", "md", "json"],
                                     timestamps=False, description=False, chapters=False)
    txt, md = files["txt"].read_text(encoding="utf-8"), files["md"].read_text(encoding="utf-8")
    js = json.loads(files["json"].read_text(encoding="utf-8"))
    for text in (txt, md):
        assert "Links in my bio" not in text and "Intro" not in text and "Chapters:" not in text
        assert "&t=" not in text and "[00:00]" not in text and "[00:01:01]" not in text
        assert "hello there." in text and "the main part." in text
    assert js["video"]["description"] == "" and js["video"]["chapters"] == []
    assert js["transcript"]["segments"][1]["start"] == 61  # the timing itself is kept in the .json
    files = writers.write_transcript(_rich_video(), _rich_transcript(), tmp_path / "on", ["txt", "md", "json"],
                                     timestamps=True, description=True, chapters=True)
    txt, md = files["txt"].read_text(encoding="utf-8"), files["md"].read_text(encoding="utf-8")
    assert "Links in my bio" in txt and "== Main (01:00) ==" in txt and "[01:01] the main part." in txt
    assert "Links in my bio" in md and "&t=61s" in md and "## Main" in md
    assert json.loads(files["json"].read_text(encoding="utf-8"))["video"]["chapters"]


def test_combined_file_and_list_follow_the_settings(tmp_path):
    v, t = _rich_video(), _rich_transcript()
    [path] = writers.write_combined([(v, t)], tmp_path, "2026-11-07_0100", timestamps=False, chapters=False)
    text = path.read_text(encoding="utf-8")
    assert "&t=" not in text and "Intro" not in text and "hello there." in text
    paths = writers.write_video_list([v], tmp_path, description=False, chapters=False)
    row = json.loads(paths["json"].read_text(encoding="utf-8"))[0]
    assert row["description"] == "" and row["chapters"] == []
    assert v.description and v.chapters  # the video itself is untouched (search filters still see it)


def test_settings_defaults_and_the_old_timestamp_name():
    from yt_transcripts.config import build_settings

    s = build_settings({})
    assert (s.timestamps, s.include_description, s.chapters) == (False, False, False)
    assert build_settings({"txt_timestamps": True}).timestamps is True  # configs from before keep working
    assert build_settings({"txt_timestamps": True, "timestamps": False}).timestamps is False
    assert not build_settings({"txt_timestamps": True})._unknown_keys  # type: ignore[attr-defined]
