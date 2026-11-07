# YouTube Transcript Tool

**Turn YouTube into text your AI can read — fast.**

An hour of video takes an hour to watch, but its transcript (about 9,000 words) takes an AI a few seconds
to read. This tool is built for that kind of fast data consumption: it searches YouTube for your keywords
(or takes whole channels and playlists), keeps the **newest videos above a view threshold**, and
**downloads every transcript** to your computer — clean, deduplicated and ready for Claude, ChatGPT,
Gemini, NotebookLM, Obsidian or your own scripts. Fifty new videos on your topic become one file you can
ask questions of, every morning, without watching any of them.

No API key needed. Windows: one `.exe` or a double-click `.bat`. macOS/Linux: the command line.

![The window: keywords and filters on the left, transcript options on the right, the run's log below](docs/screenshots/window.png)

**Contents:** [What it does](#what-it-does) · [Quick start](#quick-start-windows) ·
[Using it with AI](#using-it-with-ai) · [Tune the output for AI](#tune-the-output-for-ai) ·
[What AI can do with it](#what-ai-can-do-with-the-transcripts) ·
[Big jobs: thousands of videos](#big-jobs-read-thousands-of-videos-distill-the-knowledge-build-with-it) ·
[Features](#features-in-detail) ·
[Settings](#settings-configtoml) · [Command line](#command-line) · [Proxies and data](#proxies-speed-and-data-use) ·
[Decodo setup](#setting-up-decodo-residential-proxies-recommended) ·
[2,000+ use cases](use-cases.md) ·
[Troubleshooting](#troubleshooting)

---

## What it does

* **Finds the videos worth reading** — searches each keyword across several YouTube orderings and time
  windows, keeps videos above `min_views` (or rising fast), drops Shorts, live streams, re-uploads and
  too-short clips, and keeps the newest N.
* **Downloads the transcripts** — creator captions first, auto-captions otherwise, in your languages (or
  machine-translated into yours).
* **Cleans them for AI** — cuts sponsor reads, self-promotion and "like and subscribe" (SponsorBlock),
  optionally `[Music]` tags and "um/uh", and spots clips and re-uploads whose text repeats another video.
* **Packs them for AI** — one Markdown file per keyword per run in `combined\`, split to fit an AI's
  context, plus a `CLAUDE.md` map so Claude Code can search the whole folder itself.
* **Keeps track** — a sortable list with views per day and keyword mentions, a library of everything so
  far, a trends page, and re-runs that only fetch what's new. Runs daily on a schedule if you like.

<details>
<summary><b>Everything it can do (full list)</b></summary>

**Finding videos**
- Keyword search without an API key (yt-dlp), or with the YouTube Data API for exact dates and true newest-first.
- Time windows `today` / `week` / `month` / `year` / `any`, a finer `max_age_days`, or a date range.
- View filters: minimum, maximum (to find small creators), and *rising* videos below the minimum that gain enough views per day.
- Length filters, Shorts on/off, live streams excluded, "creator captions only".
- Title must contain / exclude words / exclude channels / only these channels; per-keyword overrides.
- Re-uploads of the same video by other channels dropped (the most-viewed copy is kept).
- **Whole channels and playlists**: every video, the newest N, Shorts and past streams too, with their own view and date filters.
- **Related keywords**: YouTube's autocomplete, phrases the top titles share, and tags of what you've downloaded, ranked — tick and add.
- Single videos or your own list of links (`.txt`, `.csv` or a list made earlier).

**Transcripts**
- Two download methods (yt-dlp, youtube-transcript-api) with automatic fallback; copes with YouTube's PO-token checks via Deno.
- Language preference list, fallback to the video's own language, or YouTube's machine translation.
- Formats: `.txt`, `.md` (with properties for Obsidian), `.srt`, `.vtt`, `.json` (every timed line + details).
- SponsorBlock cuts (sponsor, self-promotion, interaction reminders; also intro, outro, preview, filler…).
- Optional: remove sound tags, remove filler words, timestamps, the description, chapter headings, top comments.
- Repeat detection: clips and re-uploads are marked and left out of the AI files — built to have no false positives.
- Very short transcripts (music videos, intros) can be skipped with `min_transcript_words`.
- Change a text setting later and every file is rebuilt from the saved `.json` — nothing is downloaded again.

**Output**
- `combined\` AI files, split at `combine_max_words`; `CLAUDE.md` / `AGENTS.md` guide for AI assistants.
- `video_list.html` / `.csv` / `.json` with thumbnails, views/day, keyword mentions, transcript previews, **NEW** badges.
- `library.html` (every video from every run), `trends.html` (per keyword per day), dated copies in `lists\`.
- `yt.py export`: everything as one `.jsonl` and one `.csv` for embeddings, RAG or spreadsheets.
- `yt.py find`: search all transcripts with links to the exact second.
- Folders by keyword, channel, upload month or flat; your own file-name pattern.

**Running it**
- A window (`gui.bat` or the `.exe`), double-click `.bat` files, or the command line.
- Daily scheduled run (`schedule_daily.bat` / `yt.py schedule 08:00`) that also keeps yt-dlp updated.
- Proxies (HTTP/SOCKS, lists from proxy shops, rotating services), parallel downloads, per-IP hourly caps,
  proxy data metering with run/month limits and cost, and a data saver (roughly 40–100 KB per transcript).
- `yt.py doctor` self-test, `yt.py status`, resumable runs, automatic retries for "not yet" videos.

</details>

---

## Quick start (Windows)

**Easiest: the one-file program.** No Python needed.

1. Download **`YouTubeTranscriptTool.exe`** from the
   [latest release](https://github.com/austin-72/youtube-transcript-tool/releases/latest) and put it in a
   folder of its own (for example `Documents\YouTubeTranscriptTool`). It keeps `config.toml` and the
   `output` folder next to itself.
2. Install **Deno** once (YouTube needs it): open PowerShell and run `winget install DenoLand.Deno`.
3. Double-click the `.exe`. The window opens; type your keywords and press *Search + download*.

Windows may warn that the program is unrecognised (it isn't code-signed): click *More info* →
*Run anyway*. It's rebuilt every week with the newest yt-dlp — when YouTube changes something, download
it again. The same file works on the command line (`YouTubeTranscriptTool.exe run -k "ai agents"`), and
`YouTubeTranscriptTool.exe schedule 08:00` sets up a daily run.

<details>
<summary><b>Or run it from the source</b> (easy to update, and needed for the <code>.bat</code> helpers)</summary>

1. **Python 3.11 or newer.** Not sure? Just do step 2 — if Python is missing, setup offers to install it
   (via winget). By hand: <https://www.python.org/downloads/>, tick **"Add python.exe to PATH"**.
2. Double-click **`setup.bat`**. It creates a private environment in this folder, installs what's needed,
   offers to install *Deno* (say **Y**) and a Desktop shortcut, and runs a self-test.
3. Open **`config.toml`** in Notepad: set your `keywords`, `min_views` and `within`. Save.
4. Double-click **`run.bat`** — or **`gui.bat`** for the window.

`update.bat` updates yt-dlp when YouTube changes something. To build the `.exe` yourself: `build_exe.bat`.

</details>

### What you get

Everything lands in the **`output`** folder. Open **`video_list.html`**:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/video_list_dark.png">
  <img alt="The video list: thumbnails, titles, dates, views, views per day, keyword, mentions and a link to each transcript, with a preview of the first lines" src="docs/screenshots/video_list.png">
</picture>

```
output/
├── combined/transcripts_2026-10-28_2315 - ai agents.md   ← AI-ready: a keyword's new transcripts in one file
├── transcripts/ai agents/                                ← one set of files per video
│   ├── 2026-10-27 - Some Channel - Video title [VIDEO_ID].txt
│   └── 2026-10-27 - Some Channel - Video title [VIDEO_ID].json
├── video_list.html / .csv / .json   ← what was found: views, views/day, mentions, links
├── library.html                     ← every video from every run, with its transcript
├── trends.html                      ← per keyword per day: new videos, attention, fastest risers
├── lists/                           ← a dated copy of every list
├── CLAUDE.md / AGENTS.md            ← a map of this folder for Claude Code and other AI assistants
├── exports/                         ← yt.py export: all transcripts as .jsonl and .csv
├── manifest.json                    ← what's done, so re-runs skip finished videos
└── last_run.log
```

<details>
<summary><b>What a transcript file looks like</b></summary>

```
Title: <video title>
Channel: <channel name>
URL: https://www.youtube.com/watch?v=<VIDEO_ID>
Published: 2026-10-28
Views: 48,211
Duration: 14:05
Keyword: python tutorial
Transcript: English (auto-generated), via ytdlp
Downloaded: 2026-10-28 23:15
Tags: python, tutorial, beginners
Skipped (SponsorBlock): sponsor 1:12-2:03, subscribe reminder 13:40-13:52
------------------------------------------------------------

<the spoken text, grouped into paragraphs of roughly 30 seconds each>

<next paragraph ...>
```

With `include_description = true` the description follows the header; with `chapters = true` each chapter
gets a heading; with `timestamps = true` every paragraph starts with `[mm:ss]` (and in `.md`, a link to
that second). A clip of another video gets a `Repeats: <title> (<url>)` line.

</details>

Run it again any time: finished videos are skipped and only new ones are fetched; videos no earlier
search had found get a **NEW** badge.

---

## Using it with AI

There are three ways in, from simplest to most powerful:

1. **Upload a combined file.** Each run writes one Markdown file per keyword to `combined\` with every new
   transcript, split into parts of at most 80,000 words. Drop the newest one into Claude, ChatGPT, Gemini
   or NotebookLM and ask. *This is the one to upload.*
2. **Let an AI on your PC read the folder.** Claude Code (or Claude Desktop with file access) opens the
   `output` folder, reads `CLAUDE.md` and searches *everything you've ever collected*, reading only what
   it needs. Best for questions across weeks of runs.
3. **Feed your own tools.** `yt.py export` gives one `.jsonl` (one video per line) and one `.csv`; each
   video's `.json` has every timed line. For embeddings, a vector database, a RAG chatbot or a spreadsheet.

### Let Claude read the folder itself (Claude Code or Claude Desktop)

After every run the tool writes **`CLAUDE.md`** (and the same text as `AGENTS.md`, for Codex, Gemini CLI
and others) into the output folder: what's where, which keywords and channels you follow, how many
transcripts there are, and how to search them cheaply. Claude Code reads it automatically when started in
that folder, so it knows the layout from the first question.

**Claude Code** (needs a Claude subscription or API account):

1. Install it once: open PowerShell and run `irm https://claude.ai/install.ps1 | iex`
   (or `winget install Anthropic.ClaudeCode`).
2. Open a terminal in your output folder and start it:
   ```
   cd "C:\Users\you\Documents\YouTubeTranscriptTool\output"
   claude
   ```
3. Ask away:
   > What did this week's *ai agents* videos say about memory? Quote the best three explanations and
   > name the video for each.

   > Which channels in video_list.csv grew fastest (views per day), and what do their transcripts have
   > in common?

   > Compare how the three newest *local llm setup* videos install the model. Make a table.

**Claude Desktop:** add the *Filesystem* extension (Settings → Desktop app → Extensions → Manage) and give it your output
folder. Then ask the same kind of questions; point it to `CLAUDE.md` first ("read CLAUDE.md in my
transcripts folder, then…").

<details>
<summary><b>Automatic daily briefing with Claude Code</b> (no clicking at all)</summary>

Claude Code can run without a window: `claude -p "<question>"` prints the answer and exits, and it may read
files in the folder it's started in without asking. Put this in a `.bat` file next to the tool and point a
second scheduled task at it, an hour after the daily run:

```bat
cd /d "C:\Users\you\Documents\YouTubeTranscriptTool\output"
claude -p "Read CLAUDE.md. Then read today's files in combined/ and write a briefing: the 10 most important new things, which video said each one, and anything two videos disagree on." > "briefing %date:/=-%.md"
```

Each morning there's a fresh `briefing <date>.md`. See Claude Code's
[non-interactive mode](https://code.claude.com/docs/en/headless) for options.

</details>

Tips: keep asking in the same folder and Claude builds on what it found. If you edit `CLAUDE.md`
yourself, delete its first line and the tool leaves your version alone.

### Tune the output for AI

The defaults are already set for AI: plain text, no timestamps, no description, no chapter headings,
sponsor reads cut, repeats left out of the combined files. What you can still adjust:

| Setting | For AI | Why |
|---|---|---|
| `formats` | `["txt", "json"]` (default) | `.txt` is the leanest readable text. Keep `json`: it holds every timed line and lets the tool rebuild files later. Add `md` for Obsidian or clickable timestamps. |
| `timestamps` | `false` (default) | A `[mm:ss](link)` on every 30-second paragraph adds up to ~20% to `.md` and combined files (a few % in `.txt`). Turn on when you want the AI to cite the exact moment. |
| `include_description` | `false` (default) | Descriptions are mostly links, sponsor codes and social handles. Turn on for link, product or sponsor research. (It's free either way — no extra download.) |
| `chapters` | `false` (default) | Chapter headings; useful for long lectures you want the AI to outline. |
| `sponsorblock` | default on | Cuts sponsor reads, self-promotion and "like and subscribe" — the AI otherwise counts ads as content. |
| `remove_filler_words` | `true` | Removes "um", "uh", "erm", "hmm". |
| `strip_sound_tags` | `true` | Removes `[Music]`, `[Applause]`, `(laughs)`. |
| `skip_duplicates` | `true` (default) | Clips and re-uploads don't make the AI count the same statement twice. |
| `min_transcript_words` | `300` | Skips music videos and near-silent clips. |
| `combine_max_words` | `80000` (default) | ≈ 105,000 tokens per part. Lower it for AIs with smaller context windows or free plans. |
| `languages`, `translate` | your language | One language makes summaries and comparisons more reliable. |
| `list_sort` | `views_per_day` | The combined file follows the list order: the fastest-growing videos come first. |
| `top_comments` | `20` | Adds the audience's reaction; great for sentiment and "what are people asking". Costs some proxy data. |
| `organize_by` | `channel` | For studying creators: one folder per channel. |

A config for a daily AI briefing:

```toml
keywords = ["ai agents", "mcp servers"]
within = "today"
min_views = 5000
rising_views_per_day = 2000
formats = ["txt", "json"]
remove_filler_words = true
strip_sound_tags = true
min_transcript_words = 300
list_sort = "views_per_day"
```

<details>
<summary><b>How big is it? Words, tokens and how many videos fit</b></summary>

People speak about 150 words a minute, and one English word is roughly 1.3 tokens:

| Video length | Words | Tokens (approx.) |
|---|---|---|
| 1 minute | ~150 | ~200 |
| 10 minutes | ~1,500 | ~2,000 |
| 1 hour | ~9,000 | ~12,000 |

One combined part of 80,000 words ≈ 105,000 tokens ≈ fifty 10-minute videos or nine 1-hour videos.
Turning on `timestamps` adds up to ~20% (in `.md`), `include_description` a few hundred words per video,
`top_comments = 20` around 500–1,000 words per video.

</details>

<details>
<summary><b>File formats for your own code</b> (.json, .jsonl, video_list)</summary>

Each video's **`.json`**:

```json
{
  "video": {"video_id": "...", "title": "...", "channel": "...", "channel_id": "UC...",
            "published": "2026-11-03T15:04:05+00:00", "published_exact": true, "views": 48211,
            "duration_seconds": 845, "keyword": "ai agents", "tags": ["..."], "comments": [],
            "duplicate_of": "", "...": "..."},
  "transcript": {"language": "en", "language_name": "English", "kind": "auto", "method": "ytdlp",
                 "skipped": [{"start": 72.0, "end": 123.0, "category": "sponsor"}],
                 "text": "the full original text",
                 "segments": [{"start": 0.0, "duration": 3.2, "text": "..."}]}
}
```

The `.json` keeps the full original text; `skipped` lists the SponsorBlock parts the readable files cut.

**`yt.py export`** → `exports\all_transcripts_<date>.jsonl`, one video per line, with the cleaned text
(SponsorBlock cuts and your text settings applied): `video_id, title, channel, published, views,
duration_seconds, keyword, url, language, kind, words, text, segments`. The `.csv` has the same columns
without `segments`.

**`video_list.csv`** columns: `published, published_exact, is_new, views, views_per_day, title, channel,
url, duration, keyword, keyword_mentions, transcript_status, transcript_language, transcript_kind,
transcript_file, video_id, channel_id, channel_handle, duration_seconds, is_short, live_status, source,
first_seen`.

</details>

### What AI can do with the transcripts

Each of these is a setting or two plus a prompt.

**1. A daily briefing on your niche.** Keywords for your field, `within = "today"`, then
`schedule_daily.bat`. Each morning, upload the newest file from `combined\` and ask:

> These are transcripts of the most-watched new YouTube videos about *ai agents* from the last 24 hours.
> Give me a briefing: the 10 most important new things (announcements, techniques, numbers), which video
> said each one, and anything two videos disagree on.

**2. Learn a subject in an afternoon.** *Whole channels…* → paste a course playlist link (or a teacher's
channel with *Newest per channel* = 30). Add the combined file to **NotebookLM** or a Claude project:

> Turn these lectures into a study guide: the key ideas in order, a one-paragraph explanation of each, the
> examples the speaker used, and 15 quiz questions with answers. Note the video for each section.

**3. Study a creator or a competitor.** Whole channel, *Uploaded: This year*, `list_sort = "views"`.
Give the AI the transcripts *and* `channel_list.csv`:

> Using the transcripts and the view counts in the CSV: which topics does this channel return to most,
> how did that change over the year, and what do their best-performing videos (views per day) have in
> common in the first 60 seconds?

**4. Find content gaps.** *Find related keywords…* to widen your list, run it, then:

> Across these videos, which questions are raised but never properly answered? Which subtopics appear in
> only one or two videos? List 10 video ideas that would fill those gaps, each with a working title.

**5. Skip the clickbait.** Sort the list by **mentions**: a popular video whose transcript never says the
words in its title is usually not worth your time.

> For each video, does the transcript deliver what the title promises? Rate 1–5 with one sentence why.

<details>
<summary><b>30 more things to ask, by goal</b></summary>

**Research and learning**
- "Explain *X* the way these videos do, from beginner to advanced, and say where they disagree."
- "Build a glossary of every technical term used in these transcripts, with a one-line definition each."
- "What are the five most common mistakes these tutorials warn about?"
- "Make a step-by-step checklist from these setup videos. Mark the steps only one video mentions."
- "Which claims here come with evidence (numbers, demos, sources) and which are opinion?"
- "Summarise each video in three bullet points, then the whole set in one paragraph."

**Content creation**
- "Which hooks do the highest views-per-day videos use in their first 30 seconds? Quote them."
- "What questions does the audience keep asking in the comments that no video answers?" *(top_comments)*
- "Write a script outline for a video that covers what these all miss, in a voice like the top channel's."
- "List the stories, analogies and examples that appear in several videos — they're what resonates."
- "Which topics went from zero to several videos in the last two weeks?" *(daily runs + trends.html)*

**Business, marketing and products**
- "Which products, tools and brands are mentioned, how often, and is the tone positive or negative?"
- "What pain points do people describe with *X*? Group them and count how many videos raise each."
- "Compare what reviewers say about product A versus B. Make a table of pros and cons with sources."
- "Which sponsors appear across these channels?" *(include_description = true, sponsorblock = [])*
- "What do customers in these videos wish *X* did that it doesn't?"

**News, markets and events**
- "What changed this week compared with last week's files in `combined/`?" *(Claude Code)*
- "Timeline of the announcements in these videos, oldest first, with the date and the source video."
- "Which predictions were made, by whom, and with what reasoning?"
- "Separate what was reported as fact from speculation. Name the video for each."

**Fact-checking and journalism**
- "Find every claim about *X*. Quote it word for word with the video and timestamp." *(timestamps = true)*
- "Where do these videos contradict each other? Quote both sides."
- "Which statements are repeated across channels with nearly the same wording?" *(talking points)*

**Audience and sentiment** *(top_comments = 20)*
- "What do the comments praise and criticise most? Give counts and example quotes."
- "Do the comments agree with the video's main claim? One line per video."

**Data and code** *(yt.py export, the .json files)*
- Embed the `.jsonl` into a vector database and build a chatbot that answers from your transcripts with sources.
- Classify every video by topic, stance or difficulty with an AI and add the label as a column to `video_list.csv`.
- Ask Claude Code to "write a script that counts how often each keyword is mentioned per day across lists/ and plot it".
- Track how often a term appears per week to spot rising topics before they trend.
- Build a study deck: "Turn each transcript into 10 flashcards (question; answer) as CSV for Anki."

</details>

**6. …and 2,179 more.** **[use-cases.md](use-cases.md)** lists 2,179 different ways to use the tool,
across 40 fields — trading, marketing, SEO, AI, software, design, research, teaching, health, hobbies,
industry and more — each with what to collect, what to ask the AI, and what you build from it.

Tips: ask the AI to name the video (and the timestamp, with `timestamps = true`) for every point so you
can check it. Auto-generated captions mishear names — say so when a quote matters. Use the transcripts for
your own research and respect the creators' work.

Without AI: double-click `search_transcripts.bat` (or *Find in transcripts…*, or `yt.py find "context
window"`) — every match comes with a link to the exact second.

---

## Big jobs: read thousands of videos, distill the knowledge, build with it

One video gives you one person's opinion. A thousand videos on a subject give you the field's **collective
knowledge**: what everyone agrees on, where the experts disagree, the tricks only a few people know, the
mistakes everyone warns about, and the exact settings, numbers and tools people actually use. No person can
watch that much. An AI can read it in an afternoon, and you can build real things on top of the result.

The playbook has four steps. Steps 2–4 work best with **Claude Code** started in the `output` folder; the
folder's `CLAUDE.md` already describes this workflow, so you can simply ask for it.

**1. Collect broadly.** Start with one keyword, let *Find related keywords…* (or `yt.py related "<topic>"
--add 30`) grow it into 20–40 phrases, add the subject's best channels as whole channels, and widen the
window:

```toml
keywords_file = "keywords.txt"   # the 20-40 phrases
within = "year"                  # or "any" for evergreen subjects
min_views = 2000
max_results = 0                  # keep every match, not just the newest 25
scan_per_keyword = 500
channels = ["@best-teacher-1", "@best-teacher-2"]
channel_max_videos = 0           # every video of those channels
min_transcript_words = 300
remove_filler_words = true
strip_sound_tags = true
max_transcripts_per_run = 400    # spread a big collection over several days (or use proxies)
```

Repeats are left out of the AI files automatically, and SponsorBlock cuts the ads, so what the AI reads is
the actual teaching.

**2. Distill each video into notes (the "map" step).** Thousands of transcripts are millions of words —
far more than any AI can read at once. So Claude Code first turns every transcript into a short, structured
note:

> For every transcript in `transcripts/day trading/` that has no note yet, write `notes/<same file
> name>.md` with: the claims and techniques taught, every concrete specific (numbers, settings, rules,
> tools, versions), who it's for, warnings and mistakes mentioned, and a 1–5 rating of how specific and
> substantiated it is. Work in batches of 50 with subagents, and keep going until all are done.

A note is about a tenth of the transcript, and the work can be resumed at any time (it skips videos that
already have a note).

**3. Summarize the global knowledge (the "reduce" step).**

> Read all of `notes/`. Group the material into topics. For each topic write `knowledge/<topic>.md`: the
> consensus (and how many videos support it), the disagreements (both sides, with the videos), the best
> explanation (name the video), specific numbers and settings people use, common mistakes, and open
> questions nobody answers well. Then write `knowledge/index.md`: a one-page overview of the whole field
> with links to the topic files.

**4. Build with it.** The knowledge base is now something you — and your AI — can work from:

> Using `knowledge/`, build a checklist / a calculator / a setup script / a Claude skill / a study course
> for … *(see the examples below)*

**Keep it fresh:** leave the daily run on, and once a week ask Claude Code to "write notes for the new
transcripts and update `knowledge/` with anything that changed — list what's new at the top of
`index.md`."

### Five worked examples

**Trading — from 2,000 strategy videos to a testable rulebook.** Collect: "day trading strategy", "opening
range breakout", "order flow", "risk management trading", "prop firm challenge" + related keywords + 10
well-known trading educators' channels. Distill each video into its entry, exit, stop and position-size
rules. Then:

> From `knowledge/`, list every distinct strategy that at least 5 videos teach, each written as exact,
> testable rules (entry, exit, stop, sizing, timeframe, market). Mark which rules the videos disagree on.
> Then write a Python backtest for the three most-taught strategies on daily data, and a pre-trade
> checklist I can print.

What YouTube teachers claim works isn't evidence that it does — that's exactly why the output is a
*backtest*, not a recommendation. (Not financial advice; test before you trade.)

**Local AI setups — from 500 install videos to one setup that works.** Collect: "local llm setup",
"ollama", "llama.cpp", "comfyui workflow", "vllm", "open webui", "gpu for ai" (within = "month": this
field moves fast). Then:

> From `knowledge/`, which hardware and software combinations do people report working, with which
> versions and settings? Build me an install script for Windows with an RTX-class GPU and 32 GB RAM, a
> table of which model sizes fit which VRAM, and a troubleshooting guide of every error message
> mentioned and its fix.

**Vibe coding — from 1,000 workflow videos to a better AI coding setup.** Collect: "vibe coding", "claude
code workflow", "cursor tips", "ai coding agents", "spec driven development" + the top AI-coding channels.
Then:

> From `knowledge/`, what workflows do experienced AI-assisted developers converge on? Write a `CLAUDE.md`
> for my projects with the best practices, a set of reusable prompts for planning, reviewing and
> debugging, and a Claude Code skill (`.claude/skills/<name>/SKILL.md`) that applies the review
> checklist people recommend most.

**SEO — from 1,500 SEO videos to an audit you can run on your own site.** Collect: "seo 2026", "technical
seo", "on page seo", "link building", "local seo", "keyword research", "google algorithm update", "ai
overviews seo", "programmatic seo" + the best-known SEO channels and conference talks, `within = "year"`
(SEO advice ages fast; keep the daily run on to catch algorithm-update coverage). Then:

> From `knowledge/`, separate three kinds of claims: what Google itself has said, what people showed with
> tests or data, and opinion — and how many videos make each. Build an SEO audit checklist ranked by how
> strongly it's supported, a content-brief template for one keyword, and a Python script that crawls my
> site and checks titles, meta descriptions, headings, internal links, image alt text and structured data
> against the checklist. Also list what changed in SEO advice over the last three months.

**Web design — from 1,000 design videos to a design system and a review checklist.** Collect: "web design
tutorial", "landing page design", "ui design tips", "web design mistakes", "typography web design",
"color palette design", "figma web design", "framer", "webflow", "conversion rate optimization" + the top
design and UI channels. Then:

> From `knowledge/`, what rules do designers agree on — spacing, type scale, colour and contrast, visual
> hierarchy, buttons, mobile layout — with the specific numbers they use? Which landing-page sections and
> orders do they say convert best? Write these up as a one-page design system, a design-review checklist,
> and a Claude Code skill that reviews a page against it. Then build a landing-page starter template
> (HTML + CSS) that follows the rules, and critique my current homepage against the checklist.

<details>
<summary><b>60 subjects to do this with — and what to build from each</b></summary>

**Money and business**
| Subject | Collect | Build from the knowledge |
|---|---|---|
| Day trading / swing trading | strategies, setups, risk management, trading psychology | testable rulebook, backtests, pre-trade checklist, journal template |
| Options | strategies, Greeks, wheel, spreads, earnings plays | strategy-picker table, payoff calculator, risk rules |
| Crypto | on-chain analysis, DeFi, wallet security, narratives | security checklist, glossary, narrative tracker |
| Forex / futures | sessions, indicators, prop firms | prop-firm rule comparison, session cheat sheet |
| Long-term investing | valuation, dividend, index investing | valuation checklist, "questions before buying" sheet |
| Personal finance | budgeting, debt payoff, credit, taxes basics | budget template, payoff calculator, money FAQ |
| Real estate | flipping, rentals, BRRRR, house hacking | deal analyzer spreadsheet, inspection checklist |
| E-commerce | Shopify, Amazon FBA, dropshipping, product research | launch checklist, supplier question list, ad-testing plan |
| Starting a business | YC / founder talks, fundraising, pricing | pitch outline, pricing playbook, "mistakes founders regret" |
| Sales | cold calling, objection handling, closing | objection-response library, call scripts, roleplay prompts |
| Marketing & SEO | SEO, paid ads, email, copywriting | content calendar, ad-copy swipe file, SEO checklist |
| Freelancing & agencies | client acquisition, pricing, contracts | proposal template, pricing calculator, onboarding SOP |
| Product reviews | "best X 2026", "X vs Y", long-term reviews | comparison matrix with consensus pros/cons, buying guide |

**AI and software**
| Subject | Collect | Build from the knowledge |
|---|---|---|
| Local LLMs | Ollama, llama.cpp, quantization, GPUs | install script, VRAM table, troubleshooting guide |
| Image & video generation | ComfyUI, Stable Diffusion, Flux, LoRA training | workflow library, settings cheat sheet, prompt patterns |
| AI agents & automation | n8n, Make, agents, MCP servers | automation recipes, agent architecture guide, starter templates |
| Vibe coding / AI coding | Claude Code, Cursor, workflows, prompts | `CLAUDE.md`, prompt library, Claude skills, review checklist |
| Prompt engineering | prompting techniques, evals | prompt templates, an eval checklist |
| Web development | frameworks, deployment, auth, databases | stack decision guide, project boilerplate checklist |
| Cybersecurity (defensive) | home lab, hardening, certifications | hardening checklist, study plan, lab setup guide |
| Data science / ML | courses, Kaggle walkthroughs | study path, technique-by-problem table, code snippets |
| Homelab & self-hosting | Proxmox, Docker, NAS, networking | setup guide, docker-compose collection, backup plan |
| Cloud & DevOps | AWS, Kubernetes, CI/CD | architecture patterns, cost-saving checklist |
| No-code tools | Notion, Airtable, Zapier | template library, automation ideas list |
| Excel & spreadsheets | formulas, dashboards, Power Query | formula cookbook, ready-made templates |

**Creative and media**
| Subject | Collect | Build from the knowledge |
|---|---|---|
| YouTube growth | thumbnails, retention, hooks, algorithm talks | hook library, title formulas, upload checklist |
| Music production | mixing, mastering, sound design, a DAW's tutorials | mixing checklist, plugin-chain presets list, technique index |
| Video editing | Premiere, DaVinci Resolve, color grading | shortcut sheet, editing workflow, LUT/settings guide |
| Photography | composition, lighting, editing, gear | shot checklist, settings-by-situation table, gear guide |
| Writing | fiction craft, screenwriting, copywriting | structure templates, revision checklist, writing prompts |
| 3D printing & CAD | slicer settings, Fusion 360, troubleshooting | settings-by-material table, failure-fix guide |
| Web design | landing pages, UI rules, typography, Figma / Framer / Webflow, conversion | design system, review checklist, starter templates |
| 3D art & game dev | Blender, Unity, Unreal, game design talks | workflow guides, design-pattern library |
| Drawing & design | figure drawing, UI design, typography | practice plan, design-rule checklist |

**Skills, hobbies and life**
| Subject | Collect | Build from the knowledge |
|---|---|---|
| Fitness | programming, hypertrophy, mobility | program templates, exercise form-cue sheet |
| Nutrition & cooking | meal prep, techniques, cuisines | recipe database, technique guide, shopping lists |
| Home improvement / DIY | plumbing, electrical basics, tiling | job checklists, tool lists, "mistakes to avoid" |
| Car maintenance & repair | your model's repairs, diagnostics | maintenance schedule, symptom → cause table |
| Woodworking | joinery, finishes, shop setup | project plans, finish-selection guide |
| Gardening | soil, vegetables, pests, your climate zone | planting calendar, pest → remedy table |
| Language learning | grammar lessons, comprehensible input | vocabulary lists, flashcards, grammar summary |
| Chess | openings, endgames, strategy lectures | opening repertoire file, training plan |
| Video games | builds, meta, patch analysis, speedrun guides | current-meta build sheet, patch-change tracker |
| Board & card games | strategy, deck building | strategy guide, deck archetype table |
| Travel | destination guides, travel hacking, points | itinerary drafts, packing list, points strategy |
| Parenting | sleep, education, development stages | age-by-age guide, FAQ |
| Productivity | systems, tools, habits | personal system design, weekly review template |
| Mental models & thinking | talks, book summaries | mental-model library with examples |
| Public speaking | talks, coaching, TED analyses | speech structure templates, delivery checklist |
| Pets | training, health basics, breeds | training plan, care checklist |

**Learning, news and research**
| Subject | Collect | Build from the knowledge |
|---|---|---|
| University lectures | full course playlists (MIT, Stanford…) | study guide, flashcards, practice exams |
| Science explainers | physics, biology, space | concept map, "explain like I'm 15" notes |
| History | lecture series, documentaries | timeline, cause-and-effect map |
| Tech news | announcements, launches, conference talks | weekly digest, release tracker |
| Market news | daily recaps, earnings coverage | daily brief, "what changed" log |
| Politics & policy | speeches, debates, explainers (all sides) | position map by issue, claim tracker with sources |
| Health & medicine lectures | doctor-run channels, conference talks | question list for your doctor, terminology glossary |
| Law & tax explainers | your country's basics | FAQ, questions for a professional |
| Interviews & podcasts | long-form interviews in a field | quote library, "who believes what" map |
| Conference talks | a field's yearly conferences | state-of-the-field report, trend list |

For health, legal and financial subjects, treat the result as a map of what people say — a starting point
for questions to a professional, not advice.

</details>

<details>
<summary><b>More things to build from a knowledge base</b></summary>

- **A Claude skill** — `.claude/skills/<name>/SKILL.md` that teaches Claude the distilled method, so every
  future session applies it ("review my trade against the rulebook", "debug my ComfyUI error").
- **A `CLAUDE.md` for a project** — the field's best practices as standing instructions.
- **A chatbot over your library** — `yt.py export`, embed the `.jsonl`, answer with sources (RAG).
- **A course** — modules in teaching order, lessons from the best explanations, quizzes, a final project.
- **Flashcards** — "turn `knowledge/` into 300 Anki cards (question; answer; source video) as CSV".
- **Decision tools** — a "which X should I use?" flowchart or questionnaire built from the comparisons.
- **Calculators and spreadsheets** — the formulas people use, made into a sheet you fill in.
- **Setup scripts and configs** — the settings most people converge on, as a script you can run.
- **Checklists and SOPs** — the steps everyone agrees on, with the mistakes people warn about as checks.
- **A consensus map** — every claim, how many videos support or dispute it, and the strongest source each way.
- **A gap report** — questions people ask (titles, comments) that nobody answers well: content ideas.
- **A glossary** — every term in the field with the clearest definition found.
- **A trend report** — compare `knowledge/` month by month: which techniques rise, which fade.
- **A newsletter or blog series** — in your own voice, citing the videos.
- **Datasets** — "extract every (tool, use case, verdict) triple as CSV" for your own analysis.

</details>

<details>
<summary><b>How big, how long, how much: planning a big collection</b></summary>

| Videos | Download time, own connection | With 4 proxies | Proxy data (data saver) | Transcript words (≈15 min each) | Notes after step 2 |
|---|---|---|---|---|---|
| 100 | ~30 min | ~10 min | ~4–10 MB | ~225,000 | ~25,000 words |
| 1,000 | ~5 h | ~1.5 h | ~40–100 MB | ~2.2 million | ~250,000 words |
| 5,000 | ~1 day (spread over several runs) | ~6–7 h | ~200–500 MB | ~11 million | ~1.2 million words |

- **Time:** YouTube allows roughly 300 videos per hour per IP; the tool stays under 200 by default.
  `max_transcripts_per_run` spreads a collection over several daily runs.
- **AI usage:** the map step reads every word once — about 1.3 tokens per word, so 1,000 videos ≈ 3
  million tokens. That's a lot of a subscription's usage: start with the best 100–300 (sort the list by
  views or views per day, skip low *mentions*), check the notes look right, then scale up.
- **Quality filters that pay off:** `min_views` (people found it useful), `min_transcript_words` (no fluff
  clips), *mentions* (actually on topic), `exclude_words` ("reaction", "live", "giveaway"…).
- **Storage:** about 15 KB of text per 15-minute video as `.txt` — 1,000 videos ≈ 15 MB, plus the `.json`.

</details>

---

## Features in detail

### How "newest videos over N views" works

YouTube's search no longer honours "sort by upload date" (checked October 2026). So the tool:

1. asks YouTube for videos uploaded **today / this week / this month / this year** (`within`), once sorted
   by *Popularity* and once by *Relevance* — plus a *Popularity* scan of each narrower window inside it,
   so a video uploaded today isn't crowded out by older, bigger ones — looking through `scan_per_keyword`
   results in each search;
2. drops anything under `min_views` (unless it's rising fast — `rising_views_per_day`), plus Shorts, live
   streams, re-uploads, too-short clips, excluded words…;
3. sorts what's left **newest first** and keeps the top `max_results` per keyword.

Dates in the search come from YouTube's "3 days ago" labels, so they're approximate (marked `~`). When a
transcript is downloaded the exact upload date is filled in — from the video page, or with the data saver
from the channel's small feed (each channel's 15 newest uploads; older videos keep `~`). For exact dates
up front, use `exact_dates = true` (slower) or an API key.

### Every video of a channel or playlist

In the window press *Whole channels…* and paste `@handle`s, channel links or playlist links — or set
`channels = ["@mkbhd"]` in config.toml, or `yt.py channel @mkbhd --max 100`. Choose videos / Shorts /
past live streams, "newest N" (0 = all), a minimum view count and how far back to go. With *Uploaded: This
week* plus the daily schedule you get each new upload automatically.

<img alt="The Whole channels dialog: channels or playlists one per line, which tabs, newest per channel, minimum views and upload window" src="docs/screenshots/channels.png" width="514">

### Related keywords

*Find related keywords…* (or `yt.py related "ai agents"`) asks YouTube what people type after your
keyword, looks at which phrases the top videos' titles share, and at the tags of videos you've already
downloaded — and shows a ranked list you can tick and add.

<img alt="Related keywords: a ranked list with checkboxes, showing where each one was found (suggested, in titles, tags)" src="docs/screenshots/related.png" width="495">

### Trends

**`trends.html`** shows, for each keyword, how many new videos appear per day and how much attention
(views per day) they get, plus the fastest-rising videos of the latest run. It's built from your dated
lists, so it fills in as you run the tool on more days.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/trends_dark.png">
  <img alt="Keyword trends: line charts of new videos per day and views per day for each keyword, with a hover readout" src="docs/screenshots/trends.png">
</picture>

<details>
<summary><b>More: single videos, searching, the daily schedule, SponsorBlock, repeats, comments, rebuilding</b></summary>

- **Just one video (or a list of links)?** Double-click `get_transcript.bat` and paste links — or use
  *Links / a list…* in the window, or `yt.py transcripts my_links.txt`. They go to
  `output\transcripts\single videos\`.
- **Search inside your transcripts:** `search_transcripts.bat`, *Find in transcripts…* or `yt.py find`.
  Every match has a link that opens the video at that moment.
- **Run it every day:** `schedule_daily.bat` (or `yt.py schedule 08:00`) creates a Windows scheduled task
  (log in `output\scheduled_runs.log`). It also updates yt-dlp once a week. `unschedule.bat` removes it.
- **SponsorBlock:** a free, crowd-sourced database of sponsor segments. One tiny lookup per video over
  your own connection (no proxy data). Cut parts are listed in the file header; the `.json` keeps the full
  text. New uploads are checked again over their first days, as people add segments later.
- **Repeats:** a transcript counts as a repeat only if at least 90% of its word sequences appear in
  another saved transcript (checked both ways, and never for very short texts). It's still saved, marked
  *repeat* in the list and `Repeats:` in its file, and left out of the combined files.
- **Top comments:** `top_comments = 20` saves the most-liked comments under each transcript.
- **Rebuilding:** add a format or change `timestamps`, `include_description`, `chapters`,
  `strip_sound_tags`, `remove_filler_words` or `paragraph_seconds`, and the next run rebuilds the files
  from the saved `.json` — nothing is downloaded again. (A description that wasn't saved can't be added
  back this way; it comes with the next download.)
- **Library:** `library.html` lists every video from every run, newest first, with its transcript.

</details>

---

## Settings (config.toml)

Open `config.toml` in Notepad (the window saves its fields there too). The ones most people change:

| Setting | What it does |
|---|---|
| `keywords` | Search terms, each searched separately (or `keywords_file = "keywords.txt"`, one per line). |
| `min_views` | Minimum view count. |
| `within` | `today`, `week`, `month`, `year` or `any`. |
| `max_results` | Newest N matching videos kept per keyword (0 = all). |
| `languages` | Preferred transcript languages in order, e.g. `["en", "es"]`. |
| `formats` | Any of `txt`, `md`, `srt`, `vtt`, `json`. |
| `output_dir` | Where everything is saved, e.g. `'C:\Users\you\Documents\Transcripts'`. |

<details>
<summary><b>All settings</b></summary>

**Search**

| Setting | What it does |
|---|---|
| `rising_views_per_day` | Also keep videos *under* `min_views` that get at least this many views per day (0 = off). |
| `max_views` | Skip videos with more views than this — e.g. 50,000 to find smaller creators (0 = no maximum). |
| `max_age_days` | A finer cut than `within`, e.g. `3`. |
| `published_after`, `published_before` | A date range, e.g. `"2026-10-01"` (with `within = "any"` if older than the window). |
| `scan_per_keyword` | Results looked through in each search (default 150). Raise it for popular topics. |
| `sorts` | Which YouTube orderings are scanned (default `["popularity", "relevance"]`). |
| `cascade_windows` | Also scan today/this week inside a wider window, so fresh uploads aren't crowded out (default on). |
| `include_shorts`, `min_duration`, `max_duration` | Shorts and length filters (seconds). |
| `exclude_live` | Skip streams that are live or upcoming (finished streams are kept). |
| `subtitles_only` | Only videos with captions uploaded by the creator. |
| `title_must_contain`, `exclude_words`, `exclude_channels` | Title/channel filters. |
| `only_channels` | Keep only videos from these channels (names or IDs). |
| `drop_reuploads` | Skip copies re-uploaded by another channel; the most-viewed is kept (default on). |
| `exact_dates` | Look up exact upload dates during the search (slower; asks the channel feeds first). |
| `feed_dates` | Exact dates from each channel's small feed instead of the video page (default on). |
| `backend`, `api_key`, `search_language` | `auto` / `ytdlp` / `api` search; the API key; API result language. |
| `[[keyword_settings]]` | Different settings for one keyword — see below. |

**Whole channels**

| Setting | What it does |
|---|---|
| `channels` | `@handle`s, channel links, channel IDs or playlist links. |
| `channel_tabs` | Any of `videos`, `shorts`, `streams`. |
| `channel_max_videos`, `channel_min_views`, `channel_within` | Newest N per channel (0 = all), minimum views, upload window. |

**Transcripts and text**

| Setting | What it does |
|---|---|
| `download_transcripts` | `false` = make the list only. |
| `allow_other_languages` | If none of `languages` exist, save the video's own language. |
| `translate` | Instead, get YouTube's machine translation into your first language. |
| `prefer_manual` | Creator-uploaded captions before auto-generated ones (default on). |
| `timestamps` | `[mm:ss]` per paragraph in `.txt`, a link to that moment in `.md` and combined files (default off). |
| `include_description` | Save each video's description with its transcript (default off; costs no extra data). |
| `chapters` | Chapter headings when the creator added chapters (default off). |
| `sponsorblock` | SponsorBlock parts to cut — default `["sponsor", "selfpromo", "interaction"]`; also `intro`, `outro`, `preview`, `filler`, `music_offtopic`, `hook`. `[]` = off. |
| `strip_sound_tags` | Remove `[Music]`, `[Applause]`, `(laughs)` and similar. |
| `remove_filler_words` | Remove "um", "uh", "erm", "hmm". |
| `min_transcript_words` | Don't keep transcripts shorter than this. |
| `top_comments` | Also save the N most-liked comments (0 = off; costs some proxy data). |
| `skip_duplicates` | Leave repeats (clips, re-uploads) out of the combined files (default on). |
| `paragraph_seconds` | Paragraph length in the readable files (default 30). |
| `combine`, `combine_max_words` | The `combined\` AI files, split into parts of at most N words (default 80,000; 0 = never split). |
| `max_transcripts_per_run` | Cap downloads per run (0 = no limit); the rest are fetched next time. |
| `retry_failed` | Also retry videos that earlier had no captions or were unavailable. |
| `transcript_methods` | Download methods in order (default `["ytdlp", "api"]`). |

**Output**

| Setting | What it does |
|---|---|
| `organize_by` | Transcript folders by `keyword`, `channel`, `month` (of upload) or `flat`. |
| `file_name` | File names, e.g. `"{title} [{id}]"` — fields `{date} {channel} {title} {id} {views} {keyword} {lang}`. |
| `list_sort` | Order of the list, the downloads and the combined files: `newest`, `views` or `views_per_day`. |
| `open_list_when_done` | Open `video_list.html` after a run. |

**Network, proxies and speed**

| Setting | What it does |
|---|---|
| `proxy`, `proxies`, `proxy_file` | Send YouTube traffic through proxies; a blocked one is swapped for the next. |
| `proxy_for_search`, `proxy_for_transcripts` | Which steps use the proxies. |
| `data_saver` | `auto` (= `max` with proxies), `max`, `lean` (also loads the watch page) or `off`. |
| `proxy_limit_run_mb`, `proxy_limit_month_mb`, `proxy_price_per_gb` | Proxy data limits, and the price to show costs. |
| `proxy_meter` | Count proxy data (default on). |
| `workers`, `workers_per_proxy`, `proxy_rotating` | Parallel downloads (`"auto"` = one per proxy); rotating-proxy detection. |
| `proxy_switch_after` | Videos per proxy before moving to the next: `"auto"` = 10 with a list of 8+ proxies (round-robin, so no IP does much), otherwise stay until blocked; `0` = always stay. |
| `videos_per_hour_per_ip` | Hourly cap per IP (default 200; YouTube allows ~300). Short runs aren't slowed. |
| `delay_seconds`, `request_sleep` | Pause between videos (default 5, randomised) and between yt-dlp's own requests. |
| `max_consecutive_blocks` | Rounds of waiting out YouTube blocks before the run stops (default 4). |
| `cookies_file`, `cookies_from_browser` | YouTube account cookies (see Troubleshooting for the risks). |
| `ytdlp_extractor_args` | Workarounds from yt-dlp's wiki, e.g. `["youtube:player_client=default,-web"]`. |
| `js_runtimes` | JavaScript runtimes yt-dlp may use (default Deno, then Node). |

</details>

**Different settings for one keyword** — add a block like this at the end of the `[search]` part:

```toml
[[keyword_settings]]
keyword = "claude code tutorial"
min_views = 2000
within = "week"
```

---

## Command line

From the tool's folder: `.venv\Scripts\python yt.py …` (or `YouTubeTranscriptTool.exe …`, or options after
`run.bat`). `yt.py run --help` lists every option.

<details>
<summary><b>Examples</b></summary>

```bat
rem two keywords, at least 50,000 views, uploaded this week
run.bat -k "ai agents" -k "mcp servers" --min-views 50000 --within week

rem the 10 newest from the last 24 hours, as .txt and .srt, with timestamps
run.bat --within today --max-age-days 1 -n 10 -f txt -f srt --timestamps

rem big videos, plus new ones that are taking off
run.bat --within week --min-views 100000 --rising 20000

rem save descriptions and chapter headings this time
run.bat --description --chapters

rem the list only, no transcripts
.venv\Scripts\python yt.py search -k "claude code"

rem every video of a channel; the newest 50 Shorts and videos of the last year; a playlist
.venv\Scripts\python yt.py channel @mkbhd
.venv\Scripts\python yt.py channel @mkbhd --tabs videos,shorts --within year --max 50
.venv\Scripts\python yt.py channel "https://www.youtube.com/playlist?list=PL..."

rem related keywords (and add the best 10 to config.toml)
.venv\Scripts\python yt.py related "ai agents" --add 10

rem search on your own connection, transcripts through the proxies, at most 500 MB of proxy data
run.bat --search-direct --data-limit 500

rem transcripts for your own list of links, for links given directly, or for a list made earlier
.venv\Scripts\python yt.py transcripts my_links.txt
.venv\Scripts\python yt.py transcripts https://youtu.be/VIDEO_ID
.venv\Scripts\python yt.py transcripts output\video_list.csv

rem search your transcripts, see what's downloaded, export everything for AI tools
.venv\Scripts\python yt.py find "context window"
.venv\Scripts\python yt.py status
.venv\Scripts\python yt.py export

rem daily run at 08:00 (and remove it), self-test, update yt-dlp
.venv\Scripts\python yt.py schedule 08:00
.venv\Scripts\python yt.py unschedule
.venv\Scripts\python yt.py doctor
.venv\Scripts\python yt.py selfupdate
```

</details>

---

## Proxies, speed and data use

Without proxies the tool downloads one video at a time from your own connection, staying under YouTube's
limit of roughly 300 videos per hour per IP. With proxies it runs one download per proxy in parallel and
switches proxies when YouTube blocks one. Set them in the window under *Advanced settings*, or
`proxy = "http://user:pass@host:port"` (several: `proxies = [...]` or `proxy_file`).

**Data use:** through proxies the data saver makes just two small requests per video — the caption list
and the captions — roughly **40–100 KB per transcript** (an estimate; the log shows your real average).
Searches load bigger pages, so `proxy_for_search = false` saves the most if your own connection isn't
blocked.

### Setting up Decodo residential proxies (recommended)

Residential proxies are home-internet IPs, which YouTube blocks far less than datacenter IPs. Decodo's
residential plans are billed per GB, which suits this tool: with the data saver a transcript costs roughly
40–100 KB, so **a 100 GB plan covers roughly 1–2.5 million transcripts — about 2 million at ~50 KB each.**
(Check your real figure with `yt.py doctor` after setup.)

**The best setup: a list of 10,000+ sticky proxies with 10-minute sessions.** Decodo lets you generate as
many proxy endpoints as you like at no extra cost — you pay only for the GB. Each endpoint keeps one IP
for 10 minutes, then gets a new one. With a list that long:

- the tool works through it round-robin — about 10 videos per endpoint, then on to the one that has
  rested longest — so YouTube never sees more than a handful of requests from any one IP, and blocks
  become rare;
- a blocked endpoint is benched and the video moves straight to the next one, with no waiting;
- each video's two requests (the caption list and the captions) come from the same IP, as they would
  from a real viewer;
- you can run many downloads in parallel (`workers = 8` or more), each on its own IP.

1. **Buy a plan.** Sign up at [decodo.com](https://decodo.com) and choose **Residential proxies** — a
   monthly GB plan (100 GB is plenty for large collections) or pay-as-you-go to try it first.
2. **Find your proxy user.** In the dashboard open **Residential → Proxy setup**. Under **Authentication**
   your first proxy user is already created (username and password; the eye icon shows the password).
   You can set a traffic limit per user there too.
3. **Generate the list.** In the same setup page choose session type **Sticky**, session duration
   **10 minutes**, location *Random* (or a country), protocol **HTTP**, and set the number of
   endpoints to **10,000 or more**. Download the list as **.txt** and save it in the tool's folder as
   **`proxies.txt`** (one `host:port:username:password` per line — the tool reads Decodo's formats as
   they are; `proxies.txt` is never published).
4. **Point the tool at it.** In `config.toml` (open it in Notepad):
   ```toml
   proxy_file = "proxies.txt"     # the 10,000+ sticky endpoints
   proxy = ""                     # leave the single-proxy field empty
   proxy_for_search = false       # search over your own connection: saves the most data
   proxy_for_transcripts = true
   workers = 8                    # parallel downloads, each on its own IP (up to 16)
   proxy_switch_after = "auto"    # 10 videos per endpoint, then the next one (the default)
   proxy_limit_month_mb = 100000  # stop at your plan's 100 GB
   proxy_price_per_gb = 0         # put what you pay per GB here to see each run's cost
   ```
5. **Test it.** Run `update.bat` (or `yt.py doctor`, or `YouTubeTranscriptTool.exe doctor`). It tests the
   first 10 proxies — you should see *youtube.com reachable through proxy* — and then *transcript via
   ytdlp … used NN KB of proxy data*: your real cost per transcript. The run's log then shows how many
   proxies are in use and the data per video.

<details>
<summary><b>Simpler alternative: one rotating address</b></summary>

Decodo's rotating gateway gives a new IP on every connection from a single address: session type
**Rotating**, address **`gate.decodo.com:7000`**. Paste `http://USERNAME:PASSWORD@gate.decodo.com:7000`
into the window's *Proxy* field (under *Advanced settings*), untick *searches*, and in `config.toml` set
`workers_per_proxy = 4` so four downloads share it. The tool recognises the gateway: a block is retried
at once on a fresh connection. It works, but the sticky list above is more reliable.

</details>

If a password contains `@`, `:` or `/`, use the `host:port:user:pass` form (the tool encodes it), or
regenerate a password without them. Decodo's own test: `curl -U "USERNAME:PASSWORD" -x
gate.decodo.com:7000 https://ip.decodo.com/` shows the proxy's IP instead of yours.

<details>
<summary><b>Proxy details: data saver, metering and limits, parallel downloads, rotating proxies</b></summary>

![Advanced settings: results to scan, pause, parallel downloads, data saver, proxy data limits and price; proxy, which steps use it, cookies and API key](docs/screenshots/advanced.png)

* **Setting them up** — `host:port:user:pass` lists from proxy shops work as they are; `socks5://` works
  too. `update.bat` (or `yt.py doctor`) tests every proxy. The password is stored in config.toml.
* **Data saver** — on by default through proxies. It asks YouTube's visionOS app interface for the caption
  list (no 1 MB player download, no watch page) and fetches the captions in the smallest format: roughly
  40–100 KB per transcript, against 0.2–0.4 MB with `data_saver = "lean"` (which also loads the watch
  page) and 1–2 MB with `"off"`. The exact upload date comes from the channel's small feed instead of
  the watch page. If the saver ever misses captions that a fuller method finds, it steps up for the rest
  of the run (max → lean → off). The description and SponsorBlock lookups cost no proxy data.
* **Metering and limits** — every byte through your proxies is counted on your PC and added up per month
  in `output\proxy_usage.json`. The log shows it during and after each run ("Proxy data this run: 9.6 MB,
  about 64 KB per video, 1.3 GB this month"), the window shows it in the bottom bar, `yt.py status` lists
  the last months, and `yt.py doctor` shows what one test video used. Set `proxy_limit_month_mb` (e.g.
  2000 for a 2 GB plan) and/or `proxy_limit_run_mb`: when a limit is reached no new video is started.
  `proxy_price_per_gb` adds the cost. Your provider measures a little differently — leave some headroom.
* **Parallel downloads** — `workers = "auto"` runs one download per proxy (at most 4; a number up to 16
  overrides), each with its own pause and hourly budget, so 4 proxies are roughly 4x faster. A blocked or
  dead proxy is benched and its video goes to another worker. A long list (8+ proxies) is worked through
  round-robin, 10 videos per proxy (`proxy_switch_after`). Without proxies it stays one at a time,
  because parallel requests from one home IP get blocked quickly. With cookies it's always one at a time.
* **Rotating proxies** (one address, a new IP per connection, e.g. Webshare's `-rotate`) are recognised
  automatically: a block is retried at once on a fresh connection, and `workers_per_proxy = 3` runs
  several workers through that one address.
* **Residential or datacenter?** Datacenter IPs are cheaper but YouTube blocks many of them; residential
  IPs get blocked far less. With the data saver, a pay-per-GB residential plan goes a long way.

</details>

<details>
<summary><b>Optional: YouTube Data API key</b> (exact dates, true newest-first)</summary>

1. Go to <https://console.cloud.google.com/>, create a project.
2. "APIs & Services" → "Library" → enable **YouTube Data API v3**.
3. "Credentials" → "Create credentials" → **API key**. Copy it into `api_key = "..."` in config.toml
   (or the *YouTube API key* field under *Advanced settings*).

The free quota is 10,000 units/day; each keyword costs roughly 300–600 units with default settings. If the
quota runs out mid-run, the tool switches to key-less search automatically.

</details>

---

## Troubleshooting

If YouTube changes something and it stops working: double-click **`update.bat`** (or download the newest
`.exe`). `yt.py doctor` checks the whole setup.

<details>
<summary><b>Common problems and fixes</b></summary>

* **"Sign in to confirm you're not a bot" / blocked / 429** — YouTube is rate-limiting your connection.
  Wait an hour and run again (finished videos are skipped), lower `videos_per_hour_per_ip`, or use proxies.
  If it keeps happening, cookies from a YouTube account help, but carry a risk: YouTube may suspend an
  account used this way, so use a spare one. yt-dlp's advice: open a *private* browser window, sign in to
  YouTube, open `https://www.youtube.com/robots.txt` in that same tab, export the cookies with a
  "cookies.txt" browser extension, close the private window, and set
  `cookies_file = 'C:\Users\you\Documents\cookies.txt'`. (`cookies_from_browser = "firefox"` is simpler,
  but the cookies of an open browser go stale.) Don't combine account cookies with rotating proxies.
* **Lots of "FAIL … PO token" or empty transcripts** — run `update.bat` and make sure Deno is installed
  (`winget install DenoLand.Deno`); `yt.py doctor` shows whether it's found. These videos are retried on
  the next run. If it persists, see yt-dlp's [PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide).
* **"No captions"** — the video has none. YouTube creates auto-captions a while after upload, so videos
  less than 3 days old are tried again on the next run.
* **"config.toml has a mistake … (at line N, column M)"** — look at that line in Notepad. Usual causes: a
  Windows path in double quotes (use single quotes: `output_dir = 'D:\YouTube'`), or a text value without
  quotes (`within = "week"`, not `within = week`).
* **"video_list.csv is open in another program"** — it was open in Excel, so `video_list (new).csv` was
  saved instead. Close Excel before the next run.
* **"Stopping: N videos in a row failed"** — usually the internet connection dropped. Run again; only
  unfinished videos are retried.
* **Dates marked `~`** — approximate (from "3 days ago" labels). Videos older than a channel's 15 newest
  uploads keep them unless you set `exact_dates = true` or an API key.
* **Python errors on setup** — you need Python 3.11+; `setup.bat` picks the newest it finds.

</details>

## How it works (for the curious)

* Search: [yt-dlp](https://github.com/yt-dlp/yt-dlp)'s YouTube search with YouTube's own filter codes
  (`yt_transcripts/sp_params.py`), or the YouTube Data API v3.
* Transcripts: yt-dlp first (it copes with YouTube's "proof of origin" checks by using other player
  clients, with Deno solving YouTube's JavaScript), then
  [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) as a fallback.
* Sponsor segments: [SponsorBlock](https://sponsor.ajay.app). Exact dates with the data saver: YouTube's
  channel feeds.
* Tests: `.venv\Scripts\python -m pip install pytest` then `.venv\Scripts\python -m pytest` (offline; some
  replay real YouTube responses saved in `tests/fixtures`).

Please use it responsibly: it's meant for personal research. Respect creators and YouTube's terms.
