"""Shared yt-dlp setup: options for cookies, proxy, JS runtime and logging."""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path
from typing import Any

from .config import Settings

log = logging.getLogger("yt_transcripts")
PROJECT_DIR = Path(__file__).resolve().parent.parent


class YdlLogger:
    """Route yt-dlp's messages into our logger at DEBUG level and remember its warnings,
    so callers can inspect what happened during one extraction."""

    def __init__(self) -> None:
        self.warnings: list[str] = []

    def debug(self, msg: str) -> None:
        log.debug("yt-dlp: %s", msg)

    def info(self, msg: str) -> None:
        log.debug("yt-dlp: %s", msg)

    def warning(self, msg: str) -> None:
        self.warnings.append(msg)
        log.debug("yt-dlp warning: %s", msg)

    def error(self, msg: str) -> None:
        log.debug("yt-dlp error: %s", msg)


def _find_runtime(name: str) -> str | None:
    exe = name + (".exe" if os.name == "nt" else "")
    candidates = [PROJECT_DIR / "tools" / exe, PROJECT_DIR / "tools" / name / exe]
    found = shutil.which(name)
    if found:
        return found
    if os.name == "nt":  # freshly installed but not yet on this process's PATH
        local = os.environ.get("LOCALAPPDATA", "")
        home = Path.home()
        candidates += [
            Path(local) / "Microsoft" / "WinGet" / "Links" / exe,
            home / f".{name}" / "bin" / exe,  # official deno installer location
            Path(local) / "Programs" / name / exe,
        ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def js_runtime_options(settings: Settings) -> dict[str, dict[str, str]]:
    runtimes: dict[str, dict[str, str]] = {}
    for name in settings.js_runtimes:
        path = _find_runtime(name)
        if path:
            runtimes[name] = {"path": path}
    return runtimes


def parse_extractor_args(spec: str) -> tuple[str, dict[str, list[str]]]:
    """'youtube:player_client=default,-web;player_skip=webpage' -> ('youtube', {...}) - yt-dlp's CLI syntax."""
    key, sep, rest = spec.strip().partition(":")
    if not sep or not key.strip() or not rest.strip():
        raise ValueError(f"{spec!r} should look like  youtube:player_client=default,-web")
    args: dict[str, list[str]] = {}
    for part in rest.split(";"):
        if not part.strip():
            continue
        name, eq, value = part.partition("=")
        if not eq or not name.strip():
            raise ValueError(f"{part!r} in {spec!r} should look like  name=value")
        args[name.strip().replace("-", "_")] = [v.strip() for v in value.split(",")]
    return key.strip().lower(), args


def base_options(settings: Settings, *, logger: YdlLogger | None = None) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": False,
        "skip_download": True,
        "ignoreerrors": False,
        "noplaylist": True,
        "socket_timeout": 30,
        "retries": 3,
        "extractor_retries": 3,
        # NOT ignore_no_formats_error: with it, yt-dlp downgrades "rate-limited", "private video" etc.
        # to warnings and returns an empty result, which would look like "no captions".
        "extractor_args": {
            # we only need metadata + captions, so skip the streaming manifests
            # English labels always: "3 days ago" is parsed into dates, "vor 3 Tagen" is not
            "youtube": {"lang": ["en"], "skip": ["dash", "hls"]},
            "youtubetab": {"approximate_date": [""]},
        },
    }
    opts["logger"] = logger or YdlLogger()
    if settings.request_sleep > 0:
        opts["sleep_interval_requests"] = settings.request_sleep
    runtimes = js_runtime_options(settings)
    if runtimes:
        opts["js_runtimes"] = runtimes
    if settings.cookies_file:
        opts["cookiefile"] = settings.cookies_file
    elif settings.cookies_from_browser:
        opts["cookiesfrombrowser"] = (settings.cookies_from_browser.lower(),)
    if settings.proxy:
        opts["proxy"] = settings.proxy
    for spec in settings.ytdlp_extractor_args or []:  # user-supplied fixes override our defaults
        try:
            key, args = parse_extractor_args(str(spec))
        except ValueError:
            continue  # reported by validate()
        opts["extractor_args"].setdefault(key, {}).update(args)
    return opts


def patch_relative_time_parsing() -> None:
    """yt-dlp can't read YouTube's short "30m ago" labels (minutes), so the newest uploads would get
    no date and sort last. Fall back to our own parser when yt-dlp's returns nothing.
    Guarded: if yt-dlp's internals change, this silently does nothing."""
    try:
        from yt_dlp.extractor.youtube._base import YoutubeBaseInfoExtractor as Base
    except Exception:
        return
    original = getattr(Base, "_parse_time_text", None)
    if original is None or getattr(original, "_ytt_patched", False):
        return

    def _parse_time_text(self, text, report_failure=True):
        ts = original(self, text, report_failure=False)
        if ts is None and text:
            from .utils import parse_relative_time

            d = parse_relative_time(text)
            if d is not None:
                return int(d.timestamp())
        return ts

    _parse_time_text._ytt_patched = True  # type: ignore[attr-defined]
    Base._parse_time_text = _parse_time_text


STALE_DAYS = 60


def ytdlp_age_days(today=None) -> int | None:
    """How old the installed yt-dlp release is (its version is its release date, e.g. 2026.10.26)."""
    import datetime as dt

    try:
        from yt_dlp.version import __version__ as ver

        y, m, d = (int(x) for x in ver.split(".")[:3])
        return ((today or dt.date.today()) - dt.date(y, m, d)).days
    except Exception:
        return None


def warn_if_stale(log) -> None:
    age = ytdlp_age_days()
    if age is not None and age > STALE_DAYS:
        log.warning("Your yt-dlp is %d days old. YouTube changes often - double-click update.bat if searches "
                    "or transcripts fail.", age)


def make_ydl(settings: Settings, logger: YdlLogger | None = None, **extra: Any):
    import yt_dlp

    patch_relative_time_parsing()
    opts = base_options(settings, logger=logger)
    opts.update(extra)
    return yt_dlp.YoutubeDL(opts)
