"""Settings: defaults, loading from config.toml, and validation."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any

try:  # Python 3.11+
    import tomllib as _toml
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    try:
        import tomli as _toml  # type: ignore
    except ModuleNotFoundError:
        _toml = None  # type: ignore

WINDOW_DAYS = {"today": 1, "day": 1, "week": 7, "month": 31, "year": 366}
VALID_FORMATS = {"txt", "md", "srt", "vtt", "json"}
AUTO_WORKER_CAP = 4  # each worker runs its own YouTube JavaScript solver (Deno): keep laptops responsive

KEYWORD_OVERRIDABLE = {
    "min_views", "rising_views_per_day", "within", "max_age_days", "max_results", "scan_per_keyword", "sorts", "include_shorts",
    "cascade_windows",
    "min_duration", "max_duration", "exclude_live", "subtitles_only", "title_must_contain", "exclude_words",
    "exclude_channels", "only_channels", "drop_reuploads",
}


@dataclass
class Settings:
    # --- what to search -------------------------------------------------
    keywords: list[str] = field(default_factory=list)
    min_views: int = 10_000
    rising_views_per_day: int = 0  # also keep videos below min_views that gain at least this many views/day (0 = off)
    within: str = "month"  # today | week | month | year | any
    max_age_days: float | None = None  # finer cut-off than `within` (optional)
    max_results: int = 25  # newest N videos kept per keyword (0 = no limit)
    scan_per_keyword: int = 150  # search results scanned per keyword & sort order
    sorts: list[str] = field(default_factory=lambda: ["popularity", "relevance"])
    cascade_windows: bool = True  # also scan the narrower windows (today, week...) so fresh uploads aren't crowded out
    backend: str = "auto"  # auto | ytdlp | api
    api_key: str = ""
    include_shorts: bool = False
    min_duration: int = 0  # seconds
    max_duration: int = 0  # seconds, 0 = no maximum
    drop_reuploads: bool = True  # skip copies of the same video re-uploaded by another channel
    exclude_live: bool = True
    subtitles_only: bool = False  # YouTube's "Subtitles/CC" filter (uploaded captions only)
    exact_dates: bool = False  # look up exact upload date per video (slower, ytdlp backend)
    title_must_contain: list[str] = field(default_factory=list)
    exclude_words: list[str] = field(default_factory=list)
    exclude_channels: list[str] = field(default_factory=list)
    only_channels: list[str] = field(default_factory=list)  # if set, keep only these channels
    search_language: str = ""  # API search only: prefer results in this language, e.g. "en" ("" = no preference)
    keyword_settings: list[dict] = field(default_factory=list)  # per-keyword overrides

    # --- transcripts ------------------------------------------------------
    download_transcripts: bool = True
    languages: list[str] = field(default_factory=lambda: ["en"])
    allow_other_languages: bool = True  # fall back to the video's own language
    translate: bool = False  # prefer YouTube's machine translation into `languages[0]` over the original
    prefer_manual: bool = True  # human-made captions before auto-generated
    # yt-dlp first: it copes with YouTube's caption PO-token check by using other player clients;
    # youtube-transcript-api is a lighter fallback (and costs 2 extra requests when it fails)
    transcript_methods: list[str] = field(default_factory=lambda: ["ytdlp", "api"])
    formats: list[str] = field(default_factory=lambda: ["txt", "json"])
    txt_timestamps: bool = False
    strip_sound_tags: bool = False  # remove [Music], [Applause], (laughs) ... from the text
    paragraph_seconds: int = 30  # group plain-text output into paragraphs of ~N seconds
    combine: bool = True  # also write AI-ready combined Markdown files (one per keyword per run)
    combine_max_words: int = 80000  # split combined files into parts of at most this many words (0 = never)
    retry_failed: bool = False
    max_transcripts_per_run: int = 0  # 0 = no limit; the rest are fetched on the next run

    # --- output -----------------------------------------------------------
    output_dir: str = "output"
    organize_by: str = "keyword"  # keyword | channel | flat
    open_list_when_done: bool = False  # open video_list.html in the browser after a run

    # --- networking -------------------------------------------------------
    delay_seconds: float = 5.0  # between videos (randomised +/-50%)
    request_sleep: float = 0.75  # between yt-dlp's own requests (its recommended "sleep" preset value)
    max_consecutive_blocks: int = 4
    cookies_file: str = ""
    cookies_from_browser: str = ""  # firefox | chrome | edge | brave ...
    proxy: str = ""  # one proxy (or several separated by spaces); see also proxies / proxy_file
    proxies: list[str] = field(default_factory=list)  # rotated: the next one is used when YouTube blocks one
    proxy_file: str = ""
    # parallel downloads: "auto" = one worker per proxy (one in total without proxies)
    workers: str | int = "auto"
    workers_per_proxy: int = 1  # >1 only makes sense for rotating proxy services (a new IP per connection)
    proxy_rotating: str | bool = "auto"  # "auto" recognises e.g. Webshare's "-rotate" users and known gateways
    # yt-dlp --extractor-args, for fixes from the yt-dlp wiki/issues, e.g. ["youtube:player_client=default,-web"]
    ytdlp_extractor_args: list[str] = field(default_factory=list)
    videos_per_hour_per_ip: int = 200  # YouTube allows guests ~300 videos/h per IP; 0 = no cap
    js_runtimes: list[str] = field(default_factory=lambda: ["deno", "node"])

    verbose: bool = False

    # ---------------------------------------------------------------------
    def all_keywords(self) -> list[str]:
        """Keywords from `keywords` plus any that only appear in [[keyword_settings]]."""
        out = list(self.keywords)
        known = {k.lower() for k in out}
        for d in self.keyword_settings or []:
            kw = str(d.get("keyword", "")).strip() if isinstance(d, dict) else ""
            if kw and kw.lower() not in known:
                out.append(kw)
                known.add(kw.lower())
        return out

    def for_keyword(self, keyword: str) -> "Settings":
        """A copy of these settings with that keyword's [[keyword_settings]] overrides applied."""
        import copy

        for d in self.keyword_settings or []:
            if isinstance(d, dict) and str(d.get("keyword", "")).strip().lower() == keyword.lower():
                s = copy.copy(self)
                for k, v in d.items():
                    if k == "keyword":
                        continue
                    if k in KEYWORD_OVERRIDABLE:
                        v = _coerce(k, v, [])
                        if k == "within" and isinstance(v, str):
                            v = v.strip().lower()
                        elif k == "sorts" and isinstance(v, list):
                            v = [str(x).strip().lower() for x in v]
                        setattr(s, k, v)
                    else:
                        import logging

                        logging.getLogger("yt_transcripts").warning(
                            "keyword_settings for %r: %r can't be set per keyword (ignored)", keyword, k)
                return s
        return self

    def resolved_workers(self) -> int:
        """How many downloads run at once. Cookies force 1: one account seen from several IPs at once
        risks a ban, and yt-dlp would rewrite the cookie file from several places."""
        if self.cookies_file or self.cookies_from_browser:
            return 1
        n_proxies = len(self.proxies or ([self.proxy] if self.proxy else []))
        w = str(self.workers).strip().lower()
        if w == "auto":
            return min(n_proxies * max(1, int(self.workers_per_proxy or 1)), AUTO_WORKER_CAP) if n_proxies else 1
        try:
            return max(1, min(int(w), 16))
        except ValueError:
            return 1

    def resolved_api_key(self) -> str:
        return self.api_key or os.environ.get("YOUTUBE_API_KEY", "")

    def resolved_backend(self) -> str:
        if self.backend == "auto":
            return "api" if self.resolved_api_key() else "ytdlp"
        return self.backend

    def effective_max_age_days(self) -> float | None:
        days = WINDOW_DAYS.get(self.within)
        if self.max_age_days:
            return min(self.max_age_days, days) if days else self.max_age_days
        return days

    def validate(self) -> list[str]:
        problems = []
        if not self.all_keywords():
            problems.append("No keywords given (use --keyword or the `keywords` list in config.toml).")
        if self.within not in (*WINDOW_DAYS, "any"):
            problems.append(f"within must be one of {', '.join([*WINDOW_DAYS, 'any'])} (got {self.within!r}).")
        if self.backend not in ("auto", "ytdlp", "api"):
            problems.append(f"backend must be auto, ytdlp or api (got {self.backend!r}).")
        if self.resolved_backend() == "api" and not self.resolved_api_key():
            problems.append("backend=api needs an API key (api_key in config.toml or YOUTUBE_API_KEY env var).")
        if not self.formats:
            problems.append(f"formats is empty - pick at least one of {sorted(VALID_FORMATS)}, e.g. formats = [\"txt\"].")
        bad = set(self.formats) - VALID_FORMATS
        if bad:
            problems.append(f"Unknown transcript format(s) {sorted(bad)}; valid: {sorted(VALID_FORMATS)}.")
        bad_m = set(self.transcript_methods) - {"api", "ytdlp"}
        if not self.transcript_methods:
            problems.append('transcript_methods is empty - use ["ytdlp", "api"].')
        if bad_m:
            problems.append(f"Unknown transcript method(s) {sorted(bad_m)}; valid: api, ytdlp.")
        if self.organize_by not in ("keyword", "channel", "flat"):
            problems.append("organize_by must be keyword, channel or flat.")
        bad_s = set(self.sorts) - {"popularity", "relevance", "views"}
        if bad_s or not self.sorts:
            problems.append("sorts must be a non-empty list of: popularity, relevance.")
        if self.min_views < 0:
            problems.append("min_views cannot be negative.")
        from .proxies import normalize, problem, split_entries

        for raw in split_entries(self.proxy) + list(self.proxies or []):
            msg = problem(normalize(str(raw)))
            if msg:
                problems.append(msg[0].upper() + msg[1:] + ".")
        w = str(self.workers).strip().lower()
        if w != "auto" and not (w.isdigit() and 1 <= int(w) <= 16):
            problems.append(f'workers must be "auto" or a number from 1 to 16 (got {self.workers!r}).')
        if not 1 <= int(self.workers_per_proxy or 0) <= 10:
            problems.append("workers_per_proxy must be between 1 and 10.")
        if str(self.proxy_rotating).lower() not in ("auto", "true", "false"):
            problems.append('proxy_rotating must be "auto", true or false.')
        from .ytdlp_common import parse_extractor_args

        for spec in self.ytdlp_extractor_args or []:
            try:
                parse_extractor_args(str(spec))
            except ValueError as e:
                problems.append(f"ytdlp_extractor_args: {e}")
        if self.combine_max_words < 0:
            problems.append("combine_max_words cannot be negative (0 = never split the combined files).")
        if self.videos_per_hour_per_ip < 0:
            problems.append("videos_per_hour_per_ip cannot be negative (0 = no hourly cap).")
        if self.scan_per_keyword < 1:
            problems.append("scan_per_keyword must be at least 1 (150 is a good start).")
        if self.rising_views_per_day < 0:
            problems.append("rising_views_per_day cannot be negative.")
        for d in self.keyword_settings or []:
            if not isinstance(d, dict) or not str(d.get("keyword", "")).strip():
                problems.append("Every [[keyword_settings]] block needs a keyword = \"...\" line.")
                continue
            ks = self.for_keyword(str(d["keyword"]).strip())
            if ks.within not in (*WINDOW_DAYS, "any"):
                problems.append(f"[[keyword_settings]] for {d['keyword']!r}: within must be one of "
                                f"{', '.join([*WINDOW_DAYS, 'any'])} (got {ks.within!r}).")
            if ks.rising_views_per_day < 0 or ks.min_views < 0:
                problems.append(f"[[keyword_settings]] for {d['keyword']!r}: min_views / rising_views_per_day "
                                "cannot be negative.")
            bad = set(ks.sorts) - {"popularity", "relevance", "views"}
            if bad:
                problems.append(f"[[keyword_settings]] for {d['keyword']!r}: unknown sorts {sorted(bad)}.")
        return problems


