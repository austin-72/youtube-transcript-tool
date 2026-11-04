"""Small helpers: filenames, relative-time parsing, view-count parsing, logging, retry."""

from __future__ import annotations

import datetime as dt
import logging
import random
import re
import time
import unicodedata

log = logging.getLogger("yt_transcripts")

_WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def safe_filename(name: str, max_len: int = 120) -> str:
    """Make a string safe to use as a file or folder name on Windows, macOS and Linux."""
    name = unicodedata.normalize("NFKC", name or "")
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    if not name:
        name = "untitled"
    if name.upper().split(".")[0] in _WINDOWS_RESERVED:
        name = "_" + name
    if len(name) > max_len:
        name = name[:max_len].rstrip(" .")
    return name


def slug(text: str, max_len: int = 60) -> str:
    s = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return (s[:max_len].strip("-")) or "query"


_REL_UNITS = {
    "s": 1, "sec": 1, "second": 1,
    "m": 60, "min": 60, "minute": 60,
    "h": 3600, "hr": 3600, "hour": 3600,
    "d": 86400, "day": 86400,
    "w": 7 * 86400, "wk": 7 * 86400, "week": 7 * 86400,
    "mo": 30 * 86400, "month": 30 * 86400,
    "y": 365 * 86400, "yr": 365 * 86400, "year": 365 * 86400,
}
_REL_RE = re.compile(r"(\d+)\s*([a-z]+?)s?\s+ago", re.I)


def parse_relative_time(text: str, now: dt.datetime | None = None) -> dt.datetime | None:
    """Parse '3 days ago', '2d ago', 'Streamed 15h ago', '1 month ago' -> aware datetime (UTC)."""
    if not text:
        return None
    m = _REL_RE.search(text)
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2).lower()
    secs = _REL_UNITS.get(unit)
    if secs is None:
        return None
    now = now or dt.datetime.now(dt.timezone.utc)
    return now - dt.timedelta(seconds=n * secs)


_COUNT_RE = re.compile(r"([\d.,]+)\s*([KMB]?)", re.I)


def parse_count(text: str | int | None) -> int | None:
    """'1,234,567 views' -> 1234567, '1.2M views' -> 1200000, 'No views' -> 0."""
    if text is None:
        return None
    if isinstance(text, int):
        return text
    t = str(text).strip()
    if not t:
        return None
    if t.lower().startswith("no "):
        return 0
    m = _COUNT_RE.search(t)
    if not m:
        return None
    num, suffix = m.group(1), m.group(2).upper()
    if suffix:
        num = num.replace(",", ".") if num.count(",") == 1 and "." not in num else num.replace(",", "")
        mult = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[suffix]
        try:
            return int(round(float(num) * mult))
        except ValueError:
            return None
    try:
        return int(num.replace(",", "").replace(".", ""))
    except ValueError:
        return None


def iso_utc(d: dt.datetime | None, date_only: bool = False) -> str:
    if d is None:
        return ""
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    d = d.astimezone(dt.timezone.utc)
    return d.date().isoformat() if date_only else d.replace(microsecond=0).isoformat()


def format_duration(seconds: int | float | None) -> str:
    if seconds is None:
        return ""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def format_ts(seconds: float, srt: bool = False) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    if srt:
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def polite_sleep(base: float, jitter: float = 0.5) -> None:
    """Sleep for base seconds +/- jitter fraction, to avoid hammering YouTube."""
    if base <= 0:
        return
    time.sleep(max(0.0, base * (1 + random.uniform(-jitter, jitter))))


def setup_logging(verbose: bool = False, log_file: str | None = None) -> None:
    """Console shows INFO (or DEBUG with -v); the log file always gets full detail."""
    import sys

    handlers: list[logging.Handler] = []
    if sys.stderr is not None:  # pythonw.exe has no console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG if verbose else logging.INFO)
        handlers.append(console)
    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8", mode="w")
        fh.setLevel(logging.DEBUG)
        handlers.append(fh)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s  %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
        force=True,
    )
    for noisy in ("urllib3", "requests", "charset_normalizer"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


class RunLock:
    """Exclusive lock on <folder>/run.lock held for the whole run, so a scheduled run and a manual
    run can't write the same output folder at once. The OS drops the lock if the process dies.
    (No PID probing: on Windows os.kill(pid, 0) would terminate the process.)"""

    def __init__(self, folder):
        from pathlib import Path

        self.path = Path(folder) / "run.lock"
        self.fh = None

    def acquire(self) -> bool:
        import os

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(self.path, "a+")
        try:
            if os.name == "nt":
                import msvcrt

                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.fh.close()
            self.fh = None
            return False
        return True

    def release(self) -> None:
        import os

        if not self.fh:
            return
        try:
            if os.name == "nt":
                import msvcrt

                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.fh.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass
        self.fh.close()
        self.fh = None

    def __enter__(self):
        if not self.acquire():
            raise RuntimeError(f"Another run is already using {self.path.parent} - wait for it to finish.")
        return self

    def __exit__(self, *exc):
        self.release()


_NETWORK_HINTS = (
    "unable to connect to proxy", "failed to resolve", "getaddrinfo", "name or service not known",
    "no address associated", "network is unreachable", "connection refused", "timed out",
    "temporary failure in name resolution", "connection aborted", "connection reset", "nodename nor servname",
    "winerror 10060", "winerror 10061", "winerror 10054", "winerror 10065", "winerror 11001",
    "remote end closed connection",
)


def short_error(exc: BaseException) -> str:
    """One readable line from a (often very long) yt-dlp / requests error."""
    import re

    text = re.sub(r"(://[^:/@\s]+):[^@\s]*@", r"\1:***@", str(exc).strip())  # never show proxy passwords
    line = ""
    for raw in text.splitlines():
        raw = raw.strip()
        if raw and not raw.startswith("If you are sure") and set(raw) != {"-"}:
            line = raw
            break
    if not line:
        return exc.__class__.__name__
    line = line.replace("ERROR: ", "")
    line = re.sub(r";?\s*please report this issue on.*$", "", line, flags=re.I)
    line = re.sub(r"\s*\(caused by .*$", "", line, flags=re.I)
    line = re.sub(r"^\[[\w:.-]+\]\s*", "", line).strip()
    low = text.lower()
    if "dpapi" in low or "cookie" in low and any(
            x in low for x in ("could not copy", "decrypt", "could not find", "database", "permission denied",
                               "unsupported browser")):
        return ("couldn't read your browser's cookies - on Windows Chrome/Edge lock them while open; "
                "use cookies_from_browser = \"firefox\" or leave it empty")
    if any(h in low for h in _NETWORK_HINTS) and "no connection" not in line:
        line = f"no connection to YouTube ({line[:160]})"
    return line[:300]


def replace_file(src, dst, attempts: int = 6) -> None:
    """os.replace that waits a moment when OneDrive/antivirus/Explorer briefly holds the target (Windows)."""
    import os

    for n in range(attempts):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if n == attempts - 1:
                raise
            time.sleep(0.25 * (n + 1))
