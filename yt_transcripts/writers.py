"""Write the video list and the transcript files."""

from __future__ import annotations

import csv
import datetime as dt
import json
import logging
import os
import re
from pathlib import Path

from .models import Transcript, Video
from .utils import format_duration, format_ts, replace_file, safe_filename

log = logging.getLogger("yt_transcripts")

LIST_COLUMNS = [
    "published", "published_exact", "is_new", "views", "views_per_day", "title", "channel", "url", "duration",
    "keyword", "keyword_mentions", "transcript_status", "transcript_language", "transcript_kind", "transcript_file",
    "video_id", "channel_id", "channel_handle", "duration_seconds", "is_short", "live_status", "source",
    "first_seen",
]


def mark_new(videos: list[Video], out_dir: Path) -> int:
    """Flag videos no earlier search has found, and remember all of them. Returns the number of new ones."""
    path = out_dir / "seen.json"
    try:
        seen: dict[str, str] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except ValueError:
        seen = {}
    now = dt.datetime.now().isoformat(timespec="minutes")
    first_run = not seen
    new = 0
    for v in videos:
        if v.video_id in seen:
            v.is_new, v.first_seen = False, seen[v.video_id]
        else:
            seen[v.video_id] = v.first_seen = now
            v.is_new = not first_run  # on the very first run nothing is "new"
            new += v.is_new
    _atomic_write(path, json.dumps(seen, indent=0))
    return new


# ---- video list ------------------------------------------------------------------
def write_video_list(videos: list[Video], out_dir: Path, stem: str = "video_list",
                     summary: str = "") -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{stem}.csv"
    json_path = out_dir / f"{stem}.json"
    csv_path = _write_list_file(csv_path, _csv_text(videos), encoding="utf-8-sig")  # BOM so Excel shows unicode
    json_path = _write_list_file(json_path, json.dumps([_list_dict(v) for v in videos], indent=2,
                                                       ensure_ascii=False))
    from .report import render_html

    html_path = _write_list_file(out_dir / f"{stem}.html", render_html(videos, out_dir, summary=summary))
    return {"csv": csv_path, "json": json_path, "html": html_path}


LIST_DESCRIPTION_CHARS = 500  # the transcript files keep the full description; the list only a snippet


def _list_dict(v: Video) -> dict:
    d = v.to_dict()
    d.pop("comments", None)  # in the transcript files; the list stays small
    if len(d.get("description") or "") > LIST_DESCRIPTION_CHARS:
        d["description"] = d["description"][:LIST_DESCRIPTION_CHARS]
    return d


def write_library(out_dir: Path, s) -> Path | None:
    """library.html: every video from every saved list (lists/), newest first, with the transcripts
    downloaded so far - the long-term view across many daily runs. Returns None if there's nothing yet."""
    from .pipeline import apply_manifest
    from .report import render_html
    from .search import rank_newest

    files = sorted((out_dir / "lists").glob("*_list.json"))  # names start with the date: oldest first
    merged: dict[str, Video] = {}
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for d in data if isinstance(data, list) else []:
            if not isinstance(d, dict) or not d.get("video_id"):
                continue
            try:
                v = Video.from_dict(d)
            except (TypeError, ValueError):
                continue
            v.transcript_status = v.transcript_language = v.transcript_kind = v.transcript_file = ""
            v.keyword_mentions, v.is_new, v.duplicate_of = None, False, ""  # the manifest is the record
            old = merged.get(v.video_id)
            if old is None:
                merged[v.video_id] = v
            else:
                v.merge(old)  # newest sighting first; keeps every keyword and the highest view count
                merged[v.video_id] = v
    if not merged:
        return None
    videos = rank_newest(list(merged.values()))
    apply_manifest(videos, s)
    with_tx = sum(1 for v in videos if v.transcript_status == "ok")
    summary = (f"Every video from your {len(files)} saved list{'s' if len(files) != 1 else ''} "
               f"(the lists folder) - {with_tx} with a transcript. Rebuilt after each run.")
    return _write_list_file(out_dir / "library.html",
                            render_html(videos, out_dir, title="All collected videos", summary=summary))


