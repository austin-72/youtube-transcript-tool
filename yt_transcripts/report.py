"""A self-contained, sortable HTML version of the video list (opens in any browser, works offline)."""

from __future__ import annotations

import datetime as dt
import html
import os
from pathlib import Path
from urllib.parse import quote

from .models import Video
from .utils import format_duration

STATUS_TEXT = {
    "ok": ("Transcript", "ok"),
    "no_transcript": ("No captions", "none"),
    "unavailable": ("Unavailable", "none"),
    "blocked": ("Blocked - retry later", "warn"),
    "error": ("Failed - retry later", "warn"),
    "po_token": ("Needs YouTube token - retried later", "warn"),
}


def _rel_link(target: str, base: Path) -> str:
    if not target:
        return ""
    try:
        rel = os.path.relpath(target, base)
    except ValueError:  # different drive on Windows
        return Path(target).resolve().as_uri()
    return quote(rel.replace(os.sep, "/"))


PREVIEW_CHARS = 600

WINDOW_TEXT = {"today": "in the last day", "day": "in the last day", "week": "in the last week",
               "month": "in the last month", "year": "in the last year", "any": "at any time"}


def search_summary(s) -> str:
    """One plain line saying which search made this list (so an old list still explains itself)."""
    kws = s.all_keywords()
    if not kws:
        return ""
    shown = ", ".join(f"\u201c{k}\u201d" for k in kws[:6]) + (f" and {len(kws) - 6} more" if len(kws) > 6 else "")
    parts = [f"Searched {shown}", f"at least {s.min_views:,} views"]
    if s.rising_views_per_day:
        parts[-1] += f" (or {s.rising_views_per_day:,}+ views/day)"
    days = s.effective_max_age_days() if s.max_age_days else None  # the cut-off actually applied
    parts.append(f"uploaded in the last {days:g} days" if days else WINDOW_TEXT.get(s.within, s.within))
    if s.max_results:
        parts.append(f"newest {s.max_results} per keyword")
    if not s.include_shorts:
        parts.append("no Shorts")
    if s.only_channels:
        parts.append(f"only {len(s.only_channels)} channel{'s' if len(s.only_channels) != 1 else ''}")
    line = " · ".join(parts)
    if s.keyword_settings:
        line += " (some keywords have their own settings)"
    return line


def transcript_preview(path: str, limit: int = PREVIEW_CHARS) -> str:
    """The first few sentences of a saved transcript (any format this tool writes), for the list page."""
    import json
    import re

    p = Path(path) if path else None
    if not p or not p.is_file():
        return ""
    try:
        raw = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    suffix = p.suffix.lower()
    if suffix == ".json":
        try:
            text = json.loads(raw).get("transcript", {}).get("text", "")
        except (ValueError, AttributeError):
            text = ""
    elif suffix == ".txt":
        sep = "\n" + "-" * 60 + "\n"  # the header line; a description above it may contain dashes too
        text = raw.rsplit(sep, 1)[1] if sep in raw else raw
        text = "\n".join(ln for ln in text.splitlines() if not re.fullmatch(r"== .* ==", ln.strip()))
    elif suffix == ".md":
        text = raw.split("\n## Transcript\n", 1)[-1]
        text = "\n".join(ln for ln in text.splitlines() if not ln.startswith("#"))  # chapter headings
        text = re.sub(r"\[(\d+:)?\d+:\d+\]\([^)]*\)", " ", text)
        text = re.sub(r"\\([#>*+.)-])", r"\1", text)  # undo the escapes that keep text from becoming headings
    else:  # srt / vtt: drop cue numbers and timing lines
        text = "\n".join(ln for ln in raw.splitlines()
                         if ln.strip() and "-->" not in ln and not ln.strip().isdigit() and ln.strip() != "WEBVTT")
    text = re.sub(r"\[(\d+:)?\d+:\d+\]", " ", text)  # [mm:ss] paragraph stamps
    text = " ".join(text.split())
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + " …"
    return text


def _keywords_of(v: Video) -> list[str]:
    return [k for k in (v.keyword or "").split("; ") if k]


