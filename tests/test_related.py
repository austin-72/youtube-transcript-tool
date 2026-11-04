"""Related keywords: suggestion parsing, title phrases, tags, ranking, saving and --add."""

import json

from yt_transcripts import related
from yt_transcripts.config import build_settings, load_config
from yt_transcripts.models import Video


def S(tmp_path, **kw):
    return build_settings({"keywords": ["ai agents"], "output_dir": str(tmp_path), **kw})


def test_parse_suggest_both_forms():
    plain = '["ai agents",["ai agents","AI Agents Explained","ai agents tutorial"],[],{"x":1}]'
    assert related.parse_suggest(plain) == ["ai agents", "ai agents explained", "ai agents tutorial"]
    jsonp = 'window.google.ac.h(["q",[["ai agents course",0,[512]],["ai agents n8n",0]],{"k":1}])'
    assert related.parse_suggest(jsonp) == ["ai agents course", "ai agents n8n"]
    assert related.parse_suggest("<html>blocked</html>") == []


def _fake_get(table):
    asked = []

    def get(q):
        asked.append(q)
        if q in table:
            return json.dumps([q, table[q]])
        return json.dumps([q, [f"{q}x"]])
    return get, asked


def test_suggestions_rank_by_position_and_repeats():
    get, asked = _fake_get({"ai agents": ["ai agents explained", "ai agents tutorial"],
                            "ai agents e": ["ai agents explained", "ai agents examples"]})
    sc = related.suggestions("ai agents", S("."), get=get, pause=0)
    assert len(asked) == 1 + 26 + len(related.PREFIXES)
    assert sc["ai agents explained"] > sc["ai agents tutorial"] > sc["ai agents examples"]


def test_title_phrases_need_two_videos_and_skip_stopword_edges():
    vids = [Video(f"v{i:010d}", title=t, views=10_000) for i, t in enumerate([
        "Build AI Agents with n8n - full course", "n8n workflow automation for beginners",
        "My n8n workflow automation setup", "The best of the year"])]
    tp = related.title_phrases(vids, "ai agents")
    assert "n8n workflow automation" in tp and "workflow automation" in tp
    assert "the best" not in tp and "full course" not in tp  # only one title has it


def test_find_related_merges_sources_and_leaves_out_my_keywords(tmp_path):
    folder = tmp_path / "transcripts" / "ai agents"
    folder.mkdir(parents=True)
    for i in range(2):
        (folder / f"{i}.json").write_text(json.dumps(
            {"video": {"keyword": "ai agents", "tags": ["agentic ai", "AI Agents", "langchain"]}}), encoding="utf-8")
    get, _ = _fake_get({"ai agents": ["ai agents", "agentic ai", "ai agents tutorial"]})
    vids = [Video(f"v{i:010d}", title=f"Agentic AI demo {i}", views=1000) for i in range(3)]
    items = related.find_related(["ai agents"], S(tmp_path), get=get, pause=0,
                                 search_fn=lambda seed, s: vids)
    phrases = [r.phrase for r in items]
    assert "ai agents" not in phrases
    assert phrases[0] == "agentic ai"  # suggested + in titles + tags
    top = items[0]
    assert top.sources == {"suggested", "in titles", "tags"}
    assert "langchain" in phrases


def test_cmd_related_saves_and_adds_to_config(tmp_path, monkeypatch):
    cfg = tmp_path / "config.toml"
    cfg.write_text('[search]\nkeywords = ["ai agents"]  # mine\nmin_views = 5\n', encoding="utf-8")
    items = [related.Related("agentic ai", 3, {"suggested"}), related.Related("ai agents n8n", 2, {"suggested"}),
             related.Related("ai agents", 1, {"suggested"})]
    monkeypatch.setattr(related, "find_related", lambda seeds, s, **kw: items)
    lines = []
    s = S(tmp_path)
    assert related.cmd_related(s, ["ai agents"], add=2, config_path=cfg, out=lines.append) == 0
    assert load_config(cfg)["keywords"] == ["ai agents", "agentic ai", "ai agents n8n"]
    assert "# mine" in cfg.read_text(encoding="utf-8")
    txts = list((tmp_path / "related_keywords").glob("*.txt"))
    assert txts and "agentic ai\n" in txts[0].read_text(encoding="utf-8")
    assert any("Added 2" in ln for ln in lines)


def test_add_keywords_without_config_does_not_copy_the_example(tmp_path):
    (tmp_path / "config.example.toml").write_text('keywords = ["ai agents", "claude code tutorial"]\n',
                                                  encoding="utf-8")
    cfg = tmp_path / "config.toml"
    assert related.add_keywords(cfg, ["new one"]) == ["new one"]
    assert load_config(cfg)["keywords"] == ["new one"]