def _write_list_file(path: Path, content: str, encoding: str = "utf-8") -> Path:
    """Write a list file; if it's locked (open in Excel on Windows), save a copy next to it instead of failing."""
    try:
        _atomic_write(path, content, encoding=encoding, attempts=2)  # Excel holds its file until closed
        return path
    except PermissionError:
        alt = path.with_name(f"{path.stem} (new){path.suffix}")
        try:
            _atomic_write(alt, content, encoding=encoding, attempts=2)
        except PermissionError:
            log.warning("Could not save %s - it is open in another program. Close it and run again.", path.name)
            return path
        log.warning("%s is open in another program (Excel?), so this list was saved as %s instead.",
                    path.name, alt.name)
        return alt


def _csv_text(videos: list[Video]) -> str:
    import io

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=LIST_COLUMNS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for v in videos:
        row = v.to_dict()
        row["duration"] = format_duration(v.duration_seconds)
        vpd = v.views_per_day()
        row["views_per_day"] = round(vpd) if vpd is not None else ""
        w.writerow(row)
    return buf.getvalue()


def read_video_list(path: str | os.PathLike) -> list[Video]:
    """Load a list written by write_video_list (CSV or JSON), or a plain text file of URLs/IDs."""
    from .config import read_text_any

    p = Path(path)
    text = read_text_any(p)  # UTF-8, UTF-16 or Windows "ANSI" (Excel / Notepad)
    if p.suffix.lower() == ".json":
        return [Video.from_dict(d) for d in json.loads(text)]
    if p.suffix.lower() == ".csv":
        import io

        header = text.split("\n", 1)[0]
        delimiter = ","  # Excel in many countries saves "CSV" with semicolons (or tabs)
        try:
            delimiter = csv.Sniffer().sniff(header, delimiters=",;\t").delimiter
        except csv.Error:
            pass

        class _Dialect(csv.excel):  # standard quoting ("" inside quotes) - only the separator varies
            pass

        _Dialect.delimiter = delimiter
        rows = list(csv.DictReader(io.StringIO(text, newline=""), dialect=_Dialect))
        out = []
        for r in rows:
            r = {str(k).strip().lower(): v for k, v in r.items() if k is not None}  # "URL", " Video_ID "
            # Excel can turn an ID starting with "-" into #NAME? - the url column is the safer source then
            vid = _extract_id(r.get("video_id") or "") or _extract_id(r.get("url") or "")
            if vid:
                r["video_id"] = vid
                r.pop("duration", None)
                r.pop("views_per_day", None)
                out.append(Video.from_dict(r))
        if out:
            return out
        # no usable columns (no header, other names): pick up any YouTube links anywhere in the file
        seen: set[str] = set()
        for m in re.finditer(r"https?://[^\s,;\"']*(?:youtube\.com|youtu\.be)[^\s,;\"']*", text):
            vid = _extract_id(m.group(0))
            if vid and vid not in seen:
                seen.add(vid)
                out.append(Video(video_id=vid, source="list-file"))
        return out
    # plain text: one URL or ID per line
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            vid = _extract_id(line)
            if vid:
                out.append(Video(video_id=vid, source="list-file"))
    return out


def _extract_id(s: str) -> str:
    import re

    s = s.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/live/|/embed/)([A-Za-z0-9_-]{11})", s)
    return m.group(1) if m else ""


# ---- transcripts --------------------------------------------------------------------
MAX_PATH = 240  # Windows refuses paths over 260 characters unless long paths are enabled


DEFAULT_NAME = "{date} - {channel} - {title} [{id}]"


