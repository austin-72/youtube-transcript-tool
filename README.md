# YouTube Transcript Tool

Searches YouTube for your keywords, keeps the **newest videos above a view threshold**, saves that
list (CSV, JSON and a clickable HTML page), then **downloads every video's transcript** to your computer.

No API key needed. (An optional free YouTube API key gives exact dates and true newest-first ordering.)

---

## Quick start (Windows)

1. **Python 3.11 or newer** is needed. If you're not sure, just do step 2 — if Python is missing,
   setup offers to install it for you (via winget). To do it by hand: get it from
   <https://www.python.org/downloads/> and tick **"Add python.exe to PATH"**.
2. Double-click **`setup.bat`**. It creates a private environment in this folder, installs what's needed,
   offers to install *Deno* (a small helper yt-dlp uses for YouTube — say **Y**) and a Desktop shortcut,
   and runs a self-test.
3. Open **`config.toml`** in Notepad: set your `keywords`, `min_views` and `within`. Save.
4. Double-click **`run.bat`** — or **`gui.bat`** for a window where you can type everything instead.

Your results appear in the **`output`** folder:

```
output/
├── video_list.html        ← open this: sortable list with thumbnails and links to each transcript
├── video_list.csv         ← same list for Excel
├── library.html           ← every video from every run so far, with its transcript
├── video_list.json
├── transcripts/
│   └── ai agents/                                   (one folder per keyword)
│       ├── 2026-10-27 - Some Channel - Video title [VIDEO_ID].txt
│       └── 2026-10-27 - Some Channel - Video title [VIDEO_ID].json
├── combined/transcripts_2026-10-28_2315 - ai agents.md   ← AI-ready: a keyword's transcripts in one file
├── lists/                 ← a dated copy of every list you've made
├── manifest.json          ← remembers what's done, so re-runs skip finished videos
└── last_run.log
```

A transcript `.txt` file looks like this:

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
Chapters: 6

Description:
<the video's description>
------------------------------------------------------------

== Introduction (00:00) ==

<the spoken text, grouped into paragraphs of roughly 30 seconds each>

<next paragraph ...>

