"""`yt.py doctor` - check the installation and that YouTube is reachable. `yt.py init` - create config."""

from __future__ import annotations

import importlib.metadata as md
import shutil
import subprocess
import sys
from pathlib import Path

from .config import Settings


def _ok(msg: str) -> None:
    print(f"  [ OK ] {msg}")


MIN_RUNTIME = {"deno": (2, 3, 0), "node": (22, 0, 0)}  # yt-dlp's EJS wiki, 2026


def _runtime_too_old(name: str, version_text: str) -> str:
    """'2.3.0' if this runtime is older than yt-dlp supports, else ''."""
    import re

    need = MIN_RUNTIME.get(name)
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", version_text or "")
    if not need or not m:
        return ""
    have = tuple(int(x or 0) for x in m.groups())
    return ".".join(map(str, need)) if have < need else ""


def _warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


_MODULES = {"yt-dlp": ("yt_dlp.version", "__version__"), "youtube-transcript-api": ("youtube_transcript_api", ""),
            "yt-dlp-ejs": ("yt_dlp_ejs", "version"), "requests": ("requests", "__version__")}


def _version(pkg: str) -> str | None:
    try:
        return md.version(pkg)
    except md.PackageNotFoundError:
        pass
    # the one-file .exe carries the modules without their package records: ask the module itself
    mod, attr = _MODULES.get(pkg, (pkg.replace("-", "_"), "__version__"))
    try:
        import importlib

        m = importlib.import_module(mod)
    except Exception:
        return None
    return str(getattr(m, attr, "") or getattr(m, "__version__", "") or "bundled")