def transcript_basename(v: Video, max_len: int = 150, template: str = DEFAULT_NAME,
                        lang: str = "") -> str:
    """The file name (without extension) from the file_name template, e.g. '2026-10-27 - Channel - Title
    [VIDEOID]'. The video ID is always part of it (two videos can share a title); the title, then the
    channel, are shortened to fit max_len."""
    import re as _re

    template = (template or DEFAULT_NAME).strip()
    if "{id}" not in template:
        template += " [{id}]"
    fields = {
        "date": v.published[:10] if v.published else "unknown-date",
        "id": v.video_id,
        "views": str(v.views) if v.views is not None else "",
        "keyword": safe_filename((v.keyword.split("; ")[0] if v.keyword else ""), 40),
        "lang": lang,
        "channel": safe_filename(v.channel or "unknown channel", 40),
        "title": safe_filename(v.title or v.video_id, 90),
    }

    def fill(f: dict) -> str:
        out = _re.sub(r"{(\w+)}", lambda m: f.get(m.group(1), ""), template)
        out = _re.sub(r"\s+", " ", out).strip(" -_.")
        return safe_filename(out, 10_000) or v.video_id

    name = fill(fields)
    # too long: shorten the title (down to 8 characters), then the channel (down to 4)
    for key, floor in (("title", 8), ("channel", 4)):
        for _ in range(3):  # cutting can also drop a trailing space or dot, so re-check
            excess = len(name) - max_len
            if excess <= 0 or len(fields[key]) <= floor:
                break
            fields[key] = safe_filename(fields[key], max(len(fields[key]) - excess, floor))
            name = fill(fields)
    return name if len(name) <= max_len else v.video_id


def transcript_folder(root: Path, v: Video, organize_by: str) -> Path:
    if organize_by == "channel":
        return root / safe_filename(v.channel or "unknown channel", 50)
    if organize_by == "keyword":
        kw = (v.keyword.split("; ")[0] if v.keyword else "") or "no keyword"
        return root / safe_filename(kw, 50)
    if organize_by == "month":
        return root / (v.published[:7] if len(v.published) >= 7 else "unknown month")
    return root


def write_transcript(v: Video, t: Transcript, folder: Path, formats: list[str],
                     timestamps: bool = False, paragraph_seconds: int = 30, base: str = "",
                     template: str = DEFAULT_NAME, raw: Transcript | None = None) -> dict[str, Path]:
    """Write the formats; `raw` (the uncleaned transcript) goes into the .json if given."""
    folder.mkdir(parents=True, exist_ok=True)
    longest_ext = max((len(f) for f in formats), default=4) + 1
    budget = MAX_PATH - len(str(folder.resolve())) - 1 - longest_ext - 4  # 4 = ".tmp"
    # if the folder itself is extremely deep, fall back to just the video ID
    if not base:
        base = (transcript_basename(v, max_len=min(150, budget), template=template, lang=t.language)
                if budget >= 36 else v.video_id)
    written: dict[str, Path] = {}
    for fmt in formats:
        path = folder / f"{base}.{fmt}"
        if fmt == "txt":
            content = render_txt(v, t, timestamps, paragraph_seconds)
        elif fmt == "md":
            content = render_md(v, t, paragraph_seconds)
        elif fmt == "srt":
            content = render_srt(t)
        elif fmt == "vtt":
            content = render_vtt(t)
        elif fmt == "json":
            content = render_json(v, raw or t)
        else:
            continue
        _atomic_write(path, content)
        written[fmt] = path
    return written


def _kind_text(t: Transcript) -> str:
    return {"manual": "uploaded captions", "auto": "auto-generated",
            "translated": "machine-translated"}.get(t.kind, t.kind)


def _lang_name(t: Transcript) -> str:
    return re.sub(r"\s*\((?:auto-generated|Original)\)", "", t.language_name or "").strip() or t.language


MAX_TAGS_SHOWN = 20


