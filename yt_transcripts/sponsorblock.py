"""Cut sponsor reads, self-promotion and "like and subscribe" reminders out of transcripts.

SponsorBlock (https://sponsor.ajay.app) is a free, crowd-sourced database of those segments, keyed by
video ID. One small request per video - a few kB, sent over your own connection (never through the
proxies: it isn't YouTube, so no proxy data is used). For privacy the request carries only the first
characters of a hash of the video ID, as SponsorBlock recommends, and the matching video is picked out
of the answer here.

The removed parts are listed in each transcript's header, and the .json keeps the full original text,
so switching this off later rebuilds the files with everything back.
"""

from __future__ import annotations

import hashlib
import json
import logging

from .models import Segment, Transcript

log = logging.getLogger("yt_transcripts")

API = "https://sponsor.ajay.app/api/skipSegments/"
HASH_PREFIX = 5  # 4 is SponsorBlock's privacy recommendation; 5 keeps the answer ~16x smaller, still shared
TIMEOUT = 10
NAMES = {
    "sponsor": "sponsor", "selfpromo": "self-promotion", "interaction": "subscribe reminder",
    "intro": "intro", "outro": "outro/credits", "preview": "preview/recap", "filler": "filler tangent",
    "music_offtopic": "non-music part", "hook": "hook/greeting",
}
CATEGORIES = tuple(NAMES)


def fetch_segments(video_id: str, categories: list[str], duration: float | None = None, *,
                   get=None) -> list[dict] | None:
    """[{"start", "end", "category"}] for this video ([] when none are known; None when the lookup failed)."""
    cats = [c for c in categories if c in NAMES]
    if not cats or not video_id:
        return []
    prefix = hashlib.sha256(video_id.encode("ascii", "ignore")).hexdigest()[:HASH_PREFIX]
    params = {"categories": json.dumps(cats), "actionTypes": json.dumps(["skip"]), "service": "YouTube"}
    try:
        if get is None:
            import requests

            session = requests.Session()
            session.trust_env = True  # your own connection (a system proxy, if you use one, is fine)
            r = session.get(API + prefix, params=params, timeout=TIMEOUT,
                            headers={"User-Agent": "YouTubeTranscriptTool (SponsorBlock lookup)"})
            if r.status_code == 404:  # no segments for any video with this prefix
                return []
            r.raise_for_status()
            data = r.json()
        else:
            data = get(API + prefix, params)
    except Exception as e:  # noqa: BLE001 - SponsorBlock being down must never cost a transcript
        log.debug("SponsorBlock lookup for %s failed: %s", video_id, e)
        return None
    out = []
    for entry in data if isinstance(data, list) else []:
        if not isinstance(entry, dict) or entry.get("videoID") != video_id:
            continue
        for seg in entry.get("segments") or []:
            try:
                start, end = (float(x) for x in seg["segment"])
                cat = str(seg["category"])
                vdur = float(seg.get("videoDuration") or 0)
            except (KeyError, TypeError, ValueError):
                continue
            if cat not in cats or end <= start or (start, end) == (0.0, 0.0):
                continue
            # a segment submitted for an older, different-length version of the video: skip it
            if duration and vdur and abs(duration - vdur) > max(2.0, 0.02 * duration):
                continue
            out.append({"start": round(start, 2), "end": round(end, 2), "category": cat})
    out.sort(key=lambda s: s["start"])
    return out


def cut(t: Transcript, skipped: list[dict]) -> Transcript:
    """Drop caption lines that fall mostly inside a skipped segment (works on a copy's segment list)."""
    if not skipped:
        return t
    kept = []
    for sg in t.segments:
        mid = sg.start + max(sg.duration, 0.01) / 2
        if any(s["start"] <= mid < s["end"] for s in skipped):
            continue
        kept.append(Segment(sg.start, sg.duration, sg.text))
    t.segments = kept
    return t


def describe(skipped: list[dict]) -> str:
    """'sponsor 1:23-2:05, subscribe reminder 10:02-10:30' for the transcript header."""
    from .utils import format_ts

    return ", ".join(f"{NAMES.get(s['category'], s['category'])} {format_ts(s['start'])}-{format_ts(s['end'])}"
                     for s in skipped)
