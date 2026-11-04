"""A small window interface (tkinter, part of standard Python) around the same engine as the CLI."""

from __future__ import annotations

import logging
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path

from . import __version__
from .config import ConfigError, build_settings, update_config_file
from .config import load_config as _load_config_file

log = logging.getLogger("yt_transcripts")
PROJECT_DIR = Path(__file__).resolve().parent.parent

WITHIN_LABELS = {"today": "Today", "week": "This week", "month": "This month", "year": "This year", "any": "Any time"}
MISSING_LABELS = {
    "original": "Save it in the video's own language",
    "translate": "Machine-translate (else keep original)",
    "skip": "Skip the video",
}
FORMATS = ["txt", "md", "srt", "vtt", "json"]


class _QueueHandler(logging.Handler):
    def __init__(self, q: queue.Queue):
        super().__init__()
        self.q = q

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.q.put_nowait(self.format(record))
        except Exception:
            pass


def _open_path(path: Path) -> None:
    try:
        if os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception as e:  # pragma: no cover - UI convenience only
        log.error("Could not open %s: %s", path, e)


class App:
    def __init__(self, root, config_path: Path):
        import tkinter as tk
        from tkinter import ttk

        self.tk, self.ttk = tk, ttk
        self.root = root
        self.config_path = config_path
        self.q: queue.Queue = queue.Queue()
        self.worker: threading.Thread | None = None
        self.stop_event = threading.Event()
        self._running = False

        root.title(f"YouTube Transcript Tool {__version__}")
        self._setup_logging()

        cfg = self._load_config()
        s = build_settings(cfg)
        self.vars: dict[str, object] = {}
        V = self.vars

        outer = ttk.Frame(root, padding=10)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(3, weight=1)

        # ---- search options --------------------------------------------------
        sf = ttk.LabelFrame(outer, text=" 1. What to search for ", padding=8)
        sf.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        sf.columnconfigure(1, weight=1)
        ttk.Label(sf, text="Keywords\n(one per line)").grid(row=0, column=0, sticky="nw", pady=2)
        self.keywords = tk.Text(sf, height=6, width=36, wrap="none", font=("Segoe UI", 10))
        self.keywords.grid(row=0, column=1, sticky="nsew", pady=2)
        self.keywords.insert("1.0", "\n".join(s.keywords))

        r = 1
        V["min_views"] = tk.StringVar(value=str(s.min_views))
        self._row(sf, r, "Minimum views", ttk.Entry(sf, textvariable=V["min_views"], width=14)); r += 1
        V["rising_views_per_day"] = tk.StringVar(value=str(s.rising_views_per_day))
        self._row(sf, r, "…or rising: views/day (0 = off)",
                  ttk.Entry(sf, textvariable=V["rising_views_per_day"], width=14)); r += 1
        V["within"] = tk.StringVar(value=WITHIN_LABELS.get(s.within, "This month"))
        self._row(sf, r, "Uploaded", ttk.Combobox(sf, textvariable=V["within"], values=list(WITHIN_LABELS.values()),
                                                state="readonly", width=14)); r += 1
        V["max_results"] = tk.StringVar(value=str(s.max_results))
        self._row(sf, r, "Keep newest (per keyword)", ttk.Spinbox(sf, from_=0, to=1000, textvariable=V["max_results"],
                                                                 width=8)); r += 1
        V["min_duration"] = tk.StringVar(value=f"{s.min_duration / 60:g}" if s.min_duration else "0")
        self._row(sf, r, "Minimum length (minutes)", ttk.Entry(sf, textvariable=V["min_duration"], width=8)); r += 1
        V["include_shorts"] = tk.BooleanVar(value=s.include_shorts)
        ttk.Checkbutton(sf, text="Include Shorts", variable=V["include_shorts"]).grid(row=r, column=1, sticky="w"); r += 1

        # ---- transcript options ----------------------------------------------
        tf = ttk.LabelFrame(outer, text=" 2. Transcripts ", padding=8)
        tf.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        tf.columnconfigure(1, weight=1)
        r = 0
        V["download_transcripts"] = tk.BooleanVar(value=s.download_transcripts)
        ttk.Checkbutton(tf, text="Download transcripts after searching",
                        variable=V["download_transcripts"]).grid(row=r, column=0, columnspan=2, sticky="w"); r += 1
        V["languages"] = tk.StringVar(value=", ".join(s.languages))
        self._row(tf, r, "Languages (in order)", ttk.Entry(tf, textvariable=V["languages"], width=18)); r += 1
        missing = "translate" if s.translate else ("original" if s.allow_other_languages else "skip")
        V["missing"] = tk.StringVar(value=MISSING_LABELS[missing])
        self._row(tf, r, "If not available", ttk.Combobox(tf, textvariable=V["missing"], state="readonly",
                                                         values=list(MISSING_LABELS.values()), width=34)); r += 1
        fmt_frame = ttk.Frame(tf)
        for f in FORMATS:
            V[f"fmt_{f}"] = tk.BooleanVar(value=f in s.formats)
            ttk.Checkbutton(fmt_frame, text=f".{f}", variable=V[f"fmt_{f}"]).pack(side="left", padx=(0, 6))
        self._row(tf, r, "Save as", fmt_frame); r += 1
        V["txt_timestamps"] = tk.BooleanVar(value=s.txt_timestamps)
        ttk.Checkbutton(tf, text="Timestamps in .txt files", variable=V["txt_timestamps"]).grid(row=r, column=1, sticky="w"); r += 1
        V["combine"] = tk.BooleanVar(value=s.combine)
        ttk.Checkbutton(tf, text="Also make AI-ready combined files", variable=V["combine"]).grid(row=r, column=1, sticky="w"); r += 1
        V["organize_by"] = tk.StringVar(value=s.organize_by)
        self._row(tf, r, "Folders by", ttk.Combobox(tf, textvariable=V["organize_by"], state="readonly",
                                                   values=["keyword", "channel", "flat"], width=12)); r += 1
        V["output_dir"] = tk.StringVar(value=str(self._abs(s.output_dir)))
        of = ttk.Frame(tf)
        ttk.Entry(of, textvariable=V["output_dir"], width=30).pack(side="left", fill="x", expand=True)
        ttk.Button(of, text="Browse…", command=self._browse).pack(side="left", padx=(4, 0))
        self._row(tf, r, "Save to folder", of); r += 1

        # ---- advanced (hidden until asked for) -------------------------------------------
        adv_row = ttk.Frame(outer)
        adv_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        adv_row.columnconfigure(1, weight=1)
        self.adv_button = ttk.Button(adv_row, text="Advanced settings ▸", command=self._toggle_advanced)
        self.adv_button.grid(row=0, column=0, sticky="w")
        self.adv_summary = tk.StringVar(value="")
        ttk.Label(adv_row, textvariable=self.adv_summary, foreground="gray").grid(row=0, column=1, sticky="w",
                                                                                 padx=8)
        af = self.adv_frame = ttk.LabelFrame(adv_row, text=" Advanced: speed, proxies and access ", padding=8)
        af.columnconfigure(1, weight=1)
        af.columnconfigure(3, weight=1)
        r = 0
        V["scan_per_keyword"] = tk.StringVar(value=str(s.scan_per_keyword))
        self._row(af, r, "Results to scan", ttk.Spinbox(af, from_=20, to=2000, increment=10,
                                                       textvariable=V["scan_per_keyword"], width=8)); r += 1
        V["delay_seconds"] = tk.StringVar(value=str(s.delay_seconds))
        self._row(af, r, "Pause between videos (s)", ttk.Entry(af, textvariable=V["delay_seconds"], width=8)); r += 1
        V["workers"] = tk.StringVar(value=str(s.workers))
        self._row(af, r, "Parallel downloads", ttk.Combobox(af, textvariable=V["workers"], state="readonly",
                                                           values=["auto", "1", "2", "3", "4", "6", "8"],
                                                           width=6)); r += 1
        ttk.Label(af, text="auto = one per proxy; more than 1 without\nproxies gets you blocked sooner",
                  foreground="gray").grid(row=r, column=1, sticky="w"); r += 1
        r = 0
        V["proxy"] = tk.StringVar(value=" ".join([s.proxy] + [str(x) for x in s.proxies]).strip())
        self._row(af, r, "Proxy (optional)", ttk.Entry(af, textvariable=V["proxy"], width=40), col=2); r += 1
        hint = "e.g. http://user:pass@host:port - several separated by spaces are rotated"
        if s.proxy_file:
            hint += f"\nplus the proxies listed in {s.proxy_file} (config.toml)"
        ttk.Label(af, text=hint, foreground="gray").grid(row=r, column=3, sticky="w"); r += 1
        V["cookies_from_browser"] = tk.StringVar(value=s.cookies_from_browser)
        self._row(af, r, "Cookies from browser", ttk.Combobox(af, textvariable=V["cookies_from_browser"],
                                                             values=["", "firefox", "chrome", "edge", "brave"],
                                                             width=12), col=2); r += 1
        V["api_key"] = tk.StringVar(value=s.api_key)
        self._row(af, r, "YouTube API key", ttk.Entry(af, textvariable=V["api_key"], show="•", width=30),
                  col=2); r += 1
        self._advanced_open = False
        for name in ("proxy", "cookies_from_browser", "api_key", "workers", "delay_seconds", "scan_per_keyword"):
            V[name].trace_add("write", lambda *_: self._update_adv_summary())
        self._update_adv_summary()

        # ---- buttons -------------------------------------------------------------
        bf = ttk.Frame(outer, padding=(0, 8))
        bf.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.btn_run = ttk.Button(bf, text="▶  Search + download transcripts", command=lambda: self._start("run"))
        self.btn_run.pack(side="left")
        self.btn_search = ttk.Button(bf, text="Search only", command=lambda: self._start("search"))
        self.btn_search.pack(side="left", padx=4)
        self.btn_list = ttk.Button(bf, text="Transcripts for links / a list…", command=lambda: self._start("list"))
        self.btn_list.pack(side="left")
        self.btn_stop = ttk.Button(bf, text="Stop", command=self._stop, state="disabled")
        self.btn_stop.pack(side="left", padx=4)
        ttk.Button(bf, text="Open output folder", command=self._open_output).pack(side="right")
        ttk.Button(bf, text="Find in transcripts…", command=self._find).pack(side="right", padx=4)
        ttk.Button(bf, text="Open video list", command=self._open_list).pack(side="right", padx=4)
        ttk.Button(bf, text="Save settings", command=self._save).pack(side="right")

        # ---- log -----------------------------------------------------------------
        from tkinter.scrolledtext import ScrolledText

        self.logbox = ScrolledText(outer, height=14, state="disabled", wrap="word", font=("Consolas", 9))
        self.logbox.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.logbox.tag_configure("link", foreground="#1a5fb4", underline=True)
        self.logbox.tag_bind("link", "<Enter>", lambda e: self.logbox.configure(cursor="hand2"))
        self.logbox.tag_bind("link", "<Leave>", lambda e: self.logbox.configure(cursor=""))
        self.logbox.tag_bind("link", "<Button-1>", self._click_link)
        self.status = tk.StringVar(value="Ready.")
        self.phase = tk.StringVar(value="")
        sb = ttk.Frame(outer)
        sb.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        sb.columnconfigure(0, weight=1)
        ttk.Label(sb, textvariable=self.status, anchor="w").grid(row=0, column=0, sticky="ew")
        ttk.Label(sb, textvariable=self.phase, anchor="e").grid(row=0, column=1, padx=(8, 4))
        self.progress = ttk.Progressbar(sb, length=220, mode="determinate", maximum=1)
        self.progress.grid(row=0, column=2)

        root.update_idletasks()  # never let the window shrink below what the controls need
        root.minsize(max(root.winfo_reqwidth(), 900), max(root.winfo_reqheight(), 560))
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        root.after(100, self._drain_log)
        log.info("Settings loaded from %s", config_path if config_path.exists() else "defaults")
        self._log_summary(Path(V["output_dir"].get()))

    # ---- helpers -------------------------------------------------------------------
    def _row(self, parent, r, label, widget, col: int = 0):
        self.ttk.Label(parent, text=label).grid(row=r, column=col, sticky="w", pady=2,
                                                padx=(16 if col else 0, 8))
        widget.grid(row=r, column=col + 1, sticky="w", pady=2)

    def _toggle_advanced(self) -> None:
        self._advanced_open = not self._advanced_open
        if self._advanced_open:
            self.adv_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
            self.adv_button.configure(text="Advanced settings ▾")
        else:
            self.adv_frame.grid_remove()
            self.adv_button.configure(text="Advanced settings ▸")
        root = self.root
        root.update_idletasks()
        root.minsize(max(root.winfo_reqwidth(), 900), max(root.winfo_reqheight(), 560))

    def _update_adv_summary(self) -> None:
        """What's switched on in the hidden section, so nothing active is ever out of sight."""
        V = self.vars
        bits = []
        proxies = V["proxy"].get().split()
        if proxies:
            bits.append(f"{len(proxies)} prox{'y' if len(proxies) == 1 else 'ies'}")
        if V["workers"].get() not in ("auto", "1", ""):
            bits.append(f"{V['workers'].get()} parallel downloads")
        if V["cookies_from_browser"].get().strip():
            bits.append(f"cookies from {V['cookies_from_browser'].get().strip()}")
        if V["api_key"].get().strip():
            bits.append("API key set")
        self.adv_summary.set(("In use: " + ", ".join(bits)) if bits else
                             "proxies, parallel downloads, cookies, API key, pause between videos")

    def _abs(self, p: str) -> Path:
        path = Path(p).expanduser()
        return path if path.is_absolute() else PROJECT_DIR / path

    def _setup_logging(self) -> None:
        h = _QueueHandler(self.q)
        h.setFormatter(logging.Formatter("%(asctime)s  %(message)s", "%H:%M:%S"))
        h.setLevel(logging.INFO)  # the window shows INFO and up; last_run.log gets everything
        log.addHandler(h)
        log.setLevel(logging.DEBUG)
        log.propagate = False

    def _drain_log(self) -> None:
        lines = []
        try:
            while True:
                lines.append(self.q.get_nowait())
        except queue.Empty:
            pass
        finished = self._running and not (self.worker and self.worker.is_alive())
        if lines:
            self.logbox.configure(state="normal")
            start = self.logbox.index("end-1c")
            self.logbox.insert("end", "\n".join(lines) + "\n")
            self._tag_links(start)
            self.logbox.see("end")
            self.logbox.configure(state="disabled")
            self.status.set(lines[-1][10:][:140])
            self._update_progress(lines)
        if finished and self.q.empty():
            self._set_running(False)
        self.root.after(150, self._drain_log)

    def _update_progress(self, lines: list[str]) -> None:
        """Turn '[3/10] Keyword: ...' and '[12/40] OK ...' log lines into the progress bar."""
        for line in lines:
            if "Something went wrong" in line or "Stopped because of an error" in line:
                self._failed = True
            m = _PROGRESS_RE.search(line)
            if not m:
                if "Downloading transcripts for" in line:
                    self.phase.set("Transcripts")
                    self.progress.configure(maximum=1, value=0)
                continue
            i, n = int(m.group(1)), int(m.group(2))
            searching = m.group(3) == "Keyword:"
            self.phase.set(f"{'Searching keyword' if searching else 'Transcripts'} {i}/{n}")
            # a keyword's search is in progress while its line shows, so count it as half done
            self.progress.configure(maximum=n, value=(i - 0.5) if searching else i)

    @staticmethod
    def _log_summary(out: Path) -> None:
        import json

        try:
            data = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        ok = sum(1 for r in data.values() if r.get("status") == "ok")
        retry = sum(1 for r in data.values() if r.get("status") in ("error", "blocked", "po_token"))
        log.info("So far: %d transcripts saved in %s%s", ok, out,
                 f" ({retry} to retry on the next run)" if retry else "")

    def _tag_links(self, start: str) -> None:
        idx = start
        while True:
            count = self.tk.IntVar()
            pos = self.logbox.search(r"https?://\S+", idx, stopindex="end", regexp=True, count=count)
            if not pos or not count.get():
                return
            end = f"{pos}+{count.get()}c"
            self.logbox.tag_add("link", pos, end)
            idx = end

    def _click_link(self, event) -> None:
        import webbrowser

        idx = self.logbox.index(f"@{event.x},{event.y}")
        rng = self.logbox.tag_prevrange("link", idx + "+1c")
        if rng:
            webbrowser.open(self.logbox.get(*rng))

    def _find(self) -> None:
        from tkinter import simpledialog

        if self.worker and self.worker.is_alive():
            return
        phrase = simpledialog.askstring("Find in transcripts", "Word or phrase to look for:", parent=self.root)
        if not phrase or not phrase.strip():
            return
        try:
            values = self.collect()
        except ValueError:
            values = {}
        s = build_settings(self._load_config(), {"output_dir": values.get("output_dir")})
        s.output_dir = str(self._abs(s.output_dir))
        self.stop_event.clear()
        self._set_running(True)

        def job():
            from . import cli

            try:
                def out(*parts):
                    for line in " ".join(str(x) for x in parts).splitlines():
                        if line.strip():
                            log.info(line)

                cli.cmd_find(s, phrase.strip(), out=out)
            except Exception as e:
                log.error("Search failed: %s", e)

        self.worker = threading.Thread(target=job, daemon=True)
        self.worker.start()

    def _load_config(self) -> dict:
        """Read config.toml; a broken file is reported (not a crash) and the defaults are used."""
        try:
            cfg = _load_config_file(self.config_path)
            self._config_error = ""
            return cfg
        except ConfigError as e:
            self._config_error = str(e)
            if not getattr(self, "_config_error_shown", False):
                self._config_error_shown = True
                show_startup_error(f"{e}\n\nThe window will use default settings until the file is fixed.",
                                   parent=self.root)
            return {}

    def collect(self) -> dict:
        V = self.vars

        def num(key, cast=int, default=0):
            try:
                return cast(str(V[key].get()).replace(",", "").strip() or default)
            except ValueError:
                raise ValueError(f"'{key.replace('_', ' ')}' must be a number") from None

        within = {v: k for k, v in WITHIN_LABELS.items()}.get(V["within"].get(), "month")
        missing = {v: k for k, v in MISSING_LABELS.items()}.get(V["missing"].get(), "original")
        formats = [f for f in FORMATS if V[f"fmt_{f}"].get()] or ["txt"]
        return {
            "keywords": [k.strip() for k in self.keywords.get("1.0", "end").splitlines() if k.strip()],
            "min_views": num("min_views"),
            "rising_views_per_day": num("rising_views_per_day"),
            "within": within,
            "max_results": num("max_results"),
            "scan_per_keyword": num("scan_per_keyword"),
            "min_duration": int(round(num("min_duration", float) * 60)),
            "include_shorts": bool(V["include_shorts"].get()),
            "api_key": V["api_key"].get().strip(),
            "download_transcripts": bool(V["download_transcripts"].get()),
            "languages": [x.strip() for x in V["languages"].get().split(",") if x.strip()] or ["en"],
            # translating falls back to the original language when YouTube offers no translation
            "allow_other_languages": missing in ("original", "translate"),
            "translate": missing == "translate",
            "formats": formats,
            "txt_timestamps": bool(V["txt_timestamps"].get()),
            "combine": bool(V["combine"].get()),
            "organize_by": V["organize_by"].get(),
            "output_dir": V["output_dir"].get().strip() or "output",
            "delay_seconds": num("delay_seconds", float, 5.0),
            "cookies_from_browser": V["cookies_from_browser"].get().strip(),
            "proxy": " ".join(V["proxy"].get().split()),
            "proxies": [],  # the field above holds the whole list
            "workers": V["workers"].get().strip() or "auto",
        }

    # ---- actions -------------------------------------------------------------------------
    def _browse(self):
        from tkinter import filedialog

        d = filedialog.askdirectory(initialdir=self.vars["output_dir"].get() or str(PROJECT_DIR))
        if d:
            self.vars["output_dir"].set(d)

    def _save(self):
        from tkinter import messagebox

        try:
            values = self.collect()
        except ValueError as e:
            messagebox.showerror("Check your settings", str(e))
            return
        self._load_config()  # re-check: the file may have been fixed (or broken) in Notepad meanwhile
        if getattr(self, "_config_error", ""):
            messagebox.showerror(
                "Fix config.toml first",
                f"{self._config_error}\n\nThe window is showing default values, so saving now would overwrite "
                "your own settings. Fix the line above in Notepad, then close and reopen this window.")
            return
        out = self._abs(str(values.get("output_dir") or "output"))
        try:  # keep the folder relative to the tool, so moving the tool folder keeps working
            values["output_dir"] = os.path.relpath(out, PROJECT_DIR) if out.resolve().is_relative_to(
                PROJECT_DIR.resolve()) else str(out)
        except (OSError, ValueError):
            pass
        try:
            if not self.config_path.exists():
                example = PROJECT_DIR / "config.example.toml"
                if example.exists():
                    self.config_path.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
            update_config_file(self.config_path, values)
        except (ConfigError, OSError) as e:
            messagebox.showerror("Settings not saved", str(e))
            return
        log.info("Settings saved to %s (run.bat uses them too).", self.config_path)

    def _start(self, mode: str):
        from tkinter import filedialog, messagebox

        if self.worker and self.worker.is_alive():
            return
        try:
            values = self.collect()
        except ValueError as e:
            messagebox.showerror("Check your settings", str(e))
            return
        list_file = None
        if mode == "list":
            from tkinter import simpledialog

            links = simpledialog.askstring(
                "Transcripts for links / a list",
                "Paste one or more YouTube links (separated by spaces),\n"
                "or leave this empty and press OK to choose a list file:", parent=self.root)
            if links is None:  # Cancel
                return
            from .writers import _extract_id

            if links.strip():
                bad = [x for x in links.split() if not _extract_id(x)]
                if bad:
                    messagebox.showerror("Not a YouTube link", f"This doesn't look like a YouTube link:\n{bad[0]}")
                    return
                list_file = links.strip()
        if mode == "list" and not list_file:
            list_file = filedialog.askopenfilename(
                title="Choose a video list (CSV/JSON from this tool, or a .txt of YouTube links)",
                initialdir=values["output_dir"],
                filetypes=[("Video lists", "*.csv *.json *.txt"), ("All files", "*.*")])
            if not list_file:
                return
        elif mode != "list" and not build_settings(self._load_config(), values).all_keywords() \
                and not self._load_config().get("keywords_file"):
            messagebox.showwarning("No keywords", "Type at least one keyword (one per line).")
            return
        if mode == "search":
            values["download_transcripts"] = False

        cfg = self._load_config()
        kw_file = cfg.pop("keywords_file", None)
        s = build_settings(cfg, values)
        try:
            from .proxies import resolve as resolve_proxies

            resolve_proxies(s, PROJECT_DIR)
        except ConfigError as e:
            messagebox.showerror("Proxy", str(e))
            return
        if kw_file and mode != "list":  # same as run.bat: the file's keywords are added to the typed ones
            from .config import read_keywords_file

            try:
                extra = read_keywords_file(self._abs(str(kw_file)))
            except ConfigError as e:
                messagebox.showerror("Keywords file", str(e))
                return
            s.keywords = list(s.keywords) + extra
            log.info("Also searching %d keyword(s) from %s.", len(extra), kw_file)
        s.output_dir = str(self._abs(s.output_dir))
        try:
            Path(s.output_dir).mkdir(parents=True, exist_ok=True)
            # delay=True: the file is only opened (and emptied) once this run holds the folder lock
            fh = logging.FileHandler(Path(s.output_dir) / "last_run.log", encoding="utf-8", mode="w", delay=True)
        except OSError as e:
            messagebox.showerror("Output folder", f"Can't use the folder {s.output_dir}:\n{e.strerror or e}\n\n"
                                 "Is the drive connected? Pick another folder under 'Save to folder'.")
            return
        fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s %(message)s", "%H:%M:%S"))

        self.stop_event.clear()
        self._set_running(True)

        def job():
            from . import cli
            from .utils import RunLock

            cli.LIST_PRINTER = log.info
            lock = RunLock(s.output_dir)
            try:
                if not lock.acquire():
                    log.error("Another run (maybe the daily scheduled one) is using this output folder - "
                              "try again when it has finished.")
                    return
                log.addHandler(fh)
                cli.cmd_run(s, transcripts_only_list=list_file, should_stop=self.stop_event.is_set)
            except Exception as e:  # show any failure in the window instead of crashing
                from .utils import short_error

                log.debug("Unexpected error", exc_info=True)  # full details go to last_run.log only
                log.error("Something went wrong: %s", short_error(e))
                log.error("Details are in %s", Path(s.output_dir) / "last_run.log")
            finally:
                lock.release()
                log.removeHandler(fh)
                fh.close()
                # no Tk calls from this thread: the main loop notices the worker ending (_drain_log)

        self.worker = threading.Thread(target=job, daemon=True)
        self.worker.start()

    def _stop(self):
        self.stop_event.set()
        log.warning("Stopping after the current video…")

    def _set_running(self, running: bool):
        self._running = running
        state = "disabled" if running else "normal"
        for b in (self.btn_run, self.btn_search, self.btn_list):
            b.configure(state=state)
        self.btn_stop.configure(state="normal" if running else "disabled")
        if running:
            self._failed = False
            self.phase.set("Starting")
            self.progress.configure(maximum=1, value=0)
        else:
            self.status.set("Ready.")
            if getattr(self, "_failed", False):
                self.phase.set("Failed - see the log")
            elif self.stop_event.is_set():
                self.phase.set("Stopped")
            elif self.phase.get() not in ("", "Starting"):
                self.phase.set("Finished")
                self.progress.configure(value=float(self.progress["maximum"]))
            else:
                self.phase.set("")

    def _open_output(self):
        p = self._abs(self.vars["output_dir"].get() or "output")
        p.mkdir(parents=True, exist_ok=True)
        _open_path(p)

    def _open_list(self):
        p = self._abs(self.vars["output_dir"].get() or "output")
        for name in ("video_list.html", "video_list.csv"):
            if (p / name).exists():
                _open_path(p / name)
                return
        log.info("No video list yet - run a search first.")

    def _on_close(self):
        if self.worker and self.worker.is_alive():
            self.stop_event.set()
        self.root.destroy()


# "23:10:01  [2/5] Keyword: 'x'" or "23:10:30  [7/18] OK    title" - only at the start of a log line
_PROGRESS_RE = __import__("re").compile(r"^\S+\s+\[(\d+)/(\d+)\] (Keyword:|OK |skip |NONE |UNAV |BLOCK |FAIL |TOKEN)")


def show_startup_error(message: str, parent=None) -> None:
    """Show an error in a message box - gui.bat runs without a console, so print() would be invisible."""
    try:
        import tkinter as tk
        from tkinter import messagebox

        owner = parent
        if owner is None:
            owner = tk.Tk()
            owner.withdraw()
        messagebox.showerror("YouTube Transcript Tool", message, parent=owner)
        if parent is None:
            owner.destroy()
    except Exception:
        pass


def launch(config: str | None = None) -> int:
    try:
        import tkinter as tk
    except ImportError:
        print("tkinter is not available in this Python installation; use run.bat / the command line instead.")
        return 1
    if os.name == "nt":
        try:  # crisp text on high-DPI screens
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    root = tk.Tk()
    try:
        from tkinter import ttk

        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    cfg = Path(config) if config else PROJECT_DIR / "config.toml"
    App(root, cfg)
    root.mainloop()
    return 0