class ConfigError(Exception):
    """A config/keywords file that can't be read - shown to the user as a plain message."""


def read_text_any(p: Path) -> str:
    """Read a text file saved by Notepad/Excel: UTF-8 (with or without BOM), falling back to Windows ANSI."""
    try:
        data = p.read_bytes()
    except OSError as e:
        raise ConfigError(f"Could not read {p}: {e.strerror or e}") from None
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):  # Notepad "Unicode"
        return data.decode("utf-16", errors="replace")
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:  # Notepad "ANSI"
        pass
    import locale

    try:  # Windows "ANSI" code page (cp1252 in Western Europe/US, others elsewhere)
        enc = locale.getencoding() if hasattr(locale, "getencoding") else locale.getpreferredencoding(False)
        return data.decode(enc or "cp1252")
    except (LookupError, UnicodeDecodeError):
        return data.decode("cp1252", errors="replace")


def load_config(path: str | os.PathLike | None) -> dict[str, Any]:
    """Read a TOML config file into a flat dict (sections are merged)."""
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    if _toml is None:
        raise RuntimeError("Reading config.toml needs Python 3.11+ or `pip install tomli`.")
    text = read_text_any(p)
    try:
        raw = _toml.loads(text)
    except _toml.TOMLDecodeError as e:
        msg = str(e)
        hint = ""
        import re

        m = re.search(r"line (\d+)", msg)
        bad_line = text.splitlines()[int(m.group(1)) - 1] if m and 0 < int(m.group(1)) <= len(text.splitlines()) else ""
        if re.search(r"=\s*\d{1,3}(,\d{3})+\s*(#.*)?$", bad_line):
            hint = "\n  Tip: write numbers without commas, e.g.  min_views = 10000  (or 10_000)."
        elif "escape" in msg.lower() or "hex" in msg.lower() or "unicode" in msg.lower():
            hint = ("\n  Tip: Windows paths need single quotes, e.g.  output_dir = 'C:\\Users\\you\\Documents'"
                    "  (or use forward slashes).")
        elif "quote" in msg.lower() or "invalid value" in msg.lower() or "expected" in msg.lower():
            hint = "\n  Tip: text values need quotes, e.g.  within = \"week\"  and lists look like  [\"a\", \"b\"]."
        raise ConfigError(f"{p.name} has a mistake: {msg}{hint}") from None
    flat: dict[str, Any] = {}
    for k, v in raw.items():
        if isinstance(v, dict):  # [search], [transcripts], [output], [network] sections
            flat.update(v)
        else:
            flat[k] = v
    return flat