def render_html(videos: list[Video], base_dir: Path, title: str = "YouTube video list", summary: str = "") -> str:
    e = html.escape
    rows = []
    all_kws: list[str] = []
    for v in videos:
        for k in _keywords_of(v):
            if k not in all_kws:
                all_kws.append(k)
    for v in videos:
        pub = v.published[:10] if v.published else ""
        approx = "" if v.published_exact or not pub else ' <span class="approx" title="approximate">~</span>'
        st_text, st_cls = STATUS_TEXT.get(v.transcript_status, ("", ""))
        new_badge = '<span class="pill new">NEW</span> ' if v.is_new else ""
        vpd = v.views_per_day()
        link = _rel_link(v.transcript_file, base_dir)
        status = (f'<a class="pill {st_cls}" href="{link}">{st_text}</a>' if link and v.transcript_status == "ok"
                  else (f'<span class="pill {st_cls}">{e(st_text)}</span>' if st_text else ""))
        preview = transcript_preview(v.transcript_file) if v.transcript_status == "ok" else ""
        preview_html = (f'<details class="pv"><summary>preview</summary><p>{e(preview)}</p></details>'
                        if preview else "")
        kw_attr = e("|" + "|".join(k.lower() for k in _keywords_of(v)) + "|")
        rows.append(
            f'<tr data-kw="{kw_attr}">'
            f'<td><a href="https://www.youtube.com/watch?v={e(v.video_id)}" target="_blank" rel="noopener">'
            f'<img loading="lazy" src="https://i.ytimg.com/vi/{e(v.video_id)}/mqdefault.jpg" alt="" onerror="this.style.visibility=\'hidden\'"></a></td>'
            f'<td class="t">{new_badge}'
            f'<a href="https://www.youtube.com/watch?v={e(v.video_id)}" target="_blank" rel="noopener">{e(v.title)}</a>'
            f'<div class="ch">{e(v.channel)}</div>{preview_html}</td>'
            f'<td class="d" data-v="{e(v.published)}">{e(pub)}{approx}</td>'
            f'<td class="n" data-v="{v.views if v.views is not None else -1}">{f"{v.views:,}" if v.views is not None else "?"}</td>'
            f'<td class="n" data-v="{round(vpd) if vpd is not None else -1}">{f"{round(vpd):,}" if vpd is not None else ""}</td>'
            f'<td class="n" data-v="{v.duration_seconds or 0}">{e(format_duration(v.duration_seconds))}</td>'
            f"<td>{e(v.keyword)}</td>"
            f'<td class="n" data-v="{v.keyword_mentions if v.keyword_mentions is not None else -1}">'
            f'{v.keyword_mentions if v.keyword_mentions is not None else ""}</td>'
            f'<td data-v="{e(v.transcript_status)}">{status}</td>'
            "</tr>"
        )
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    new_count = sum(1 for v in videos if v.is_new)
    counts: dict[str, int] = {}
    for v in videos:
        if v.transcript_status:
            counts[v.transcript_status] = counts.get(v.transcript_status, 0) + 1
    status_line = " · ".join(f"{n} {STATUS_TEXT.get(k, (k,))[0].split(' - ')[0].lower()}"
                             for k, n in sorted(counts.items(), key=lambda kv: -kv[1]))
    if counts.get("ok"):
        status_line = status_line.replace(f"{counts['ok']} transcript", f"{counts['ok']} with transcript", 1)
    kw_select = ""
    if len(all_kws) > 1:
        opts = "".join(f'<option value="{e(k.lower())}">{e(k)}</option>' for k in all_kws)
        kw_select = (f'<label>Keyword <select id="kw"><option value="">all ({len(all_kws)})</option>{opts}'
                     "</select></label>")
    summary_html = f'<div class="meta">{e(summary)}</div>' if summary else ""
    status_html = f'<div class="meta">Transcripts: {e(status_line)}</div>' if status_line else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<style>
:root {{ --bg:#fafaf9; --fg:#1c1917; --muted:#78716c; --line:#e7e5e4; --card:#fff; --accent:#c2410c;
        --ok:#15803d; --okbg:#dcfce7; --warn:#a16207; --warnbg:#fef9c3; --nonebg:#f5f5f4; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#1c1917; --fg:#f5f5f4; --muted:#a8a29e; --line:#44403c; --card:#292524;
        --accent:#fb923c; --ok:#86efac; --okbg:#14532d; --warn:#fde68a; --warnbg:#713f12; --nonebg:#3a3532; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; font:14px/1.45 "Segoe UI", system-ui, sans-serif; background:var(--bg); color:var(--fg); }}
header {{ padding:20px 24px 8px; }}
h1 {{ margin:0 0 4px; font-size:20px; }}
.meta {{ color:var(--muted); }} .legend {{ font-size:12px; margin-top:2px; }}
select {{ padding:6px 8px; border:1px solid var(--line); border-radius:6px; background:var(--card); color:var(--fg); max-width:260px; }}
.bar {{ padding:8px 24px 12px; display:flex; gap:12px; align-items:center; flex-wrap:wrap; }}
.bar label {{ color:var(--muted); display:flex; gap:4px; align-items:center; }}
input[type=search] {{ padding:7px 10px; border:1px solid var(--line); border-radius:6px; background:var(--card); color:var(--fg); min-width:260px; }}
.wrap {{ padding:0 24px 32px; overflow-x:auto; }}
table {{ border-collapse:collapse; width:100%; background:var(--card); border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
th, td {{ padding:8px 10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
th {{ position:sticky; top:0; background:var(--card); cursor:pointer; user-select:none; white-space:nowrap; font-weight:600; }}
th:hover {{ color:var(--accent); }}
th.sorted::after {{ content:" ▼"; font-size:10px; }} th.sorted.asc::after {{ content:" ▲"; }}
td.d {{ white-space:nowrap; }}
td.n {{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }}
td img {{ width:120px; height:68px; object-fit:cover; border-radius:4px; display:block; background:var(--nonebg); }}
td.t a {{ color:var(--fg); text-decoration:none; font-weight:500; }} td.t a:hover {{ color:var(--accent); text-decoration:underline; }}
.ch {{ color:var(--muted); font-size:13px; margin-top:2px; }}
.pv summary {{ color:var(--muted); font-size:12px; cursor:pointer; margin-top:4px; }}
.pv p {{ font-size:13px; line-height:1.45; margin:4px 0 0; max-width:60ch; }}
.approx {{ color:var(--muted); }}
.pill {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; white-space:nowrap; text-decoration:none; }}
.pill.ok {{ background:var(--okbg); color:var(--ok); }} .pill.warn {{ background:var(--warnbg); color:var(--warn); }}
.pill.none {{ background:var(--nonebg); color:var(--muted); }}
.pill.new {{ background:var(--accent); color:var(--card); font-weight:600; margin-right:4px; }}
@media (max-width:700px) {{ #t td:first-child, #t th:first-child {{ display:none; }} td.t {{ min-width:180px; }} header, .bar, .wrap {{ padding-left:12px; padding-right:12px; }} }}
</style></head><body>
<header><h1>{e(title)}</h1><div class="meta">{len(videos)} videos{f" ({new_count} new since last run)" if new_count else ""} · generated {generated} · ~ = approximate date</div>
{summary_html}{status_html}<div class="meta legend"><b>Views/day</b> = how fast it's growing · <b>Mentions</b> = how often the transcript says the keyword's main words (0 on a popular video often means clickbait)</div></header>
<div class="bar"><input type="search" id="q" placeholder="Filter by title, channel, keyword or transcript start…" aria-label="Filter">
{kw_select}
<label><input type="checkbox" id="onlynew"> New only</label>
<label><input type="checkbox" id="onlytx"> Has transcript</label>
<span class="meta" id="count"></span></div>
<div class="wrap"><table id="t"><thead><tr>
<th data-k="none"></th><th data-k="text">Title</th><th data-k="v" class="sorted">Published</th><th data-k="vn">Views</th>
<th data-k="vn" title="Views divided by days since upload">Views/day</th>
<th data-k="vn">Length</th><th data-k="text">Keyword</th>
<th data-k="vn" title="How many times the transcript says the keyword">Mentions</th><th data-k="v">Transcript</th>
</tr></thead><tbody>
{''.join(rows)}
</tbody></table></div>
<script>
(function () {{
  var t = document.getElementById('t'), tb = t.tBodies[0];
  var q = document.getElementById('q'), onlyNew = document.getElementById('onlynew'),
      onlyTx = document.getElementById('onlytx'), count = document.getElementById('count'),
      kw = document.getElementById('kw');
  function apply() {{
    var term = q.value.toLowerCase(), shown = 0, k = kw ? kw.value : '';
    Array.prototype.forEach.call(tb.rows, function (r) {{
      var ok = r.textContent.toLowerCase().indexOf(term) >= 0
        && (!k || (r.getAttribute('data-kw') || '').indexOf('|' + k + '|') >= 0)
        && (!onlyNew.checked || r.querySelector('.pill.new'))
        && (!onlyTx.checked || r.querySelector('.pill.ok'));
      r.style.display = ok ? '' : 'none';
      if (ok) shown++;
    }});
    count.textContent = shown + ' shown';
  }}
  if (kw) kw.addEventListener('change', apply);
  q.addEventListener('input', apply); onlyNew.addEventListener('change', apply); onlyTx.addEventListener('change', apply);
  apply();
  Array.prototype.forEach.call(t.tHead.rows[0].cells, function (th, i) {{
    var k = th.getAttribute('data-k'); if (k === 'none') return;
    th.addEventListener('click', function () {{
      var asc = th.classList.contains('sorted') && !th.classList.contains('asc');
      Array.prototype.forEach.call(t.tHead.rows[0].cells, function (c) {{ c.classList.remove('sorted', 'asc'); }});
      th.classList.add('sorted'); if (asc) th.classList.add('asc');
      var rows = Array.prototype.slice.call(tb.rows);
      rows.sort(function (a, b) {{
        var x = a.cells[i], y = b.cells[i], r;
        if (k === 'vn') r = parseFloat(x.getAttribute('data-v')) - parseFloat(y.getAttribute('data-v'));
        else if (k === 'v') r = (x.getAttribute('data-v') || '').localeCompare(y.getAttribute('data-v') || '');
        else r = x.textContent.localeCompare(y.textContent);
        return asc ? r : -r;
      }});
      rows.forEach(function (r) {{ tb.appendChild(r); }});
    }});
  }});
}})();
</script></body></html>
"""