== Installing Python (01:42) ==
...
```

If the creator added chapters, each one starts with its own heading. The `.md` format also has clickable
timestamps and properties at the top (title, channel, date, views, keywords) that **Obsidian** and similar
note apps show and can search. The files in `combined\` are made for **AI tools**: all of a keyword's
transcripts from one run in a single file, split into parts small enough for ChatGPT, Claude, Gemini or
NotebookLM — upload one and ask "what are the main points across these videos?".

Besides title, channel, date and views, the list shows **views/day** (how fast a video is growing) and
**mentions** (how often the transcript actually says your keyword's main words — a quick clickbait detector).
Click *preview* under a title to read the start of its transcript right in the list.

Run it again any time: videos that already have a transcript are skipped, so only new ones are fetched,
and videos no earlier search had found get a **NEW** badge in the list. (Tick an extra format later, or change
`txt_timestamps`, `strip_sound_tags` or `paragraph_seconds`, and the files are rebuilt from the saved `.json`
copies — nothing is downloaded again. Keep `json` in `formats` for this.)
If YouTube changes something and it stops working, double-click **`update.bat`**.

**Every video of a channel?** In the window press *Whole channels…* and paste `@handle`s, channel links or
playlist links — or `run.bat` with `channels = ["@mkbhd"]` in config.toml, or
`.venv\Scripts\python yt.py channel @mkbhd --max 100`. You choose videos / Shorts / past live streams,
"newest N" (0 = all), a minimum view count and how far back to go. The channel's transcripts get their own
folder, and with *Uploaded: This week* plus the daily schedule you get each new upload automatically.

**Not sure what to search for?** *Find related keywords…* (or `yt.py related "ai agents"`) asks YouTube
what people type after your keyword, looks at which phrases the top videos' titles share, and at the tags
of videos you've already downloaded — and shows a ranked list you can tick and add to your keywords.

**Just one video?** Double-click **`get_transcript.bat`** and paste its link (or several links) —
or use *Links / a list…* in the window.
Those transcripts go to `output\transcripts\single videos\`.

**Search inside your transcripts:** double-click **`search_transcripts.bat`** (or use *Find in transcripts…*
in the window). Every match comes with a link that opens the video at that exact moment.

**Run it automatically every day:** double-click **`schedule_daily.bat`** and pick a time. It creates a
Windows scheduled task (runs while you're logged in; log in `output\scheduled_runs.log`). It also
updates yt-dlp once a week, so it keeps working when YouTube changes something.
**`unschedule.bat`** removes it.

---

## How "newest videos over N views" works

YouTube's search no longer honours "sort by upload date" (checked October 2026). So the tool:

1. asks YouTube for videos uploaded **today / this week / this month / this year** (`within`),
   once sorted by *Popularity* and once by *Relevance* — plus a *Popularity* scan of each narrower window
   inside it, so a video uploaded today isn't crowded out by older, bigger ones — looking through
   `scan_per_keyword` results in each search;
2. drops anything under `min_views` (unless it's rising fast — see `rising_views_per_day`), plus Shorts,
   live streams, re-uploads of the same video, too-short clips, excluded words…;
3. sorts what's left **newest first** and keeps the top `max_results` per keyword.

Dates come from YouTube's "3 days ago" labels, so they're approximate (marked `~`). When yt-dlp fetches a
transcript it also learns the exact upload date and the list is updated. For exact dates up front, use `exact_dates = true`
(slower) or an API key (below).

## The settings (config.toml)

| Setting | What it does |
|---|---|
| `keywords` | Search terms, each searched separately. Also `keywords_file = "keywords.txt"` (one per line), added to `keywords`. |
| `min_views` | Minimum view count. |
| `rising_views_per_day` | Also keep videos *under* `min_views` that are getting at least this many views per day — catches uploads a few hours old that are taking off (0 = off). |
| `within` | `today`, `week`, `month`, `year` or `any`. `max_age_days = 3` gives a finer cut. |
| `max_results` | Newest N matching videos kept per keyword (0 = all). |
| `scan_per_keyword` | How many results to look through in each individual search. Raise it for popular topics. |
| `include_shorts`, `min_duration`, `max_duration` | Length filters (seconds). |
| `title_must_contain`, `exclude_words`, `exclude_channels` | Title/channel filters. |
| `only_channels` | If set, keep only videos from these channels (names or IDs). |
| `drop_reuploads` | Skip copies of a video re-uploaded by another channel (same title and length); only the most-viewed copy is kept. On by default. |
| `cascade_windows` | Also scan today/this week inside a wider window, so fresh uploads aren't crowded out (default on). |
| `subtitles_only` | Only videos with captions uploaded by the creator. |
| `languages` | Preferred transcript languages in order, e.g. `["en", "es"]`. |
| `allow_other_languages` | If none of those exist, save the video's own language. |
| `translate` | Instead, get YouTube's machine translation into your first language. |
| `formats` | Any of `txt`, `md` (with clickable timestamps), `srt`, `vtt`, `json` (all segments + metadata). |
| `output_dir` | Where everything is saved, e.g. `'C:\Users\you\Documents\Transcripts'`. |
| `delay_seconds` | Pause between videos (default 5, randomised), per worker. |
| `proxy`, `proxies`, `proxy_file` | Send all YouTube traffic through a proxy; with several, a blocked one is swapped for the next (see Troubleshooting). |
| `workers`, `workers_per_proxy` | Parallel downloads: `"auto"` = one per proxy (one without proxies), or a number. |
| `videos_per_hour_per_ip` | Hourly cap per IP (default 200; YouTube allows ~300). Short runs aren't slowed. |
| `ytdlp_extractor_args` | Paste workarounds from yt-dlp's wiki, e.g. `["youtube:player_client=default,-web"]`. |
| `max_transcripts_per_run` | Cap downloads per run (0 = no limit); the rest are fetched next time. |
| `strip_sound_tags` | Remove `[Music]`, `[Applause]`, `(laughs)` and similar from the text. |
| `txt_timestamps` | Put `[mm:ss]` at the start of each paragraph in .txt files. |
| `max_views` | Skip videos with more views than this — e.g. 50,000 to find smaller creators (0 = no maximum). |
| `published_after`, `published_before` | Only videos uploaded in a date range, e.g. `"2026-10-01"` (with `within = "any"` if it's older than the window). |
| `channels`, `channel_tabs`, `channel_max_videos`, `channel_min_views`, `channel_within` | Whole channels or playlists (see *Every video of a channel?* above). |
| `remove_filler_words` | Remove "um", "uh", "erm", "hmm" from the text. |
| `min_transcript_words` | Don't keep transcripts shorter than this (music videos, short intros). |
| `organize_by` | Transcript folders by `keyword`, `channel`, `month` (of upload) or `flat`. |
| `file_name` | File names, e.g. `"{title} [{id}]"` — fields `{date} {channel} {title} {id} {views} {keyword} {lang}`. |
| `list_sort` | Order of the list and downloads: `newest`, `views` or `views_per_day`. |
| `proxy_for_search`, `proxy_for_transcripts` | Which steps use the proxies (e.g. search on your own connection, transcripts through proxies). |
| `proxy_limit_run_mb`, `proxy_limit_month_mb`, `proxy_price_per_gb` | Proxy data limits and the price, to show costs (see *Proxy data* below). |
| `data_saver` | Fewer bytes per video through proxies: `auto` (on with proxies), `on`, `off` or `max`. |
| `combine`, `combine_max_words` | AI-ready files in `combined/`: one per keyword per run, split into parts of at most 80,000 words (fits ChatGPT, Claude, Gemini or a NotebookLM source; 0 = never split). |

**Different settings for one keyword** — add a block like this to config.toml (at the end of the
`[search]` part), one per keyword:

```toml
[[keyword_settings]]
keyword = "claude code tutorial"
min_views = 2000
within = "week"
```

## Command line

From this folder (after setup), `.venv\Scripts\python yt.py …` — or add the options to `run.bat`:

```bat
rem two keywords, at least 50,000 views, uploaded this week
run.bat -k "ai agents" -k "mcp servers" --min-views 50000 --within week