_DEFAULTS = Settings()


def _coerce(name: str, value: Any, problems: list[str]) -> Any:
    """Turn hand-written config values into the type the setting expects."""
    default = getattr(_DEFAULTS, name)
    try:
        if isinstance(default, bool):
            if isinstance(value, str):
                low = value.strip().lower()
                if low in ("true", "yes", "on", "1"):
                    return True
                if low in ("false", "no", "off", "0", ""):
                    return False
                raise ValueError
            return bool(value)
        if isinstance(default, int) and not isinstance(default, bool):
            if isinstance(value, str):
                value = value.replace(",", "").replace("_", "").strip()
            return int(float(value))
        if isinstance(default, float) or name == "max_age_days":
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    return None if name == "max_age_days" else default
            return float(value)
        if isinstance(default, list) and name != "keyword_settings":
            if isinstance(value, str):
                return [x.strip() for x in value.split(",") if x.strip()]
            return [str(x) for x in value]
        if isinstance(default, str):
            return str(value)
    except (TypeError, ValueError):
        problems.append(f"Setting {name} = {value!r} doesn't look right (expected {type(default).__name__}); "
                        f"using the default {default!r}.")
        return default
    return value


def build_settings(config: dict[str, Any] | None = None, overrides: dict[str, Any] | None = None) -> Settings:
    """Defaults <- config file <- command-line overrides (ignoring None values)."""
    known = {f.name for f in fields(Settings)}
    merged: dict[str, Any] = {}
    unknown = []
    coerce_problems: list[str] = []
    for source in (config or {}, overrides or {}):
        for k, v in source.items():
            if v is None:
                continue
            if k not in known:
                unknown.append(k)
                continue
            merged[k] = _coerce(k, v, coerce_problems)
    s = Settings(**merged)
    # normalise
    s.keywords = _dedupe([k.strip() for k in s.keywords if k and k.strip()])
    s.within = (s.within or "month").lower()
    s.sorts = [x.lower() for x in s.sorts]
    s.formats = [f.lower().lstrip(".") for f in s.formats]
    s.languages = [lang.strip() for lang in s.languages if lang.strip()]
    s._unknown_keys = unknown  # type: ignore[attr-defined]
    s._coerce_problems = coerce_problems  # type: ignore[attr-defined]
    return s


