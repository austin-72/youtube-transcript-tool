"""Find related keywords: what people actually type into YouTube, and the phrases popular videos use.

Three sources, combined into one ranked list:

* YouTube's search suggestions (the drop-down under the search box) for the keyword, for the keyword
  followed by each letter a-z, and for "how to <keyword>", "best <keyword>"... - about 30 tiny requests.
* Phrases that keep coming up in the titles of the top search results for the keyword (one search).
* Tags of videos you've already downloaded for that keyword (read from the saved .json files - free).

    yt.py related "ai agents"             # show the list (and save it to output/related_keywords/)
    yt.py related "ai agents" --add 10    # ...and add the top 10 to the keywords in config.toml
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .config import Settings

log = logging.getLogger("yt_transcripts")

SUGGEST_URL = "https://suggestqueries.google.com/complete/search"
PREFIXES = ("how to", "best", "what is", "why")
_STOP = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "is", "are", "be", "you", "your", "my",
    "i", "we", "it", "this", "that", "how", "what", "why", "when", "vs", "at", "by", "from", "do", "does", "can",
    "will", "new", "our", "just", "all", "out", "up", "get", "go", "now", "here", "its", "it's", "so", "not",
    "no", "yes", "me", "us", "they", "them", "their", "these", "those", "has", "have", "was", "were", "if", "but",
    "part", "ep", "episode", "video", "videos", "official", "full", "free", "live", "2024", "2025", "2026", "2027",
    "shorts", "short", "|", "-", "&",
}


@dataclass
class Related:
    phrase: str
    score: float = 0.0
    sources: set[str] = field(default_factory=set)
    seed: str = ""


def parse_suggest(text: str) -> list[str]:
    """Suggestions from either the plain JSON or the JSONP form of the suggest endpoint."""
    t = (text or "").strip()
    m = re.match(r"^[\w.$]+\((.*)\)\s*;?$", t, re.S)  # window.google.ac.h([...])
    if m:
        t = m.group(1)
    try:
        data = json.loads(t)
    except ValueError:
        return []
    items = data[1] if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list) else []
    out = []
    for it in items:
        s = it[0] if isinstance(it, list) and it else it
        if isinstance(s, str) and s.strip():
            out.append(_norm(s))
    return out


def _norm(phrase: str) -> str:
    return " ".join(re.sub(r"[\"“”]", " ", phrase.lower()).split())


def _session(s: Settings):
    import requests

    from . import netmeter

    sess = requests.Session()
    proxies = s.stage_proxies("search")
    if proxies:
        url = netmeter.route(proxies[0])
        sess.trust_env = False
        sess.proxies = {"http": url, "https": url}
    sess.headers["User-Agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 "
                                  "Firefox/140.0")
    return sess


def suggestions(seed: str, s: Settings, *, get: Callable | None = None, pause: float = 0.15,
                should_stop: Callable[[], bool] | None = None) -> dict[str, float]:
    """phrase -> score from YouTube's autocomplete (higher in the drop-down and for more prompts = higher)."""
    hl = (s.search_language or (s.languages[0] if s.languages else "en")).split("-")[0] or "en"
    queries = [seed] + [f"{seed} {c}" for c in "abcdefghijklmnopqrstuvwxyz"] + [f"{p} {seed}" for p in PREFIXES]
    if get is None:
        session = _session(s)

        def get(q):  # noqa: E306
            r = session.get(SUGGEST_URL, params={"client": "firefox", "ds": "yt", "q": q, "hl": hl}, timeout=10)
            r.raise_for_status()
            return r.text
    scores: dict[str, float] = defaultdict(float)
    failures = 0
    for i, q in enumerate(queries):
        if should_stop and should_stop():
            break
        try:
            found = parse_suggest(get(q))
        except Exception as e:  # noqa: BLE001 - one failed prompt is fine
            failures += 1
            log.debug("suggestions for %r failed: %s", q, e)
            if failures >= 3 and failures > i // 2:
                log.warning("  YouTube's suggestions aren't answering (%s) - skipping them", e)
                break
            continue
        weight = 2.0 if i == 0 else 1.0  # the plain keyword's own suggestions count double
        for rank, ph in enumerate(found):
            scores[ph] += weight * (1.0 - rank / (len(found) + 1))
        if pause:
            time.sleep(pause)
    return dict(scores)


