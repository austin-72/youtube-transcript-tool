"""trends.html: how each keyword (and channel) develops over time, from the dated lists in lists/.

For every day with a run (the last run of the day counts), per keyword:
  * new videos       - videos that no earlier run had found (how much is being published)
  * views per day    - the summed views/day of the matching videos (how much attention the topic gets)
  * matching videos  - how many videos passed your filters
plus the fastest-rising videos of the latest run. Nothing is downloaded - it only reads your lists.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path

from .models import Video

MAX_SERIES = 8  # more keywords than this: the 8 with the most attention are charted, all are in the table
_STAMP = re.compile(r"^(\d{4}-\d{2}-\d{2})_(\d{4})_")


def collect(out_dir: Path) -> dict:
    """{"days": [...], "series": {kw: {"new": [...], "attention": [...], "count": [...]}}, "risers": [...]}"""
    lists = Path(out_dir) / "lists"
    per_day: dict[str, dict[str, tuple[str, Path]]] = {}  # day -> list kind -> (stamp, path) of its last run
    for f in sorted(lists.glob("*_list.json")) if lists.exists() else []:
        m = _STAMP.match(f.name)
        if not m:
            continue
        kind = f.name[m.end():]
        day = m.group(1)
        per_day.setdefault(day, {})[kind] = (m.group(1) + m.group(2), f)
    days = sorted(per_day)
    series: dict[str, dict[str, list]] = {}
    risers: list[dict] = []
    for i, day in enumerate(days):
        videos: dict[str, Video] = {}
        for _, path in per_day[day].values():
            try:
                rows = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for d in rows if isinstance(rows, list) else []:
                try:
                    v = Video.from_dict(d)
                except (TypeError, ValueError):
                    continue
                videos[v.video_id] = v
        ref = dt.datetime.fromisoformat(day + "T23:59:59+00:00")
        for v in videos.values():
            vpd = v.views_per_day(ref) or 0.0
            # the first day is everyone's first sighting: count only what that run itself called new
            new = v.is_new if i == 0 else (v.first_seen or "")[:10] == day
            for kw in [k for k in v.keyword.split("; ") if k] or ["(no keyword)"]:
                s = series.setdefault(kw, {"new": [0] * len(days), "attention": [0.0] * len(days),
                                           "count": [0] * len(days)})
                s["count"][i] += 1
                s["new"][i] += int(new)
                s["attention"][i] += vpd
        if i == len(days) - 1:
            ranked = sorted(videos.values(), key=lambda v: -(v.views_per_day(ref) or 0))[:15]
            risers = [{"id": v.video_id, "title": v.title, "channel": v.channel, "views": v.views,
                       "vpd": round(v.views_per_day(ref) or 0), "keyword": v.keyword,
                       "published": v.published[:10]} for v in ranked]
    for s in series.values():
        s["attention"] = [round(x) for x in s["attention"]]
    return {"days": days, "series": series, "risers": risers}


def render(data: dict) -> str:
    days, series = data["days"], data["series"]
    latest = {k: (s["attention"][-1] if s["attention"] else 0) for k, s in series.items()}
    charted = sorted(series, key=lambda k: -latest[k])[:MAX_SERIES]
    payload = {"days": days, "keys": charted, "series": {k: series[k] for k in charted}}
    e = html.escape
    table_rows = []
    show_days = days[-14:]
    for k in sorted(series, key=lambda k: -latest[k]):
        s = series[k]
        cells = "".join(f"<td>{s['new'][days.index(d)]}</td>" for d in show_days)
        table_rows.append(f"<tr><th scope='row'>{e(k)}</th>{cells}<td>{s['attention'][-1]:,}</td>"
                          f"<td>{s['count'][-1]}</td></tr>")
    riser_rows = "".join(
        f"<tr><td><a href='https://www.youtube.com/watch?v={e(r['id'])}' target='_blank' rel='noopener'>"
        f"{e(r['title'])}</a><div class='muted'>{e(r['channel'])} · {e(r['keyword'])}</div></td>"
        f"<td class='n'>{r['vpd']:,}</td><td class='n'>{(r['views'] or 0):,}</td><td>{e(r['published'])}</td></tr>"
        for r in data["risers"])
    note = ""
    if len(days) < 2:
        note = ("<p class='note'>Trends need runs on at least two different days - run again tomorrow "
                "(or set up the daily schedule) and the lines appear.</p>")
    more = (f"<p class='muted'>Charting the {MAX_SERIES} keywords with the most attention today; all "
            f"{len(series)} are in the table.</p>" if len(series) > MAX_SERIES else "")
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    return _PAGE.format(
        generated=e(generated), n_days=len(days), first=e(days[0] if days else "-"), last=e(days[-1] if days else "-"),
        note=note, more=more, data=json.dumps(payload).replace("<", "\\u003c"),
        head_days="".join(f"<th scope='col'>{e(d[5:])}</th>" for d in show_days),
        table_rows="".join(table_rows) or "<tr><td>No lists yet.</td></tr>",
        riser_rows=riser_rows or "<tr><td colspan='4'>No videos yet.</td></tr>",
        latest=e(days[-1] if days else "-"))


def write_trends(out_dir: Path) -> Path | None:
    data = collect(Path(out_dir))
    if not data["days"]:
        return None
    path = Path(out_dir) / "trends.html"
    from .writers import _write_list_file

    return _write_list_file(path, render(data))


_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Keyword trends</title>
<style>
.viz-root {{ color-scheme: light;
  --page:#f9f9f7; --surface-1:#fcfcfb; --text-primary:#0b0b0b; --text-secondary:#52514e; --muted:#898781;
  --grid:#e1e0d9; --axis:#c3c2b7; --border:rgba(11,11,11,0.10); --link:#2a78d6;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s5:#e87ba4; --s6:#008300; --s7:#6250d6; --s8:#e34948; }}
@media (prefers-color-scheme: dark) {{ :root:where(:not([data-theme="light"])) .viz-root {{ color-scheme: dark;
  --page:#0d0d0d; --surface-1:#1a1a19; --text-primary:#f0efec; --text-secondary:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --border:rgba(255,255,255,0.10); --link:#86b6ef;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181; --s6:#008300; --s7:#9085e9; --s8:#e66767; }} }}
:root[data-theme="dark"] .viz-root {{ color-scheme: dark;
  --page:#0d0d0d; --surface-1:#1a1a19; --text-primary:#f0efec; --text-secondary:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --border:rgba(255,255,255,0.10); --link:#86b6ef;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181; --s6:#008300; --s7:#9085e9; --s8:#e66767; }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--page); color:var(--text-primary); font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:20px 16px 40px; }}
h1 {{ font-size:20px; margin:0 0 4px; }} h2 {{ font-size:15px; margin:0 0 2px; }}
.muted, .sub {{ color:var(--text-secondary); }} .sub {{ margin:0 0 10px; font-size:13px; }}
.note {{ background:var(--surface-1); border:1px solid var(--border); border-radius:8px; padding:10px 12px; }}
.card {{ background:var(--surface-1); border:1px solid var(--border); border-radius:10px; padding:14px 16px 10px; margin:14px 0; }}
.chart {{ position:relative; width:100%; }}
.legend {{ display:flex; flex-wrap:wrap; gap:4px 14px; margin:6px 0 2px; font-size:13px; color:var(--text-secondary); }}
.legend span {{ display:inline-flex; align-items:center; gap:6px; }} .legend i {{ width:14px; height:2px; border-radius:1px; display:inline-block; }}
.tip {{ position:absolute; pointer-events:none; background:var(--surface-1); border:1px solid var(--border); border-radius:8px;
  padding:6px 9px; font-size:12px; box-shadow:0 2px 8px rgba(0,0,0,.12); display:none; min-width:150px; z-index:2; }}
.tip .d {{ color:var(--muted); margin-bottom:3px; }} .tip .r {{ display:flex; align-items:center; gap:6px; }}
.tip .r i {{ width:10px; height:2px; display:inline-block; }} .tip .r b {{ font-variant-numeric:tabular-nums; min-width:44px; }}
.tip .r span {{ color:var(--text-secondary); }}
table {{ border-collapse:collapse; width:100%; font-size:13px; }}
th, td {{ padding:6px 8px; border-bottom:1px solid var(--grid); text-align:left; vertical-align:top; }}
td.n, th.n, .tbl td {{ text-align:right; font-variant-numeric:tabular-nums; }} .tbl th[scope=row] {{ text-align:left; font-weight:500; }}
.wrap {{ overflow-x:auto; }} a {{ color:var(--link); text-decoration:none; }} a:hover {{ text-decoration:underline; }}
details summary {{ cursor:pointer; color:var(--text-secondary); margin:6px 0; }}
svg text {{ fill:var(--muted); font-size:11px; }} svg .end {{ fill:var(--text-secondary); font-size:12px; }}
</style></head><body class="viz-root"><main>
<h1>Keyword trends</h1>
<p class="sub">{n_days} day(s) with runs, {first} to {last} · from the lists in the <i>lists</i> folder · generated {generated}</p>
{note}{more}
<section class="card"><h2>New videos per day</h2><p class="sub">Videos no earlier run had found - how much is being published.</p>
<div class="chart" id="c-new"></div></section>
<section class="card"><h2>Attention: views per day of the matching videos</h2><p class="sub">Summed views/day of every video that passed your filters - how much people are watching the topic.</p>
<div class="chart" id="c-att"></div></section>
<section class="card"><h2>Fastest-rising videos ({latest})</h2><div class="wrap"><table>
<thead><tr><th>Video</th><th class="n">Views/day</th><th class="n">Views</th><th>Uploaded</th></tr></thead><tbody>{riser_rows}</tbody></table></div></section>
<section class="card"><details><summary>Show as a table (new videos per day, last 14 days)</summary><div class="wrap"><table class="tbl">
<thead><tr><th>Keyword</th>{head_days}<th>Views/day now</th><th>Matching now</th></tr></thead><tbody>{table_rows}</tbody></table></div></details></section>
</main>
<script type="application/json" id="data">{data}</script>
<script>
(function () {{
  var D = JSON.parse(document.getElementById('data').textContent);
  var css = getComputedStyle(document.body);
  function color(i) {{ return css.getPropertyValue('--s' + (i + 1)).trim(); }}
  function fmt(n) {{ n = Math.round(n); return n >= 1e6 ? (n / 1e6).toFixed(1).replace(/\\.0$/, '') + 'M'
    : n >= 1e4 ? Math.round(n / 1e3) + 'K' : n.toLocaleString(); }}
  function niceStep(raw) {{ if (raw <= 1) return 1; var p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p;
    return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; }}
  function label(k, v) {{ return (k.length > 18 ? k.slice(0, 17) + '\\u2026' : k) + ' ' + fmt(v); }}
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) {{ var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }}
  function draw(id, metric) {{
    var host = document.getElementById(id); host.textContent = '';
    var keys = D.keys, days = D.days, n = days.length;
    if (!keys.length) {{ host.textContent = 'No data yet.'; return; }}
    var W = host.clientWidth || 800, H = 260, L = 48, T = 10, B = 26, R = 16;
    if (keys.length <= 4) keys.forEach(function (k) {{ var vals = D.series[k][metric];
      R = Math.max(R, label(k, vals[n - 1]).length * 6.6 + 18); }});
    R = Math.min(R, W * 0.35);
    var max = 0; keys.forEach(function (k) {{ D.series[k][metric].forEach(function (v) {{ if (v > max) max = v; }}); }});
    var step = niceStep(Math.max(max, 1) * 1.05 / 4), top = step * Math.max(1, Math.ceil(Math.max(max, 1) * 1.05 / step));
    var pw = W - L - R, ph = H - T - B;
    function x(i) {{ return L + (n === 1 ? pw / 2 : i * pw / (n - 1)); }}
    function y(v) {{ return T + ph - v / top * ph; }}
    var svg = el('svg', {{ width: W, height: H, role: 'img', 'aria-label': id === 'c-new' ? 'New videos per day by keyword' : 'Views per day by keyword' }}, host);
    for (var gv = 0; gv <= top + 1e-9; gv += step) {{ var g = gv;
      el('line', {{ x1: L, x2: L + pw, y1: y(gv), y2: y(gv), stroke: g ? css.getPropertyValue('--grid') : css.getPropertyValue('--axis'), 'stroke-width': 1 }}, svg);
      el('text', {{ x: L - 6, y: y(gv) + 4, 'text-anchor': 'end' }}, svg).textContent = fmt(gv); }}
    var every = Math.max(1, Math.ceil(n / Math.max(2, Math.floor(pw / 70))));
    for (var i = 0; i < n; i += every) el('text', {{ x: x(i), y: H - 8, 'text-anchor': 'middle' }}, svg).textContent = days[i].slice(5);
    keys.forEach(function (k, s) {{ var vals = D.series[k][metric], d = '';
      vals.forEach(function (v, i) {{ d += (i ? 'L' : 'M') + x(i).toFixed(1) + ',' + y(v).toFixed(1); }});
      if (n > 1) el('path', {{ d: d, fill: 'none', stroke: color(s), 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }}, svg);
      el('circle', {{ cx: x(n - 1), cy: y(vals[n - 1]), r: 4, fill: color(s), stroke: css.getPropertyValue('--surface-1'), 'stroke-width': 2 }}, svg);
      if (keys.length <= 4) {{ var t = el('text', {{ x: x(n - 1) + 8, y: y(vals[n - 1]) + 4, 'class': 'end' }}, svg);
        t.textContent = label(k, vals[n - 1]); }} }});
    if (keys.length < 2) return addHover();
    var leg = document.createElement('div'); leg.className = 'legend';
    keys.forEach(function (k, s) {{ var sp = document.createElement('span'), i = document.createElement('i');
      i.style.background = color(s); sp.appendChild(i); sp.appendChild(document.createTextNode(k)); leg.appendChild(sp); }});
    host.appendChild(leg);
    addHover();
    function addHover() {{
    var cross = el('line', {{ y1: T, y2: T + ph, stroke: css.getPropertyValue('--axis'), 'stroke-width': 1, visibility: 'hidden' }}, svg);
    var tip = document.createElement('div'); tip.className = 'tip'; host.appendChild(tip);
    var hit = el('rect', {{ x: L, y: T, width: pw, height: ph, fill: 'transparent', tabindex: 0 }}, svg);
    function show(i) {{ cross.setAttribute('x1', x(i)); cross.setAttribute('x2', x(i)); cross.setAttribute('visibility', 'visible');
      tip.textContent = ''; var dd = document.createElement('div'); dd.className = 'd'; dd.textContent = days[i]; tip.appendChild(dd);
      keys.map(function (k, s) {{ return [k, s, D.series[k][metric][i]]; }}).sort(function (a, b) {{ return b[2] - a[2]; }})
        .forEach(function (r) {{ var row = document.createElement('div'); row.className = 'r';
          var key = document.createElement('i'); key.style.background = color(r[1]);
          var b = document.createElement('b'); b.textContent = fmt(r[2]);
          var sp = document.createElement('span'); sp.textContent = r[0];
          row.appendChild(key); row.appendChild(b); row.appendChild(sp); tip.appendChild(row); }});
      tip.style.display = 'block';
      var left = x(i) + 12; if (left + tip.offsetWidth > W) left = x(i) - tip.offsetWidth - 12;
      tip.style.left = Math.max(0, left) + 'px'; tip.style.top = T + 'px'; }}
    function hide() {{ cross.setAttribute('visibility', 'hidden'); tip.style.display = 'none'; }}
    var cur = n - 1;
    hit.addEventListener('pointermove', function (ev) {{ var r = svg.getBoundingClientRect();
      cur = n === 1 ? 0 : Math.max(0, Math.min(n - 1, Math.round((ev.clientX - r.left - L) / pw * (n - 1)))); show(cur); }});
    hit.addEventListener('pointerleave', hide); hit.addEventListener('blur', hide);
    hit.addEventListener('focus', function () {{ show(cur); }});
    hit.addEventListener('keydown', function (ev) {{ if (ev.key === 'ArrowLeft') cur = Math.max(0, cur - 1);
      else if (ev.key === 'ArrowRight') cur = Math.min(n - 1, cur + 1); else return; ev.preventDefault(); show(cur); }});
    }}
  }}
  function all() {{ draw('c-new', 'new'); draw('c-att', 'attention'); }}
  all(); var t; window.addEventListener('resize', function () {{ clearTimeout(t); t = setTimeout(all, 150); }});
}})();
</script></body></html>
"""