def read_keywords_file(path: str | os.PathLike) -> list[str]:
    """One keyword per line; blank lines and lines starting with # are ignored."""
    out = []
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"The keywords file {p} does not exist.")
    for line in read_text_any(p).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def toml_value(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, (list, tuple)):
        if len(v) > 3 or sum(len(str(x)) for x in v) > 60:
            return "[\n" + "".join(f"    {toml_value(x)},\n" for x in v) + "]"
        return "[" + ", ".join(toml_value(x) for x in v) + "]"
    s = str(v).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{s}"'


def _value_span(text: str, start: int) -> int:
    """Index just past the TOML value starting at `start` (handles arrays and quoted strings)."""
    i, depth, quote = start, 0, ""
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\" and quote == '"':
                i += 2
                continue
            if c == quote:
                quote = ""
        elif c in "\"'":
            quote = c
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return i + 1
        elif c == "#":  # a comment runs to the end of the line, even inside a multi-line array
            if depth == 0:
                return i
            nl = text.find("\n", i)
            i = len(text) if nl < 0 else nl
            continue
        elif c == "\n" and depth == 0:
            return i
        i += 1
    return i


def update_config_file(path: str | os.PathLike, updates: dict[str, Any]) -> None:
    """Change `key = value` lines in a TOML file in place, keeping comments and layout.
    Keys that are not in the file yet are appended at the end."""
    import re

    p = Path(path)
    text = read_text_any(p) if p.exists() else ""
    crlf = "\r\n" in text  # Notepad files: edit with \n, write back with \r\n
    text = text.replace("\r\n", "\n")
    original = text
    missing = []
    for key, value in updates.items():
        found = []
        for cand in re.finditer(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*", text):
            headers = re.findall(r"(?m)^[ \t]*(\[\[?)", text[: cand.start()])
            if headers and headers[-1] == "[[":
                continue  # inside a [[keyword_settings]] block - that's a per-keyword override
            found.append(cand)
        if not found:
            missing.append(f"{key} = {toml_value(value)}")
            continue
        for m in reversed(found):  # every copy (e.g. one in [search] and one in [saved_from_window])
            end = _value_span(text, m.end())
            old = text[m.end():end]
            trailing = old[len(old.rstrip()):]  # keep spacing before an inline comment
            text = text[: m.end()] + toml_value(value) + trailing + text[end:]
    if missing:
        # a section of its own, so the keys can't end up inside a [[keyword_settings]] table
        hm = re.search(r"(?m)^[ \t]*\[saved_from_window\][ \t]*(#.*)?$", text)
        if hm:  # put them right under the existing header, wherever it is
            at = hm.end()
            text = text[:at] + "\n" + "\n".join(missing) + text[at:]
        else:
            text = (text.rstrip("\n") + "\n\n# saved from the window interface\n[saved_from_window]\n"
                    + "\n".join(missing) + "\n")
    _check_rewrite(original, text, updates)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\r\n" if crlf else "\n")
    from .utils import replace_file

    replace_file(tmp, p)


def _check_rewrite(before: str, after: str, updates: dict[str, Any]) -> None:
    """Never write a config that lost settings: the new text must parse, keep every key it had
    (sections and [[keyword_settings]] included) and hold the new values."""
    if _toml is None:
        return
    try:
        new = _toml.loads(after)
    except _toml.TOMLDecodeError as e:
        raise ConfigError(f"Not saved - the settings file could not be updated safely ({e}).") from None
    try:
        old = _toml.loads(before) if before.strip() else {}
    except _toml.TOMLDecodeError:
        old = {}

    def keys(d: dict, prefix: str = "") -> set[str]:
        out = set()
        for k, v in d.items():
            out.add(prefix + k)
            if isinstance(v, dict):
                out |= keys(v, f"{prefix}{k}.")
            elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
                out.add(f"{prefix}{k}[{len(v)}]")
        return out

    lost = keys(old) - keys(new)
    if lost:
        raise ConfigError(f"Not saved - updating the settings file would have lost: {', '.join(sorted(lost)[:5])}.")
    flat = {}
    for k, v in new.items():
        flat.update(v) if isinstance(v, dict) else flat.__setitem__(k, v)
    wrong = [k for k, v in updates.items()
             if v is not None and (k not in flat or (flat[k] != v and not isinstance(v, float)))]
    if wrong:
        raise ConfigError(f"Not saved - could not update {', '.join(wrong[:5])} safely.")


def _dedupe(items: list[str]) -> list[str]:
    seen, out = set(), []
    for i in items:
        if i.lower() not in seen:
            seen.add(i.lower())
            out.append(i)
    return out