def title_phrases(videos, seed: str) -> dict[str, float]:
    """2-4 word phrases that several result titles share, weighted by how popular those videos are."""
    seed_words = set(_norm(seed).split())
    counts: dict[str, float] = defaultdict(float)
    seen_in: dict[str, set] = defaultdict(set)
    for v in videos:
        words = re.findall(r"[\w'+#.-]+", (v.title or "").lower())
        words = [w.strip(".-'") for w in words]
        weight = 1.0 + math.log10(max(v.views or 1, 1)) / 3
        grams = set()
        for n in (2, 3, 4):
            for j in range(len(words) - n + 1):
                g = words[j:j + n]
                if g[0] in _STOP or g[-1] in _STOP or any(not w for w in g):
                    continue
                if all(w in seed_words for w in g) or sum(w not in _STOP for w in g) < 2:
                    continue
                grams.add(" ".join(g))
        for g in grams:
            counts[g] += weight
            seen_in[g].add(v.video_id)
    return {g: c for g, c in counts.items() if len(seen_in[g]) >= 2}


def tag_phrases(out_dir: Path, seed: str, limit_files: int = 3000) -> dict[str, float]:
    """Tags of saved transcripts (their .json files) whose keyword is this seed."""
    root = Path(out_dir) / "transcripts"
    if not root.exists():
        return {}
    want = _norm(seed)
    counts: Counter = Counter()
    for i, f in enumerate(root.rglob("*.json")):
        if i >= limit_files:
            break
        try:
            video = json.loads(f.read_text(encoding="utf-8")).get("video", {})
        except (OSError, ValueError, AttributeError):
            continue
        kws = [_norm(k) for k in str(video.get("keyword", "")).split(";")]
        if want not in kws:
            continue
        for t in video.get("tags") or []:
            t = _norm(str(t))
            if 2 <= len(t) <= 60 and t != want:
                counts[t] += 1
    return {t: float(n) for t, n in counts.items() if n >= 2}


def _scaled(d: dict[str, float]) -> dict[str, float]:
    top = max(d.values(), default=0.0)
    return {k: v / top for k, v in d.items()} if top else {}


def find_related(seeds: list[str], s: Settings, *, use_titles: bool = True, search_fn: Callable | None = None,
                 get: Callable | None = None, pause: float = 0.15,
                 should_stop: Callable[[], bool] | None = None) -> list[Related]:
    """Ranked related keywords for all seeds (your own keywords are left out)."""
    import copy

    mine = {_norm(k) for k in s.all_keywords()} | {_norm(x) for x in seeds}
    merged: dict[str, Related] = {}
    for seed in seeds:
        if should_stop and should_stop():
            break
        log.info("Related keywords for %r ...", seed)
        sources: list[tuple[str, dict[str, float], float]] = []
        sug = suggestions(seed, s, get=get, pause=pause, should_stop=should_stop)
        log.info("  %d from YouTube's search suggestions", len(sug))
        sources.append(("suggested", _scaled(sug), 1.0))
        if use_titles:
            try:
                ts = copy.copy(s)
                ts.sorts, ts.cascade_windows, ts.include_shorts = ["relevance"], False, False
                ts.scan_per_keyword = min(s.scan_per_keyword, 80)
                if search_fn is None:
                    from . import netmeter
                    from .search_ytdlp import search_keyword

                    proxies = s.stage_proxies("search")
                    ts.proxy = netmeter.route(proxies[0]) if proxies else ""
                    videos = search_keyword(seed, ts, should_stop=should_stop)
                else:
                    videos = search_fn(seed, ts)
                tp = title_phrases(videos, seed)
                log.info("  %d from the titles of %d top videos", len(tp), len(videos))
                sources.append(("in titles", _scaled(tp), 0.7))
            except Exception as e:  # noqa: BLE001 - suggestions alone are still useful
                log.warning("  title search failed: %s", e)
        tags = tag_phrases(Path(s.output_dir), seed)
        if tags:
            log.info("  %d from the tags of videos you downloaded", len(tags))
            sources.append(("tags", _scaled(tags), 0.5))
        for name, scores, weight in sources:
            for ph, sc in scores.items():
                if ph in mine or len(ph) < 3:
                    continue
                r = merged.setdefault(ph, Related(ph, seed=seed))
                r.score += sc * weight
                r.sources.add(name)
    for r in merged.values():
        if len(r.sources) > 1:
            r.score *= 1.0 + 0.5 * (len(r.sources) - 1)  # found by several sources: a stronger signal
    return sorted(merged.values(), key=lambda r: (-r.score, r.phrase))