def _one_line(text: str) -> str:
    return " ".join(str(text).split())  # titles can hold line breaks (incl. U+2028) - they'd break the layout


def _header_lines(v: Video, t: Transcript) -> list[str]:
    pub = v.published[:10] if v.published else "unknown"
    if v.published and not v.published_exact:
        pub += " (approximate)"
    lines = [
        f"Title: {_one_line(v.title)}",
        f"Channel: {_one_line(v.channel)}",
        f"URL: https://www.youtube.com/watch?v={v.video_id}",
        f"Published: {pub}",
        f"Views: {v.views:,}" if v.views is not None else "Views: unknown",
        f"Duration: {format_duration(v.duration_seconds) or 'unknown'}",
        f"Keyword: {v.keyword}",
        f"Transcript: {_lang_name(t)} ({_kind_text(t)}), via {t.method}",
        f"Downloaded: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ]
    if v.tags:
        lines.append(f"Tags: {', '.join(v.tags[:MAX_TAGS_SHOWN])}")
    if v.chapters:
        lines.append(f"Chapters: {len(v.chapters)}")
    if t.removed:
        from .sponsorblock import describe

        lines.append(f"Skipped (SponsorBlock): {describe(t.removed)}")
    if v.duplicate_of:
        vid, _, title = v.duplicate_of.partition(" ")
        lines.append(f"Repeats: {title or vid} (https://www.youtube.com/watch?v={vid})")
    return lines


def _chapter_starts(v: Video) -> list[float]:
    return [c["start"] for c in v.chapters if c["start"] > 0]


CHAPTER_SLACK = 1.0  # seconds: caption lines rarely start exactly on a chapter mark


def paragraphs(t: Transcript, seconds: int = 30, breaks: list[float] | None = None) -> list[tuple[float, str]]:
    """Group segments into ~N-second paragraphs, breaking at sentence ends when possible - and always
    at the given break times (chapter starts), so every chapter begins with a new paragraph."""
    out: list[tuple[float, str]] = []
    cur: list[str] = []
    start = None
    pending = sorted(b for b in (breaks or []) if b > 0)
    for s in t.segments:
        if pending and s.start >= pending[0] - CHAPTER_SLACK:
            while pending and s.start >= pending[0] - CHAPTER_SLACK:
                pending.pop(0)
            if cur:
                out.append((start or 0.0, " ".join(cur)))
                cur, start = [], None
        if start is None:
            start = s.start
        cur.append(s.text)
        long_enough = s.end - start >= seconds
        sentence_end = s.text.rstrip().endswith((".", "?", "!", '"', "”"))
        if long_enough and (sentence_end or s.end - start >= seconds * 2):
            out.append((start, " ".join(cur)))
            cur, start = [], None
    if cur:
        out.append((start or 0.0, " ".join(cur)))
    return out


def _with_chapters(v: Video, paras: list[tuple[float, str]]):
    """Yield ("chapter", start, title) and ("text", start, text) items in reading order."""
    chapters = list(v.chapters)
    i = 0
    for start, text in paras:
        while i < len(chapters) and chapters[i]["start"] <= start + CHAPTER_SLACK:
            yield "chapter", chapters[i]["start"], chapters[i]["title"]
            i += 1
        yield "text", start, text
    # chapters after the last caption line (e.g. an outro without speech) are left out on purpose


def render_txt(v: Video, t: Transcript, timestamps: bool = False, paragraph_seconds: int = 30,
               description: bool = True) -> str:
    lines = _header_lines(v, t)
    if description and v.description.strip():
        lines += ["", "Description:", v.description.strip()]
    lines += ["-" * 60, ""]
    paras = paragraphs(t, paragraph_seconds, _chapter_starts(v))
    for kind, start, text in _with_chapters(v, paras):
        if kind == "chapter":
            lines += [f"== {_one_line(text)} ({format_ts(start)}) ==", ""]
        else:
            lines += [f"[{format_ts(start)}] {text}" if timestamps else text, ""]
    if v.comments:
        lines += ["-" * 60, "", "Top comments:", ""]
        for c in v.comments:
            lines += [f"- {_one_line(c['author']) or 'someone'} ({c['likes']:,} likes): {' '.join(c['text'].split())}"]
    return "\n".join(lines).rstrip() + "\n"


def _yaml_str(value: str) -> str:
    """A YAML double-quoted scalar (JSON string syntax is valid YAML; escape YAML's extra line breaks)."""
    out = json.dumps(str(value), ensure_ascii=False)
    return "".join(c if c.isprintable() or c in "\t" else
                   (f"\\u{ord(c):04x}" if ord(c) <= 0xFFFF else f"\\U{ord(c):08x}") for c in out)


def front_matter(v: Video, t: Transcript) -> str:
    """YAML properties for Obsidian / Logseq / static-site tools (and harmless anywhere else)."""
    kws = [k for k in v.keyword.split("; ") if k]
    items: list[tuple[str, str]] = [
        ("title", _yaml_str(v.title)),
        ("channel", _yaml_str(v.channel)),
        ("url", _yaml_str(f"https://www.youtube.com/watch?v={v.video_id}")),
        ("video_id", _yaml_str(v.video_id)),
        ("published", _yaml_str(v.published[:10]) if v.published else '""'),
        ("views", str(v.views) if v.views is not None else '""'),
        ("duration", _yaml_str(format_duration(v.duration_seconds) or "")),
        ("keywords", "[" + ", ".join(_yaml_str(k) for k in kws) + "]"),
        ("youtube_tags", "[" + ", ".join(_yaml_str(x) for x in v.tags[:MAX_TAGS_SHOWN]) + "]"),
        ("language", _yaml_str(t.language)),
        ("captions", _yaml_str(_kind_text(t))),
        ("downloaded", _yaml_str(dt.datetime.now().strftime("%Y-%m-%d %H:%M"))),
        ("source", '"youtube"'),
    ]
    return "---\n" + "".join(f"{k}: {val}\n" for k, val in items) + "---\n"


def _md_text(text: str) -> str:
    """Caption text that Markdown would otherwise turn into a heading, list or quote."""
    return re.sub(r"^(\s*)([#>*+-]|\d+[.)])(\s)", r"\1\\\2\3", text)


def render_md(v: Video, t: Transcript, paragraph_seconds: int = 30, *, properties: bool = True,
              description: bool = True, level: int = 1) -> str:
    h = "#" * level
    lines = [front_matter(v, t)] if properties else []
    lines += [f"{h} {_one_line(v.title) or v.video_id}", ""]
    lines += [f"- **{ln.split(': ', 1)[0]}:** {ln.split(': ', 1)[1]}" for ln in _header_lines(v, t)[1:]]
    if description and v.description.strip():
        quoted = "\n".join(f"> {_md_text(ln)}".rstrip() for ln in v.description.strip().splitlines())
        lines += ["", f"{h}# Description", "", quoted]
    lines += ["", f"{h}# Transcript", ""]
    paras = paragraphs(t, paragraph_seconds, _chapter_starts(v))
    for kind, start, text in _with_chapters(v, paras):
        link = f"https://www.youtube.com/watch?v={v.video_id}&t={int(start)}s"
        if kind == "chapter":
            lines += [f"{h}## {_one_line(text)} ([{format_ts(start)}]({link}))", ""]
        else:
            lines += [f"[{format_ts(start)}]({link}) {_md_text(text)}", ""]
    if v.comments:
        lines += [f"{h}# Top comments", ""]
        for c in v.comments:
            lines += [f"- **{_md_text(_one_line(c['author'])) or 'someone'}** ({c['likes']:,} likes): "
                      f"{_md_text(' '.join(c['text'].split()))}"]
    return "\n".join(lines).rstrip() + "\n"


def render_srt(t: Transcript) -> str:
    blocks = []
    for i, s in enumerate(t.segments, 1):
        end = s.end if s.duration > 0 else s.start + 2
        blocks.append(f"{i}\n{format_ts(s.start, srt=True)} --> {format_ts(end, srt=True)}\n{s.text}\n")
    return "\n".join(blocks)


def render_vtt(t: Transcript) -> str:
    blocks = ["WEBVTT", ""]
    for s in t.segments:
        end = s.end if s.duration > 0 else s.start + 2
        a = format_ts(s.start, srt=True).replace(",", ".")
        b = format_ts(end, srt=True).replace(",", ".")
        blocks += [f"{a} --> {b}", s.text, ""]
    return "\n".join(blocks)


def render_json(v: Video, t: Transcript) -> str:
    return json.dumps({
        "video": v.to_dict(),
        "transcript": {
            "language": t.language,
            "language_name": t.language_name,
            "kind": t.kind,
            "method": t.method,
            "skipped": t.skipped,  # SponsorBlock segments (the text below is complete; other formats cut them)
            "text": t.text,
            "segments": [{"start": round(s.start, 3), "duration": round(s.duration, 3), "text": s.text}
                         for s in t.segments],
        },
    }, indent=2, ensure_ascii=False)


def _combined_key(v: Video) -> str:
    return (v.keyword.split("; ")[0] if v.keyword else "") or "videos from a list"


def write_combined(entries: list[tuple[Video, Transcript]], folder: Path, stamp: str,
                   paragraph_seconds: int = 30, max_words: int = 0) -> list[Path]:
    """AI-ready files: one Markdown file per keyword per run, split into parts of at most `max_words`
    words (0 = no limit) so each part fits an AI chat or NotebookLM source. A video is never split."""
    groups: dict[str, list[tuple[Video, Transcript]]] = {}
    for v, t in entries:
        groups.setdefault(_combined_key(v), []).append((v, t))
    written: list[Path] = []
    used: set[str] = set()  # names taken in this run - case-insensitive, like Windows
    for key, items in groups.items():
        blocks = [(v, render_md(v, t, paragraph_seconds, properties=False, description=False, level=2))
                  for v, t in items]
        parts: list[list[tuple[Video, str]]] = [[]]
        words = 0
        for v, block in blocks:
            n = len(block.split())
            if max_words and parts[-1] and words + n > max_words:
                parts.append([])
                words = 0
            parts[-1].append((v, block))
            words += n
        for i, part in enumerate(parts, 1):
            suffix = f" (part {i} of {len(parts)})" if len(parts) > 1 else ""
            title = f"YouTube transcripts: {key}{suffix}"
            lines = [f"# {title}", "",
                     f"{len(part)} video{'s' if len(part) != 1 else ''}, collected "
                     f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}. Each video starts with a level-2 "
                     "heading, followed by its details and the transcript.", ""]
            for n, (v, _) in enumerate(part, 1):
                lines.append(f"{n}. [{_one_line(v.title) or v.video_id}]"
                             f"(https://www.youtube.com/watch?v={v.video_id}) - {_one_line(v.channel)}")
            lines.append("")
            for _, block in part:
                lines += ["---", "", block]
            base = f"transcripts_{stamp} - {safe_filename(key, 60)}"
            name, n = f"{base}{suffix}.md", 2
            while name.lower() in used:  # "AI: news" and "AI news" make the same file name
                name, n = f"{base} ({n}){suffix}.md", n + 1
            used.add(name.lower())
            path = folder / name
            _atomic_write(path, "\n".join(lines))
            written.append(path)
    return written


def _atomic_write(path: Path, content: str, encoding: str = "utf-8", attempts: int = 6) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(content, encoding=encoding, newline="\n")
    try:
        replace_file(tmp, path, attempts)
    except OSError:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise
