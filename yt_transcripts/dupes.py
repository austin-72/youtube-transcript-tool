"""Spot transcripts that repeat another video's text - clips cut from a longer video, re-uploads,
mirrors - so the AI files don't feed the same words twice (and one video's claims don't look like a
consensus of several).

Built to have no false positives: two transcripts only count as the same when at least 90% of the
shorter one's 8-word sequences appear, in the same words, in the other one - and only for transcripts
of 100+ words. Different videos about the same topic share phrases, but not 90% of their
8-word sequences. Missing a duplicate (say, uploaded and auto captions that differ a little) is fine;
calling two different videos the same never should happen.

An index of small fingerprints (a sample of each transcript's sequence hashes) is kept in
output/duplicate_index.json, so new videos are also checked against everything downloaded before.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path

log = logging.getLogger("yt_transcripts")

SHINGLE = 8  # words per sequence
SAMPLE_MOD = 32  # keep the hashes divisible by this as the fingerprint (same rule for every text)
MIN_SHINGLES = 100
CONTAINMENT = 0.90  # share of the shorter text's sequences that must appear in the other one
INDEX_FILE = "duplicate_index.json"


_CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff]")


def words(text: str) -> list[str]:
    """Words in any script; Chinese/Japanese/Korean characters count one each (no spaces between words)."""
    text = (text or "").lower()
    out = []
    for tok in re.findall(r"\w+(?:'\w+)?", text):
        if _CJK.search(tok):
            out.extend(ch for ch in re.findall(r"\w", tok))  # one "word" per character
        else:
            out.append(tok)
    return out


def shingles(text: str) -> set[int]:
    w = words(text)
    out = set()
    for i in range(len(w) - SHINGLE + 1):
        h = hashlib.blake2b("\x1f".join(w[i:i + SHINGLE]).encode(), digest_size=8).digest()
        out.add(int.from_bytes(h, "big"))
    return out


def _short_hash(h: int) -> int:
    return h >> 32  # the fingerprint keeps 32 bits: a pre-filter only, the decision uses the full hashes


def fingerprint(sh: set[int]) -> list[int]:
    return sorted({_short_hash(h) for h in sh if h % SAMPLE_MOD == 0})


class DuplicateIndex:
    def __init__(self, out_dir: Path):
        self.path = Path(out_dir) / INDEX_FILE
        self.prints: dict[str, list[int]] = {}
        self.sizes: dict[str, int] = {}
        self.titles: dict[str, str] = {}
        self.by_hash: dict[int, list[str]] = {}
        self.dirty = False
        self.loaded = False

    def _load(self) -> None:
        """Read the index file - only when the first video of a run needs checking."""
        if self.loaded:
            return
        self.loaded = True
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            for vid, rec in (data.get("videos") or {}).items():
                self._add(vid, [int(x) for x in rec.get("fp", [])], int(rec.get("n", 0)), str(rec.get("title", "")))
        except FileNotFoundError:
            pass
        except (OSError, ValueError, TypeError, AttributeError) as e:
            log.debug("duplicate index not readable (%s) - starting a new one", e)

    def _add(self, vid: str, fp: list[int], n: int, title: str) -> None:
        old = self.prints.get(vid)
        for h in old or []:
            ids = self.by_hash.get(h)
            if ids and vid in ids:
                ids.remove(vid)
        self.prints[vid], self.sizes[vid], self.titles[vid] = fp, n, title
        for h in fp:
            self.by_hash.setdefault(h, []).append(vid)

    def check_and_add(self, vid: str, title: str, text: str, load_text,
                      skip=None) -> tuple[tuple[str, str] | None, list[str]]:
        """Add this transcript to the index. Returns (repeats, contained):
        repeats   - (video_id, title) of an indexed video whose text contains this one, or None;
        contained - indexed videos whose text this one contains (e.g. a clip that came first).
        `load_text(video_id)` gives another video's saved transcript text, for the exact check;
        `skip(video_id)` -> True leaves that video out (e.g. one already marked as a repeat of this one)."""
        self._load()
        sh = shingles(text)
        fp = fingerprint(sh)
        repeats, contained = None, []
        if len(sh) >= MIN_SHINGLES and fp:
            counts: dict[str, int] = {}
            for h in fp:
                for other in self.by_hash.get(h, ()):
                    if other != vid:
                        counts[other] = counts.get(other, 0) + 1
            if skip is not None:
                counts = {o: c for o, c in counts.items() if not skip(o)}
            cache: dict[str, set[int]] = {}

            def other_shingles(o: str) -> set[int]:
                if o not in cache:
                    cache[o] = shingles(load_text(o) or "")
                return cache[o]
            # (1) this text inside a longer (or equal) one: most of OUR fingerprint is in theirs
            bigger = sorted((o for o, c in counts.items()
                             if c >= 0.8 * len(fp) and self.sizes.get(o, 0) >= len(sh) * 0.9), key=lambda o: -counts[o])
            for o in bigger[:5]:
                osh = other_shingles(o)
                if len(osh) >= len(sh) * 0.9 and len(sh & osh) >= CONTAINMENT * len(sh):
                    repeats = (o, self.titles.get(o, ""))
                    break
            # (2) a shorter one inside this text: most of THEIR fingerprint is in ours
            if repeats is None:
                for o, c in counts.items():
                    ofp = self.prints.get(o) or []
                    if not ofp or c < 0.8 * len(ofp) or self.sizes.get(o, 0) < MIN_SHINGLES:
                        continue
                    osh = other_shingles(o)
                    if len(osh) >= MIN_SHINGLES and len(osh & sh) >= CONTAINMENT * len(osh):
                        contained.append(o)
        self._add(vid, fp, len(sh), title)
        self.dirty = True
        return repeats, contained

    def save(self) -> None:
        if not self.dirty or not self.loaded:
            return
        from .utils import replace_file

        data = {"about": "fingerprints used to spot repeated transcripts (safe to delete; rebuilt over time)",
                "videos": {v: {"n": self.sizes[v], "title": self.titles.get(v, "")[:120], "fp": self.prints[v]}
                           for v in self.prints}}
        tmp = self.path.with_name(self.path.name + ".tmp")
        try:
            tmp.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
            replace_file(tmp, self.path)
            self.dirty = False
        except OSError as e:
            log.debug("could not save %s: %s", self.path.name, e)
