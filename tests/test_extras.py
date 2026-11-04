"""SponsorBlock cuts, repeated-transcript detection and top comments."""

import hashlib
import json

import pytest

from yt_transcripts import dupes, pipeline, sponsorblock
from yt_transcripts.config import build_settings
from yt_transcripts.models import Segment, Transcript, Video


# ---- SponsorBlock ---------------------------------------------------------------------------------------
def _answer(vid, segs):
    return [{"videoID": "someOtherVid", "segments": [{"segment": [0, 50], "category": "sponsor"}]},
            {"videoID": vid, "segments": segs}]


def test_sponsorblock_lookup_uses_a_hash_prefix_and_picks_this_video():
    asked = []

    def get(url, params):
        asked.append((url, params))
        return _answer("abcdefghijk", [
            {"segment": [30.0, 60.0], "category": "sponsor", "videoDuration": 600},
            {"segment": [500, 520], "category": "interaction", "videoDuration": 600.4},
            {"segment": [100, 110], "category": "sponsor", "videoDuration": 300},  # an older, shorter upload
            {"segment": [0, 0], "category": "sponsor"},
            {"segment": "bad", "category": "sponsor"}])
    segs = sponsorblock.fetch_segments("abcdefghijk", ["sponsor", "interaction"], 600, get=get)
    assert segs == [{"start": 30.0, "end": 60.0, "category": "sponsor"},
                    {"start": 500.0, "end": 520.0, "category": "interaction"}]
    url, params = asked[0]
    prefix = hashlib.sha256(b"abcdefghijk").hexdigest()[:sponsorblock.HASH_PREFIX]
    assert url.endswith("/" + prefix) and "abcdefghijk" not in url + json.dumps(params)
    assert json.loads(params["categories"]) == ["sponsor", "interaction"]


def test_sponsorblock_failure_or_off_costs_nothing():
    def boom(url, params):
        raise OSError("down")
    assert sponsorblock.fetch_segments("abcdefghijk", ["sponsor"], get=boom) is None  # failed: asked again later
    called = []
    assert sponsorblock.fetch_segments("abcdefghijk", [], get=lambda u, p: called.append(1)) == [] and not called


def _fake_fetcher(text_segments, comments=None):
    class F:
        name, last_info = "ytdlp", None
        last_comments = comments or []

        def fetch(self, v):
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp",
                              [Segment(i * 10.0, 10.0, t) for i, t in enumerate(text_segments)])
    return F


def test_sponsor_parts_are_cut_from_readable_files_but_kept_in_json(tmp_path, monkeypatch):
    texts = ["welcome to the video", "this video is sponsored by Acme", "use code ACME for ten percent",
             "now back to the actual topic", "please like and subscribe", "the end"]
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [_fake_fetcher(texts)()])
    monkeypatch.setattr(sponsorblock, "fetch_segments", lambda vid, cats, duration=None, **k: [
        {"start": 10.0, "end": 30.0, "category": "sponsor"}, {"start": 40.0, "end": 50.0, "category": "interaction"}])
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0,
                        "formats": ["txt", "md", "json"]})
    pipeline.download_all([Video("vid00000001", title="T", keyword="k")], s)
    folder = tmp_path / "transcripts" / "k"
    txt = next(folder.glob("*.txt")).read_text(encoding="utf-8")
    body = txt.split("-" * 60, 1)[1]
    assert "Acme" not in body and "ACME" not in body and "subscribe" not in body and "actual topic" in body
    assert "Skipped (SponsorBlock): sponsor 00:10-00:30, subscribe reminder 00:40-00:50" in txt
    js = json.loads(next(folder.glob("*.json")).read_text(encoding="utf-8"))
    assert "sponsored by Acme" in js["transcript"]["text"] and len(js["transcript"]["skipped"]) == 2
    # switched off later: rebuilt from the .json, nothing downloaded, text complete again
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: pytest.fail("no download"))
    s2 = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0,
                         "formats": ["txt", "md", "json"], "sponsorblock": []})
    pipeline.download_all([Video("vid00000001", title="T", keyword="k")], s2)
    assert "sponsored by Acme" in next(folder.glob("*.txt")).read_text(encoding="utf-8")


# ---- repeated transcripts ----------------------------------------------------------------------------------
def _speech(seed, n):
    import random

    rnd = random.Random(seed)
    vocab = [f"w{i}" for i in range(3000)]
    return " ".join(rnd.choice(vocab) for _ in range(n))


def test_no_false_positives_between_videos_on_one_topic(tmp_path):
    """Different videos share stock phrases; that must never make them 'the same'."""
    stock = "hey everyone welcome back to the channel today we are going to talk about ai agents and why they matter "
    idx = dupes.DuplicateIndex(tmp_path)
    texts = {f"v{i:010d}": stock * 3 + _speech(i, 1500) + " " + stock * 2 for i in range(30)}
    for vid, text in texts.items():
        rep, contained = idx.check_and_add(vid, vid, text, texts.get)
        assert rep is None and contained == []


def test_clip_and_reupload_are_found_both_ways(tmp_path):
    full = _speech(1, 3000)
    words = full.split()
    clip = " ".join(words[1000:1400])
    reupload = " ".join(words[:1500] + ["um"] + words[1500:])  # captions differ by one word
    texts = {}
    idx = dupes.DuplicateIndex(tmp_path)
    texts["clip0000000"] = clip
    assert idx.check_and_add("clip0000000", "Clip", clip, texts.get) == (None, [])
    texts["full0000000"] = full
    rep, contained = idx.check_and_add("full0000000", "Full", full, texts.get)
    assert rep is None and contained == ["clip0000000"]  # the clip came first: reported the other way round
    texts["reup0000000"] = reupload
    rep, _ = idx.check_and_add("reup0000000", "Re-upload", reupload, texts.get)
    assert rep == ("full0000000", "Full")
    idx.save()
    again = dupes.DuplicateIndex(tmp_path)  # remembered across runs
    texts["clip2000000"] = clip
    assert again.check_and_add("clip2000000", "Clip again", clip, texts.get)[0] is not None


def test_short_texts_are_never_called_duplicates(tmp_path):
    idx = dupes.DuplicateIndex(tmp_path)
    t = "thanks for watching see you next time " * 10  # 70 words
    texts = {"a" * 11: t, "b" * 11: t}
    idx.check_and_add("a" * 11, "A", t, texts.get)
    assert idx.check_and_add("b" * 11, "B", t, texts.get) == (None, [])


def test_repeats_are_marked_and_left_out_of_combined_files(tmp_path, monkeypatch):
    full = _speech(7, 2000)
    clip = " ".join(full.split()[200:700])
    bodies = {"vid00000001": clip, "vid00000002": full, "vid00000003": _speech(8, 900)}

    class F:
        name, last_info, last_comments = "ytdlp", None, []

        def fetch(self, v):
            ws = bodies[v.video_id].split()
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp",
                              [Segment(i, 1, " ".join(ws[i * 20:(i + 1) * 20])) for i in range((len(ws) + 19) // 20)])
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [F()])
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt", "json"]})
    vids = [Video(vid, title=f"Video {vid[-1]}", keyword="k") for vid in bodies]
    pipeline.download_all(vids, s)
    assert vids[0].duplicate_of.startswith("vid00000002") and not vids[1].duplicate_of and not vids[2].duplicate_of
    combined = next((tmp_path / "combined").glob("*.md")).read_text(encoding="utf-8")
    assert "## Video 2" in combined and "## Video 3" in combined and "## Video 1" not in combined
    from yt_transcripts.report import render_html

    page = render_html(vids, tmp_path)
    assert page.count(">repeat</a>") == 1
    # the next run remembers it
    vids2 = [Video(vid, title=f"Video {vid[-1]}", keyword="k") for vid in bodies]
    pipeline.apply_manifest(vids2, s)
    assert vids2[0].duplicate_of.startswith("vid00000002")


# ---- top comments ----------------------------------------------------------------------------------------
def test_top_comments_from_ytdlp_post_extractor():
    from yt_transcripts import transcripts as tr

    calls = []

    def post():
        calls.append(1)
        return {"comments": [{"author": "@a", "text": "Great point at 3:10", "like_count": 5, "parent": "root"},
                             {"author": "@b", "text": "reply", "like_count": 99, "parent": "xyz"},
                             {"author": "@c", "text": "Best explanation", "like_count": 40, "parent": "root"}]}
    f = tr.YtDlpFetcher(build_settings({"top_comments": 2}))
    assert f._top_comments({"__post_extractor": post}) == [
        {"author": "@c", "text": "Best explanation", "likes": 40}, {"author": "@a", "text": "Great point at 3:10", "likes": 5}]
    off = tr.YtDlpFetcher(build_settings({"top_comments": 0}))
    assert off._top_comments({"__post_extractor": post}) == [] and len(calls) == 1  # off: never fetched

    def broken():
        raise RuntimeError("comments disabled")
    assert f._top_comments({"__post_extractor": broken}) == []


def test_comment_options_only_when_asked():
    from yt_transcripts.ytdlp_common import base_options

    assert "max_comments" not in base_options(build_settings({}))["extractor_args"]["youtube"]
    yt = base_options(build_settings({"top_comments": 15}))["extractor_args"]["youtube"]
    assert yt["max_comments"] == ["15", "15", "0", "0", "1"] and yt["comment_sort"] == ["top"]


def test_comments_are_written_and_kept_out_of_the_list(tmp_path, monkeypatch):
    comments = [{"author": "@viewer", "text": "You skipped the hard part", "likes": 120}]
    monkeypatch.setattr(pipeline, "build_fetchers",
                        lambda s, ydl_factory=None: [_fake_fetcher(["hello there friends"], comments)()])
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0,
                        "formats": ["txt", "md", "json"], "top_comments": 5})
    vids = [Video("vid00000001", title="T", keyword="k")]
    pipeline.download_all(vids, s)
    folder = tmp_path / "transcripts" / "k"
    assert "@viewer (120 likes): You skipped the hard part" in next(folder.glob("*.txt")).read_text(encoding="utf-8")
    assert "## Top comments" in next(folder.glob("*.md")).read_text(encoding="utf-8")
    assert json.loads(next(folder.glob("*.json")).read_text(encoding="utf-8"))["video"]["comments"] == comments
    from yt_transcripts.writers import write_video_list

    write_video_list(vids, tmp_path)
    assert "comments" not in json.loads((tmp_path / "video_list.json").read_text(encoding="utf-8"))[0]
    combined = next((tmp_path / "combined").glob("*.md")).read_text(encoding="utf-8")
    assert "### Top comments" in combined and "You skipped the hard part" in combined


# ---- regressions from the review -----------------------------------------------------------------------
def _fetcher_for(bodies):
    class F:
        name, last_info, last_comments = "ytdlp", None, []

        def fetch(self, v):
            ws = bodies[v.video_id].split()
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp",
                              [Segment(i, 1, " ".join(ws[i * 20:(i + 1) * 20])) for i in range((len(ws) + 19) // 20)])
    return F


def test_a_run_where_every_new_video_is_a_repeat_finishes(tmp_path, monkeypatch):
    full = _speech(21, 1500)
    bodies = {"vid00000001": full, "vid00000002": full}
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [_fetcher_for(bodies)()])
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt", "json"]})
    pipeline.download_all([Video("vid00000001", title="One", keyword="k")], s)
    stats = pipeline.download_all([Video("vid00000002", title="Two", keyword="k")], s)  # only a re-upload
    assert stats["ok"] == 1
    txt = next(p for p in (tmp_path / "transcripts" / "k").glob("*Two*.txt")).read_text(encoding="utf-8")
    assert "Repeats: One (https://www.youtube.com/watch?v=vid00000001)" in txt  # written into the file


def test_clip_found_later_in_the_run_gets_its_files_rewritten(tmp_path, monkeypatch):
    full = _speech(22, 2000)
    bodies = {"vid00000001": " ".join(full.split()[100:600]), "vid00000002": full}
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [_fetcher_for(bodies)()])
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt", "json"]})
    pipeline.download_all([Video("vid00000001", title="Clip", keyword="k"),
                           Video("vid00000002", title="Full", keyword="k")], s)
    clip = next(p for p in (tmp_path / "transcripts" / "k").glob("*Clip*.txt")).read_text(encoding="utf-8")
    assert "Repeats: Full" in clip
    js = json.loads(next(p for p in (tmp_path / "transcripts" / "k").glob("*Clip*.json")).read_text(encoding="utf-8"))
    assert js["video"]["duplicate_of"].startswith("vid00000002")


def test_two_videos_never_point_at_each_other_and_old_flags_clear(tmp_path, monkeypatch):
    full = _speech(23, 1500)
    bodies = {"vid00000001": full, "vid00000002": full}
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [_fetcher_for(bodies)()])
    s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt", "json"],
                        "retry_failed": True})
    x, y = Video("vid00000001", title="X", keyword="k"), Video("vid00000002", title="Y", keyword="k")
    pipeline.download_all([x, y], s)
    assert not x.duplicate_of and y.duplicate_of.startswith("vid00000001")
    # X's files go missing and X is downloaded again: it must not now be "a repeat of Y"
    for f in (tmp_path / "transcripts" / "k").glob("*[[]vid00000001[]]*"):
        f.unlink()
    m = json.loads((tmp_path / "manifest.json").read_text())
    m["vid00000001"]["status"] = "error"
    (tmp_path / "manifest.json").write_text(json.dumps(m))
    x2 = Video("vid00000001", title="X", keyword="k")
    pipeline.download_all([x2], s)
    assert not x2.duplicate_of
    assert json.loads((tmp_path / "manifest.json").read_text())["vid00000001"].get("duplicate_of", "") == ""


def test_different_non_latin_transcripts_are_not_repeats(tmp_path):
    import random

    rnd = random.Random(5)
    han = [chr(c) for c in range(0x4E00, 0x4E00 + 2000)]
    code = "public static void main String args System out println int i for".split()
    a = " ".join("".join(rnd.choice(han) for _ in range(12)) + " " + " ".join(code[:6]) for _ in range(60))
    b = " ".join("".join(rnd.choice(han) for _ in range(12)) + " " + " ".join(code) for _ in range(80))
    idx = dupes.DuplicateIndex(tmp_path)
    texts = {"a" * 11: a, "b" * 11: b}
    assert idx.check_and_add("a" * 11, "A", a, texts.get) == (None, [])
    assert idx.check_and_add("b" * 11, "B", b, texts.get) == (None, [])
    russian = " ".join(f"слово{i % 400} пример{i % 97}" for i in range(600))
    assert len(dupes.words(russian)) == 1200  # Cyrillic counts as words, not dropped


def test_sponsorblock_is_asked_again_for_added_categories_and_new_uploads(tmp_path, monkeypatch):
    import datetime as dt

    texts = ["intro music and hello", "the real content starts here", "and it continues", "the end"]
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [_fake_fetcher(texts)()])
    calls = []

    def lookup(vid, cats, duration=None, **k):
        calls.append(sorted(cats))
        return [{"start": 0.0, "end": 10.0, "category": "intro"}] if "intro" in cats else []
    monkeypatch.setattr(sponsorblock, "fetch_segments", lookup)
    base = {"keywords": ["k"], "output_dir": str(tmp_path), "delay_seconds": 0, "formats": ["txt", "json"]}
    yesterday = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).isoformat()
    v = lambda: Video("vid00000001", title="T", keyword="k", published=yesterday, published_exact=True)  # noqa: E731
    pipeline.download_all([v()], build_settings(base))
    assert len(calls) == 1
    pipeline.download_all([v()], build_settings(base))  # checked minutes ago: not asked again yet
    assert len(calls) == 1
    s2 = build_settings({**base, "sponsorblock": ["sponsor", "selfpromo", "interaction", "intro"]})
    pipeline.download_all([v()], s2)  # a category was added: asked again, files rewritten without the intro
    assert len(calls) == 2 and "intro" in calls[-1]
    txt = next((tmp_path / "transcripts" / "k").glob("*.txt")).read_text(encoding="utf-8")
    assert "intro music" not in txt.split("-" * 60, 1)[1] and "real content" in txt
    # a young video with no segments yet is asked again once 12 hours have passed
    m = json.loads((tmp_path / "manifest.json").read_text())
    m["vid00000001"]["sb"] = {"asked": ["interaction", "selfpromo", "sponsor"], "found": 0, "tries": 1,
                              "checked": (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=13)).isoformat()}
    (tmp_path / "manifest.json").write_text(json.dumps(m))
    pipeline.download_all([v()], build_settings(base))
    assert len(calls) == 3


def test_duplicate_index_loads_only_when_needed(tmp_path):
    (tmp_path / dupes.INDEX_FILE).write_text("{not json")
    idx = dupes.DuplicateIndex(tmp_path)
    assert not idx.loaded
    idx.save()  # nothing checked: the (broken) file is left alone
    assert (tmp_path / dupes.INDEX_FILE).read_text() == "{not json"