rem the 10 newest from the last 24 hours, as .txt and .srt
run.bat --within today --max-age-days 1 -n 10 -f txt -f srt

rem big videos, plus new ones that are taking off
run.bat --within week --min-views 100000 --rising 20000

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

rem search your transcripts (with links to the exact moment), see what's downloaded, export everything
.venv\Scripts\python yt.py find "context window"
.venv\Scripts\python yt.py status
.venv\Scripts\python yt.py export

rem check the setup, update yt-dlp, and list every option
.venv\Scripts\python yt.py doctor
.venv\Scripts\python yt.py selfupdate
.venv\Scripts\python yt.py run --help
```

## Optional: YouTube Data API key (exact dates, true newest-first)

1. Go to <https://console.cloud.google.com/>, create a project.
2. "APIs & Services" → "Library" → enable **YouTube Data API v3**.
3. "Credentials" → "Create credentials" → **API key**. Copy it into `api_key = "..."` in config.toml
   (or the *YouTube API key* field under *Advanced settings* in the window).

The free quota is 10,000 units/day; each keyword costs roughly 300–600 units with default settings.
If the quota runs out mid-run, the tool switches to key-less search automatically.

## Troubleshooting

* **Using a proxy** — set `proxy = "http://user:pass@host:port"` in config.toml (or the *Proxy* field under
  *Advanced settings* in the window, or `--proxy` on the command line). Everything — search, transcripts, the API — then goes
  through it. Give several (`proxies = [...]`, a `proxy_file` with one per line, or several in the field
  separated by spaces) and the tool switches to the next one as soon as YouTube blocks the current one.
  `host:port:user:pass` lists from proxy shops work as they are; `socks5://` works too.
  Run `update.bat` (or `yt.py doctor`) to test every proxy. Note the password is stored in config.toml.
