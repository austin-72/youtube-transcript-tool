"""trends.html from the dated lists."""

import json

from yt_transcripts import trends


def _list(folder, stamp, rows, kind="video_list"):
    (folder / f"{stamp}_{kind}.json").write_text(json.dumps(rows), encoding="utf-8")


def _row(vid, kw, views, published, first_seen, is_new=False):
    return {"video_id": vid, "title": f"T {vid}", "channel": "C", "views": views, "published": published,
            "keyword": kw, "first_seen": first_seen, "is_new": is_new}


def test_collect_counts_new_videos_and_attention_per_day(tmp_path):
    lists = tmp_path / "lists"
    lists.mkdir()
    a = _row("a" * 11, "ai agents", 1000, "2026-11-01T00:00:00+00:00", "2026-11-01T08:00")
    b = _row("b" * 11, "ai agents; mcp", 5000, "2026-11-02T00:00:00+00:00", "2026-11-02T08:00", True)
    _list(lists, "2026-11-01_0800", [a])
    _list(lists, "2026-11-01_0700", [])  # an earlier run the same day: the later one counts
    _list(lists, "2026-11-02_0800", [a, b])
    _list(lists, "2026-11-02_0900", [_row("c" * 11, "@chan", 300, "2026-11-02T00:00:00+00:00",
                                          "2026-11-02T09:00", True)], kind="channel_list")
    d = trends.collect(tmp_path)
    assert d["days"] == ["2026-11-01", "2026-11-02"]
    s = d["series"]
    assert s["ai agents"]["count"] == [1, 2] and s["ai agents"]["new"] == [0, 1]
    assert s["mcp"]["new"] == [0, 1] and s["@chan"]["count"] == [0, 1]
    assert s["ai agents"]["attention"][1] > s["ai agents"]["attention"][0] > 0
    assert d["risers"][0]["id"] == "b" * 11
    page = trends.render(d)
    assert "Keyword trends" in page
    assert trends.write_trends(tmp_path).name == "trends.html"


def test_one_day_explains_itself_and_no_lists_writes_nothing(tmp_path):
    assert trends.write_trends(tmp_path) is None
    (tmp_path / "lists").mkdir()
    _list(tmp_path / "lists", "2026-11-01_0800", [_row("a" * 11, "k", 10, "2026-11-01", "2026-11-01T08:00")])
    page = trends.write_trends(tmp_path).read_text(encoding="utf-8")
    assert "at least two different days" in page


def test_titles_cannot_break_out_of_the_page(tmp_path):
    (tmp_path / "lists").mkdir()
    evil = _row("a" * 11, "<!--<script></script><script>alert(1)</script>", 10, "2026-11-01", "2026-11-01T08:00")
    evil["title"] = "<img src=x onerror=alert(1)>"
    _list(tmp_path / "lists", "2026-11-01_0800", [evil])
    page = trends.write_trends(tmp_path).read_text(encoding="utf-8")
    assert "<img src=x" not in page and "</script><script>alert" not in page and "<!--<script" not in page
    data = page.split('<script type="application/json" id="data">', 1)[1].split("</script>", 1)[0]
    assert "<" not in data and json.loads(data)["keys"]


def test_ai_guide_is_written_and_respects_hand_edits(tmp_path):
    from yt_transcripts.ai_guide import MARK, write_ai_guide
    from yt_transcripts.config import build_settings

    s = build_settings({"keywords": ["ai agents"], "channels": ["@chan"], "output_dir": str(tmp_path)})
    (tmp_path / "manifest.json").write_text(json.dumps({"a" * 11: {"status": "ok", "run": "2026-11-04_0900"}}))
    paths = write_ai_guide(tmp_path, s)
    assert {p.name for p in paths} == {"CLAUDE.md", "AGENTS.md"}
    text = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert text.startswith(MARK) and '"ai agents"' in text and "1 transcripts saved" in text and "@chan" in text
    (tmp_path / "CLAUDE.md").write_text("# my own notes\n", encoding="utf-8")
    assert [p.name for p in write_ai_guide(tmp_path, s)] == ["AGENTS.md"]
    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8") == "# my own notes\n"