def run_doctor(s: Settings, test_video: str = "dQw4w9WgXcQ") -> int:
    failures = 0
    print("\nChecking your setup\n")

    v = sys.version_info
    (_ok if v >= (3, 11) else _fail)(f"Python {v.major}.{v.minor}.{v.micro} ({sys.executable})"
                                     + ("" if v >= (3, 11) else "  -> yt-dlp needs Python 3.11 or newer"))
    failures += v < (3, 11)

    for pkg, need in (("yt-dlp", True), ("youtube-transcript-api", True), ("yt-dlp-ejs", False), ("requests", True)):
        ver = _version(pkg)
        if ver and pkg == "yt-dlp":
            from .ytdlp_common import STALE_DAYS, ytdlp_age_days

            age = ytdlp_age_days()
            if age is not None and age > STALE_DAYS:
                _warn(f"yt-dlp {ver} is {age} days old - run update.bat (YouTube changes often)")
            else:
                _ok(f"{pkg} {ver}")
        elif ver:
            _ok(f"{pkg} {ver}")
        elif need:
            _fail(f"{pkg} is not installed  ->  run setup.bat  (or: pip install -r requirements.txt)")
            failures += 1
        else:
            _warn(f"{pkg} not installed (pip install \"yt-dlp[default]\") - yt-dlp may miss some videos")

    from .ytdlp_common import js_runtime_options

    runtimes = js_runtime_options(s)
    if runtimes:
        for name, cfg in runtimes.items():
            ver = ""
            try:
                out = subprocess.run([cfg["path"], "--version"], capture_output=True, text=True, timeout=20)
                ver = (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else ""
            except Exception:
                pass
            too_old = _runtime_too_old(name, ver)
            if too_old:
                _warn(f"JavaScript runtime {name} {ver} is too old - yt-dlp needs {too_old} or newer. "
                      "Update it:  winget upgrade DenoLand.Deno  (or run setup.bat)")
            else:
                _ok(f"JavaScript runtime for yt-dlp: {name} {ver} ({cfg['path']})")
    else:
        _warn("No JavaScript runtime (Deno) found. yt-dlp needs one for YouTube (only a reduced fallback "
              "works without it). Install with:  winget install DenoLand.Deno  - or run setup.bat again.")

    if s.resolved_api_key():
        _ok("YouTube Data API key configured (search backend: api)")
    else:
        _ok("No API key - using key-less yt-dlp search (that's fine)")

    if s.cookies_file and not Path(s.cookies_file).exists():
        _fail(f"cookies_file {s.cookies_file} does not exist")
        failures += 1

    for pr in s.validate():
        if "proxy" in pr.lower():
            _fail(pr)
            failures += 1

    print("\nChecking YouTube connectivity\n")
    from .proxies import mask
    from .utils import short_error

    proxies = list(s.proxies or ([s.proxy] if s.proxy else []))
    working = []
    for px in proxies[:10] or [""]:
        label = f"through proxy {mask(px)}" if px else "directly"
        try:
            import requests

            r = requests.get("https://www.youtube.com/", timeout=15,
                             proxies={"https": px, "http": px} if px else None)
            if r.status_code == 200:
                _ok(f"youtube.com reachable {label}")
                working.append(px)
            else:
                _warn(f"youtube.com answered HTTP {r.status_code} {label}")
        except Exception as e:
            msg = short_error(e)[:200]
            if "socks" in msg.lower() and "missing dependencies" in msg.lower():
                msg = "SOCKS proxies need PySocks - run update.bat"
            _fail(f"cannot reach youtube.com {label}: {msg}")
    if len(proxies) > 10:
        print(f"         ({len(proxies) - 10} more proxies not tested)")
    if not working:
        hint = "check the proxy address, user name and password" if proxies else "check your internet connection"
        _fail(f"YouTube is not reachable - {hint}")
        return failures + 1
    if proxies and working[0] != s.proxy:
        s.proxy = working[0]  # test search below through a proxy that works

    # search
    try:
        import copy

        from .search_ytdlp import search_keyword

        ts = copy.copy(s)
        if not s.proxy_for_search:
            ts.proxy = ""
            print("         (searching over your own connection: proxy_for_search = false)")
        ts.sorts, ts.scan_per_keyword, ts.include_shorts, ts.within = ["relevance"], 5, False, "year"
        ts.cascade_windows = False
        res = search_keyword("python tutorial", ts)
        if res:
            ex = res[0]
            _ok(f"key-less search works ({len(res)} results, e.g. {ex.title[:50]!r}, "
                f"{ex.views if ex.views is not None else '?'} views, published ~{ex.published[:10] or '?'})")
        else:
            _fail("key-less search returned no results")
            failures += 1
    except Exception as e:
        _fail(f"key-less search failed: {e}")
        failures += 1

    if s.resolved_api_key():
        try:
            from .search_api import YouTubeApi

            api = YouTubeApi(s.resolved_api_key(), proxy=s.proxy)
            ids = api.search_ids("python", "date", None, 1)
            _ok(f"YouTube Data API works (got {len(ids)} result)")
        except Exception as e:
            _fail(f"YouTube Data API failed: {e}")
            failures += 1

    # transcripts
    from .models import Video
    from .pipeline import build_fetchers
    from .transcripts import FetchError

    import copy as _copy

    from . import netmeter
    from .transcripts import saver_profile

    ts = _copy.copy(s)
    ts.allow_other_languages = True
    upstream = s.proxy if s.proxy_for_transcripts else ""
    video = Video(video_id=test_video, title="test video")
    any_ok = False
    with netmeter.Session(ts, "doctor") as sess:
        for name in ts.transcript_methods:
            ts1 = _copy.copy(ts)
            ts1.transcript_methods = [name]
            ts1.proxy = netmeter.route(upstream)
            before = sess.meter.total
            for f in build_fetchers(ts1):
                try:
                    t = f.fetch(video)
                    any_ok = True
                    used = sess.meter.total - before
                    data = ""
                    if upstream and sess.enabled:
                        mode = saver_profile(ts1) if f.name == "ytdlp" else ""
                        data = f"; used {netmeter.fmt_bytes(used)} of proxy data" + (
                            f" (data saver: {mode})" if mode else "")
                    _ok(f"transcript via {f.name}: {len(t.segments)} lines, language {t.language} "
                        f"({t.kind}){data}")
                except FetchError as e:
                    (_warn if f.name == "api" else _fail)(f"transcript via {f.name}: {e.status} - {e}")
                finally:
                    if hasattr(f, "close"):
                        f.close()
    if not any_ok:
        failures += 1
        print("\n  No method could download the test transcript. If the error mentions a bot check,\n"
              "  try again later, or set cookies_from_browser = \"firefox\" in config.toml.")

    print("\n" + ("All good - you're ready to go." if failures == 0 else f"{failures} problem(s) found."))
    return 1 if failures else 0


def init_config(project_dir: Path) -> int:
    from .paths import resource

    target = project_dir / "config.toml"
    example = project_dir / "config.example.toml"
    if not example.exists():
        example = resource("config.example.toml")
    if target.exists():
        print(f"{target} already exists - not overwriting.")
        return 0
    if not example.exists():
        print("config.example.toml is missing.")
        return 1
    shutil.copyfile(example, target)
    print(f"Created {target}. Open it in Notepad to set your keywords and view threshold.")
    return 0