* **Proxy data (how much, and limits)** — every byte that goes through your proxies is counted on your PC
  and added up per month in `output\proxy_usage.json`. The log shows it during and after each run
  ("Proxy data this run: 42 MB, about 0.5 MB per video, 1.3 GB this month"), the window shows it in the
  bottom bar, and `yt.py status` lists the last months. Set `proxy_limit_month_mb` (e.g. 2000 for a 2 GB
  plan) and/or `proxy_limit_run_mb`: when a limit is reached no new video is started and the rest wait for
  the next run. `proxy_price_per_gb` adds the cost. (Your provider measures a little differently, so
  leave some headroom.) Ways to use less: `proxy_for_search = false` (searching and channel listing use
  your own connection — they're the big pages, and YouTube rarely blocks them), and the **data saver**,
  on by default through proxies: it asks YouTube for the captions with one small request instead of
  three bigger ones, skips the 1 MB player download, and fetches the smallest caption format. If it ever
  misses captions that the full method finds, it switches itself off for the run. `data_saver = "max"`
  also skips the watch page (smallest, but exact upload dates may be missing). `yt.py doctor` shows how
  much one test video used through your proxy.
* **Faster: parallel downloads** — with proxies, `workers = "auto"` (the default) runs one download per
  proxy at the same time (at most 4; set a number up to 16 to override), each with its own pause and hourly
  budget, so 4 proxies are roughly 4x faster. A blocked or dead proxy is benched and its video goes to
  another worker. *Rotating* services (one address, a new IP per connection, e.g. Webshare's `-rotate`) are
  recognised automatically: a block is retried at once on a fresh connection, and `workers_per_proxy = 3`
  runs several workers through that one address. Without proxies it stays one-at-a-time, because parallel
  requests from one home IP get blocked quickly. Keyword searches run in parallel the same way. When cookies
  are set it always runs one at a time (one account from several IPs at once risks a ban).
* **How fast can it go?** YouTube allows logged-out use roughly 300 videos per hour per IP. The tool keeps
  each IP under `videos_per_hour_per_ip` (200) and pauses `delay_seconds` (5) between videos. Short runs are
  never slowed down by the hourly cap; long runs pause only when needed.
* **"Sign in to confirm you're not a bot" / blocked / 429** — YouTube is rate-limiting your connection.
  Wait an hour and run again (finished videos are skipped), lower `videos_per_hour_per_ip`, or use proxies.
  If it keeps happening, cookies from a YouTube account help, but carry a risk: YouTube may suspend an
  account used this way, so use a spare one. yt-dlp's own advice: open a *private* browser window, sign in
  to YouTube, then open `https://www.youtube.com/robots.txt` in that same tab, export the cookies with a
  "cookies.txt" browser extension into a file, close the private window, and set
  `cookies_file = 'C:\Users\you\Documents\cookies.txt'`. (`cookies_from_browser = "firefox"` is simpler, but YouTube keeps changing the cookies of an
  open browser, so they go stale.) Don't combine account cookies with rotating proxies.
* **Lots of "FAIL … PO token" or empty transcripts** — run `update.bat`, and make sure Deno is installed
  (`winget install DenoLand.Deno`). The `yt.py doctor` check shows whether it's found. These videos are
  retried automatically on the next run. If it persists, YouTube is demanding a "proof of origin" token
  for your connection; yt-dlp's [PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide)
  explains the optional provider plugins.
* **"No captions"** — the video has no captions (auto or manual). YouTube creates auto-captions a while
  after upload, so for videos less than 3 days old the tool tries again on the next run.
* **"config.toml has a mistake … (at line N, column M)"** — open config.toml in Notepad and look at that line.
  Usual causes: a Windows path in double quotes (use single quotes: `output_dir = 'D:\YouTube'`), or a text
  value without quotes (`within = "week"`, not `within = week`).
* **"video_list.csv is open in another program"** — the list was open in Excel, so a `video_list (new).csv`
  was saved next to it instead. Close Excel before the next run.
* **"Stopping: N videos in a row failed"** — usually the internet connection dropped. Just run again; only
  unfinished videos are retried.
* **Python errors on setup** — you need Python 3.11+. Uninstalling old versions isn't necessary; `setup.bat`
  picks the newest it finds.

## How it works (for the curious)

* Search: [yt-dlp](https://github.com/yt-dlp/yt-dlp)'s YouTube search with YouTube's own filter codes
  (`yt_transcripts/sp_params.py`), or the YouTube Data API v3.
* Transcripts: first [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) (fast),
  then yt-dlp (handles YouTube's newer "proof of origin" token requirement that breaks simple scrapers).
* Tests: `.venv\Scripts\python -m pip install pytest` then `.venv\Scripts\python -m pytest`
  (they replay real YouTube responses captured in `tests/fixtures`, so they work offline).

Please use it responsibly: it's meant for personal research. Respect creators and YouTube's terms.
