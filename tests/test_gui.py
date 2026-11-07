"""GUI smoke test: builds the window hidden, checks value collection and saving. Skipped without a display."""

import os
import sys

import pytest

tk = pytest.importorskip("tkinter")


@pytest.fixture
def root():
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        pytest.skip("no display")
    try:
        r = tk.Tk()
    except tk.TclError:
        pytest.skip("no display")
    r.withdraw()
    yield r
    r.destroy()


def test_collect_and_save(root, tmp_path):
    from conftest import ROOT

    from yt_transcripts import gui
    from yt_transcripts.config import load_config

    cfg = tmp_path / "config.toml"
    cfg.write_text((ROOT / "config.example.toml").read_text(encoding="utf-8"), encoding="utf-8")
    app = gui.App(root, cfg)
    app.keywords.delete("1.0", "end")
    app.keywords.insert("1.0", "ai agents\n\n  mcp servers  \n")
    app.vars["min_views"].set("25,000")
    app.vars["within"].set("This week")
    app.vars["min_duration"].set("2.5")
    app.vars["missing"].set(gui.MISSING_LABELS["translate"])
    for f in gui.FORMATS:
        app.vars[f"fmt_{f}"].set(f in ("md", "srt"))
    values = app.collect()
    assert values["keywords"] == ["ai agents", "mcp servers"]
    assert values["rising_views_per_day"] == 0
    assert values["min_views"] == 25_000 and values["within"] == "week" and values["min_duration"] == 150
    assert values["translate"] is True and values["allow_other_languages"] is True
    assert values["formats"] == ["md", "srt"]

    app._save()
    saved = load_config(cfg)
    assert saved["keywords"] == ["ai agents", "mcp servers"] and saved["min_views"] == 25_000
    assert saved["formats"] == ["md", "srt"] and saved["translate"] is True


def test_bad_number_is_reported(root, tmp_path):
    from yt_transcripts import gui

    app = gui.App(root, tmp_path / "none.toml")
    app.vars["min_views"].set("lots")
    with pytest.raises(ValueError, match="min views"):
        app.collect()


def test_broken_config_opens_with_defaults(root, tmp_path, monkeypatch):
    from yt_transcripts import gui

    shown = []
    monkeypatch.setattr(gui, "show_startup_error", lambda msg, parent=None: shown.append(msg))
    cfg = tmp_path / "config.toml"
    cfg.write_text('output_dir = "C:\\Users\\me"\n', encoding="utf-8")
    app = gui.App(root, cfg)
    assert len(shown) == 1 and "single quotes" in shown[0]
    assert app.vars["min_views"].get()  # defaults filled in


def test_progress_bar_follows_log(root, tmp_path):
    from yt_transcripts import gui

    app = gui.App(root, tmp_path / "none.toml")
    app._update_progress(["23:00:01  [2/4] Keyword: 'ai agents'"])
    assert app.phase.get() == "Searching keyword 2/4" and float(app.progress["value"]) == 1.5
    app._update_progress(["23:00:05  Downloading transcripts for 10 videos -> x",
                          "23:00:09  [3/10] OK    Some title  (en, auto, 900 words)"])
    assert app.phase.get() == "Transcripts 3/10" and float(app.progress["maximum"]) == 10


def test_progress_ignores_brackets_inside_titles(root, tmp_path):
    from yt_transcripts import gui

    app = gui.App(root, tmp_path / "none.toml")
    app._update_progress(["23:00:01  [3/10] OK    Keyword: secrets [2/5] of SEO  (en, auto, 10 words)"])
    assert app.phase.get() == "Transcripts 3/10"
    app._update_progress(["23:00:02    2026-10-28~  5,000  1:00  Top [1/2] tips  -  Chan"])
    assert app.phase.get() == "Transcripts 3/10"


def test_paste_links_runs_transcripts_for_them(root, tmp_path, monkeypatch):
    import time
    from tkinter import simpledialog

    from yt_transcripts import cli, gui

    got = {}
    monkeypatch.setattr(simpledialog, "askstring", lambda *a, **k: "https://youtu.be/aaaaaaaaaaa  bbbbbbbbbbb")
    monkeypatch.setattr(cli, "cmd_run", lambda s, transcripts_only_list=None, should_stop=None, channels=None:
                        got.setdefault("list", transcripts_only_list))
    app = gui.App(root, tmp_path / "none.toml")
    app.keywords.delete("1.0", "end")  # no keywords needed for links
    app.vars["output_dir"].set(str(tmp_path / "out"))
    app._start("list")
    for _ in range(50):
        if not (app.worker and app.worker.is_alive()):
            break
        time.sleep(0.05)
    assert got["list"] == "https://youtu.be/aaaaaaaaaaa  bbbbbbbbbbb"


def test_save_refuses_while_config_is_broken_and_keeps_output_relative(root, tmp_path, monkeypatch):
    from tkinter import messagebox

    from yt_transcripts import gui
    from yt_transcripts.config import load_config

    errors = []
    monkeypatch.setattr(gui, "show_startup_error", lambda *a, **k: None)
    monkeypatch.setattr(messagebox, "showerror", lambda title, msg, **k: errors.append(title))
    cfg = tmp_path / "config.toml"
    cfg.write_text('min_views = 50000\nwithin = week\n', encoding="utf-8")  # typo: unquoted
    app = gui.App(root, cfg)
    app._save()
    assert errors == ["Fix config.toml first"] and "50000" in cfg.read_text(encoding="utf-8")

    cfg.write_text('min_views = 50000\nwithin = "week"\n', encoding="utf-8")
    app = gui.App(root, cfg)
    app.vars["output_dir"].set(str(gui.PROJECT_DIR / "output"))
    app._save()
    assert load_config(cfg)["output_dir"] == "output"


