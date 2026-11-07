"""CLAUDE.md / AGENTS.md in the output folder: a map of the folder for AI assistants that read files
locally (Claude Code, Claude Desktop with file access, Codex, Gemini CLI...).

Claude Code loads CLAUDE.md from the folder it's started in, so opening it in the output folder means
it already knows where everything is and how to search it cheaply. Rewritten after each run with the
current keywords and counts - unless you edited it (delete the first line to keep your own version).
"""

from __future__ import annotations

import datetime as dt
import json
import logging
from pathlib import Path

log = logging.getLogger("yt_transcripts")

MARK = "<!-- written by YouTube Transcript Tool after each run; delete this line to keep your own edits -->"


def _stats(out: Path) -> tuple[int, list[str], str]:
    try:
        data = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0, [], ""
    ok = sum(1 for r in data.values() if isinstance(r, dict) and r.get("status") == "ok")
    runs = sorted({r.get("run", "") for r in data.values() if isinstance(r, dict) and r.get("run")})
    folders = sorted(p.name for p in (out / "transcripts").iterdir() if p.is_dir()) if (out / "transcripts").exists() else []
    return ok, folders, runs[-1] if runs else ""


def render(out: Path, s) -> str:
    ok, folders, last = _stats(out)
    kws = ", ".join(f'"{k}"' for k in s.all_keywords()[:20]) or "none"
    chans = ", ".join(s.channels[:20]) or "none"
    fmts = ", ".join(f".{f}" for f in s.formats)
    when = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    by = {"keyword": "one folder per keyword (or channel)", "channel": "one folder per channel",
          "month": "one folder per upload month", "flat": "all in one folder"}.get(s.organize_by, s.organize_by)
    ts = bool(getattr(s, "timestamps", False))
    details = ", ".join(["title", "channel", "views", "published"]
                        + (["description"] if getattr(s, "include_description", False) else []) + ["tags"]
                        + (["chapters"] if getattr(s, "chapters", False) else []) + ["comments"])
    md_line = ("readable, every paragraph starts with a `[mm:ss](https://www.youtube.com/watch?v=ID&t=Ns)`\n"
               "    link to that moment - quote these links when citing." if ts else
               "readable paragraphs with the video's details on top (no timestamps; the `.json` has\n"
               "    each line's start time in seconds if a moment is needed).")
    cite = ("Name the video (title + channel) and the timestamp link for every claim, so it can be checked."
            if ts else "Name the video (title + channel) and its URL for every claim, so it can be checked.")
    return f"""{MARK}
# YouTube transcripts - guide for AI assistants

This folder holds YouTube transcripts collected by YouTube Transcript Tool, so you can answer questions
about the videos without anyone watching them. Updated {when}: {ok} transcripts saved, last run {last or "-"}.
Keywords: {kws}. Channels: {chans}.

## Where things are
- `combined/` - **start here for "what's new" questions.** One Markdown file per keyword per run
  (`transcripts_<YYYY-MM-DD_HHMM> - <keyword>.md`, newest = latest run), each video as a `## title`
  section with its details and transcript. Big runs are split into `(part i of n)` files.
- `transcripts/` - one set of files per video, {by}. Formats: {fmts}.
  File names: `<upload date> - <channel> - <title> [<VIDEO_ID>]`.
  - `.json`: complete text and timed segments (`transcript.segments[].start/duration/text`, seconds),
    plus video details ({details}).
  - `.md`: {md_line}
  - `.txt`: plain text with a header (title, channel, URL, date, views).
- `video_list.csv` / `.json` - the latest search: views, views per day, upload date, keyword,
  `keyword_mentions`, transcript file. `channel_list.*` - the latest channel download.
- `lists/` - a dated copy of every list ever made; `trends.html` charts them per day.
- `library.html` - every video from every run. `manifest.json` - download status per video (don't edit).
- `exports/` - `yt.py export` output: all transcripts as one `.jsonl` (one video per line) and `.csv`.

## How to work with it efficiently
- Search before reading: grep the `.txt` or `.md` files under `transcripts/` for a phrase, then open
  only the matching videos. Whole transcripts are long (an hour of speech is ~9,000 words).
- For recent news on a keyword, read the newest file in `combined/` for that keyword.
- For numbers (views, dates, growth) use `video_list.csv` or the `lists/` files, not the transcripts.
- {cite}
- Auto-generated captions have no punctuation guarantees and mishear names - say so when a quote
  matters. Sponsor reads and subscribe reminders may already be cut (see "Skipped" in the file header).
- A header line "Repeats: ..." marks a clip or re-upload of another video: don't count it twice.
- These files are rewritten by the tool; put your own notes in a separate file.

## Big jobs: distilling hundreds or thousands of videos
Too much to read at once, so work in two passes and keep the results in files (the tool never touches
`notes/` or `knowledge/`):
1. Map - for each transcript without a note, write `notes/<same file name>.md`: the claims and
   techniques taught, every concrete specific (numbers, settings, rules, tools, versions), who it's for,
   warnings and mistakes, and a 1-5 rating of how specific and substantiated it is. Work in batches
   (subagents help); skip videos that already have a note, so the work can be resumed.
2. Reduce - from `notes/`, write `knowledge/<topic>.md` per topic: consensus (how many videos support
   it), disagreements (both sides, with videos), the best explanation, specific numbers and settings,
   common mistakes, open questions. Then `knowledge/index.md` as the one-page overview.
3. Build from `knowledge/` what the user asks for (checklists, scripts, a Claude skill, a course...),
   citing videos. When new transcripts arrive, add their notes and update `knowledge/`, listing what
   changed at the top of `index.md`.
Skip files marked "Repeats:" (clips of other videos). Treat claims as what YouTubers say, not facts:
say how many videos support something, and flag health, legal and financial claims as such.
"""


def write_ai_guide(out_dir: Path, s) -> list[Path]:
    """Write CLAUDE.md and AGENTS.md (same text) unless the user made them their own."""
    out = Path(out_dir)
    if not out.exists():
        return []
    text = render(out, s)
    written = []
    for name in ("CLAUDE.md", "AGENTS.md"):
        p = out / name
        try:
            if p.exists() and not p.read_text(encoding="utf-8", errors="replace").startswith(MARK):
                continue  # edited by hand: leave it alone
            p.write_text(text, encoding="utf-8")
            written.append(p)
        except OSError as e:
            log.debug("could not write %s: %s", p, e)
    return written