def save_related(items: list[Related], out_dir: Path, seeds: list[str]) -> tuple[Path, Path]:
    """keywords.txt-style list (one per line, ready for keywords_file) and a CSV with scores and sources."""
    import csv
    import io

    from .utils import safe_filename

    folder = Path(out_dir) / "related_keywords"
    folder.mkdir(parents=True, exist_ok=True)
    stem = safe_filename(f"{dt.datetime.now():%Y-%m-%d_%H%M} {', '.join(seeds)}", 90)
    txt = folder / f"{stem}.txt"
    txt.write_text("# related keywords - delete the ones you don't want, then use this file as keywords_file\n"
                   + "".join(f"{r.phrase}\n" for r in items), encoding="utf-8")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["keyword", "score", "found in", "from"])
    for r in items:
        w.writerow([r.phrase, f"{r.score:.2f}", " + ".join(sorted(r.sources)), r.seed])
    csv_path = folder / f"{stem}.csv"
    csv_path.write_text(buf.getvalue(), encoding="utf-8-sig")
    return txt, csv_path


def cmd_related(s: Settings, seeds: list[str], *, max_items: int = 40, use_titles: bool = True, add: int = 0,
                config_path: Path | None = None, out=print) -> int:
    from .cli import metered

    seeds = [x.strip() for x in seeds if x and x.strip()]
    if not seeds:
        out("Which keyword? e.g.  yt.py related \"ai agents\"")
        return 2
    with metered(s, "related"):
        items = find_related(seeds, s, use_titles=use_titles)
    if not items:
        out("Nothing found - check your internet connection (or try a broader keyword).")
        return 1
    shown = items[:max_items]
    out(f"\n{'#':>3}  {'Keyword':<48} {'Score':>6}  Found in")
    out("-" * 80)
    for i, r in enumerate(shown, 1):
        out(f"{i:>3}  {r.phrase[:48]:<48} {r.score:6.2f}  {' + '.join(sorted(r.sources))}")
    txt, csv_path = save_related(items, Path(s.output_dir), seeds)
    out(f"\nSaved all {len(items)}: {txt.resolve()}\n       and {csv_path.resolve()}")
    if add > 0:
        added = add_keywords(config_path, [r.phrase for r in items[:add]])
        out(f"Added {len(added)} keyword(s) to {config_path}: {', '.join(added)}" if added
            else "Those keywords are already in your list.")
    return 0


def add_keywords(config_path: Path | None, new: list[str]) -> list[str]:
    """Append keywords to the `keywords` list in config.toml (not to keywords_file), skipping duplicates."""
    from .config import load_config, update_config_file

    if config_path is None:
        return []
    cfg = Path(config_path)
    if not cfg.exists():  # not the example: its sample keywords would become active too
        cfg.write_text("# YouTube Transcript Tool settings (see config.example.toml for all of them)\n",
                       encoding="utf-8")
    current = load_config(cfg).get("keywords") or []
    if isinstance(current, str):
        current = [x.strip() for x in current.split(",") if x.strip()]
    have = {str(k).lower() for k in current}
    added = []
    for k in new:
        if k.lower() not in have:
            have.add(k.lower())
            added.append(k)
    if added:
        update_config_file(cfg, {"keywords": [str(k) for k in current] + added})
    return added