def test_bad_proxy_file_is_reported_in_the_window(root, tmp_path, monkeypatch):
    from tkinter import messagebox

    from yt_transcripts import gui

    shown = []
    monkeypatch.setattr(messagebox, "showerror", lambda title, msg, **k: shown.append((title, msg)))
    cfg = tmp_path / "config.toml"
    cfg.write_text('keywords = ["x"]\nproxy_file = "nope.txt"\n', encoding="utf-8")
    app = gui.App(root, cfg)
    app.vars["output_dir"].set(str(tmp_path / "out"))
    app._start("run")
    assert shown and shown[0][0] == "Proxy" and "does not exist" in shown[0][1]
    assert not (app.worker and app.worker.is_alive())


def test_proxy_field_holds_the_whole_list(root, tmp_path):
    from yt_transcripts import gui
    from yt_transcripts.config import load_config

    cfg = tmp_path / "config.toml"
    cfg.write_text('[network]\nproxy = "http://a:1"\nproxies = ["http://b:2"]\n', encoding="utf-8")
    app = gui.App(root, cfg)
    assert app.vars["proxy"].get() == "http://a:1 http://b:2"
    app.vars["proxy"].set("")  # clearing the field turns proxies off
    app._save()
    saved = load_config(cfg)
    assert saved["proxy"] == "" and saved["proxies"] == []


def test_advanced_section_is_hidden_but_shows_what_is_in_use(root, tmp_path):
    from yt_transcripts import gui

    cfg = tmp_path / "config.toml"
    cfg.write_text('[network]\nproxy = "http://a:1 http://b:2"\ncookies_from_browser = "firefox"\n',
                   encoding="utf-8")
    app = gui.App(root, cfg)
    root.update_idletasks()
    assert not app.adv_frame.winfo_ismapped() and not app.adv_frame.grid_info()
    assert "2 proxies" in app.adv_summary.get() and "cookies from firefox" in app.adv_summary.get()
    app._toggle_advanced()
    assert app.adv_frame.grid_info()
    app.vars["proxy"].set("")
    app.vars["workers"].set("3")
    assert "proxies" not in app.adv_summary.get().split(":", 1)[1] and "3 parallel" in app.adv_summary.get()
    app._toggle_advanced()
    assert not app.adv_frame.grid_info()
    assert app.collect()["workers"] in ("3", 3)


def test_new_advanced_fields_round_trip(root, tmp_path):
    from yt_transcripts import gui
    from yt_transcripts.config import load_config

    cfg = tmp_path / "config.toml"
    cfg.write_text('[network]\nproxy = "http://a:1"\nproxy_for_search = false\nproxy_limit_month_mb = 2000\n'
                   'data_saver = "lean"\n', encoding="utf-8")
    app = gui.App(root, cfg)
    v = app.collect()
    assert v["proxy_for_search"] is False and v["proxy_for_transcripts"] is True
    assert v["proxy_limit_month_mb"] == 2000 and v["data_saver"] == "lean"
    summary = app.adv_summary.get()
    assert "proxies for transcripts only" in summary and "proxy data limit" in summary and "data saver lean" in summary
    app.vars["max_views"].set("50000")
    app.vars["remove_filler_words"].set(True)
    app._save()
    saved = load_config(cfg)
    assert saved["max_views"] == 50000 and saved["remove_filler_words"] is True
    assert saved["proxy_for_search"] is False


def test_channels_dialog_starts_a_channel_run(root, tmp_path, monkeypatch):
    from yt_transcripts import gui
    from yt_transcripts.config import load_config

    cfg = tmp_path / "config.toml"
    cfg.write_text('output_dir = "%s"\n' % (tmp_path / "out").as_posix(), encoding="utf-8")
    app = gui.App(root, cfg)
    started = {}
    monkeypatch.setattr(app, "_start", lambda mode, channels=None, extra=None: started.update(
        mode=mode, channels=channels, extra=extra))
    app._channels()
    win = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)][-1]

    def walk(w):
        yield w
        for c in w.winfo_children():
            yield from walk(c)
    text = next(w for w in walk(win) if isinstance(w, tk.Text))
    text.insert("1.0", "@somechannel\nhttps://www.youtube.com/playlist?list=PLabcdefghijkl")
    checks = [w for w in walk(win) if w.winfo_class() == "TCheckbutton"]
    remember = next(c for c in checks if "Remember" in c.cget("text"))
    remember.invoke()
    start = next(w for w in walk(win) if w.winfo_class() == "TButton" and w.cget("text") == "Start")
    win.grab_release()
    start.invoke()
    assert started["mode"] == "channel" and started["channels"][0] == "@somechannel"
    assert started["extra"]["channel_tabs"] == ["videos"] and started["extra"]["download_transcripts"] is True
    assert load_config(cfg)["channels"] == ["@somechannel", "https://www.youtube.com/playlist?list=PLabcdefghijkl"]


def test_summary_mentions_a_proxy_list_file(tmp_path):
    import tkinter as tk

    from yt_transcripts import gui

    try:
        root = tk.Tk()
    except tk.TclError:
        import pytest
        pytest.skip("no display")
    root.withdraw()
    cfg = tmp_path / "c.toml"
    cfg.write_text('proxy_file = "proxies.txt"\nproxy_for_search = false\n', encoding="utf-8")
    try:
        app = gui.App(root, cfg)
        summary = app.adv_summary.get()
        assert "proxy list proxies.txt" in summary and "proxies for transcripts only" in summary
        assert app.vars["proxy"].get() == ""  # the list's entries never land in the single field
    finally:
        root.destroy()
