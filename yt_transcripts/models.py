"""Data model shared by the search backends, the list writers and the transcript stage."""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass, field, fields
from typing import Any


@dataclass
class Video:
    video_id: str
    title: str = ""
    channel: str = ""
    channel_id: str = ""
    channel_handle: str = ""  # e.g. "@realpython"
    url: str = ""
    views: int | None = None
    published: str = ""  # ISO 8601 date or datetime (UTC)
    published_exact: bool = False  # False when derived from "3 days ago" text
    duration_seconds: int | None = None
    is_short: bool = False
    live_status: str = ""
    keyword: str = ""  # keyword(s) that found this video, "; "-separated
    source: str = ""  # which search backend found it
    description: str = ""
    tags: list[str] = field(default_factory=list)
    chapters: list[dict] = field(default_factory=list)  # [{"start": seconds, "title": "..."}]
    comments: list[dict] = field(default_factory=list)  # top comments [{"author", "text", "likes"}] (optional)
    duplicate_of: str = ""  # "VIDEO_ID title" when this transcript repeats another one (clip / re-upload)
    is_new: bool = False  # not seen in any earlier search
    first_seen: str = ""  # when a search first found it
    # filled in by the transcript stage
    transcript_status: str = ""
    transcript_language: str = ""
    transcript_kind: str = ""  # "manual" or "auto"
    transcript_file: str = ""
    keyword_mentions: int | None = None  # how often the transcript says the search phrase

    def __post_init__(self) -> None:
        if not self.url:
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"

    # ---- convenience -------------------------------------------------
    @property
    def published_dt(self) -> dt.datetime | None:
        return parse_iso(self.published)

    def age_days(self, now: dt.datetime | None = None) -> float | None:
        p = self.published_dt
        if p is None:
            return None
        now = now or dt.datetime.now(dt.timezone.utc)
        return (now - p).total_seconds() / 86400

    def views_per_day(self, now: dt.datetime | None = None) -> float | None:
        age = self.age_days(now)
        if self.views is None or age is None:
            return None
        return self.views / max(age, 0.5)  # don't explode for videos only minutes old

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Video":
        known = {f.name for f in fields(cls)}
        clean = {k: v for k, v in d.items() if k in known}
        for int_field in ("views", "duration_seconds", "keyword_mentions"):
            v = clean.get(int_field)
            if v in ("", None):
                clean[int_field] = None
            else:
                try:
                    clean[int_field] = int(float(v))
                except (TypeError, ValueError):
                    clean[int_field] = None
        for bool_field in ("published_exact", "is_short", "is_new"):
            v = clean.get(bool_field)
            if isinstance(v, str):
                clean[bool_field] = v.strip().lower() in ("1", "true", "yes")
        clean["tags"] = clean_tags(clean.get("tags"))
        clean["chapters"] = clean_chapters(clean.get("chapters"))
        clean["comments"] = clean_comments(clean.get("comments"))
        for k, v in list(clean.items()):
            if v is None and k not in ("views", "duration_seconds", "keyword_mentions"):
                clean[k] = ""
        return cls(**clean)

    def merge(self, other: "Video") -> None:
        """Merge another sighting of the same video into this record."""
        kws = [k for k in self.keyword.split("; ") if k]
        for k in other.keyword.split("; "):
            if k and k not in kws:
                kws.append(k)
        self.keyword = "; ".join(kws)
        if other.views is not None and (self.views is None or other.views > self.views):
            self.views = other.views
        if other.published_exact and not self.published_exact:
            self.published, self.published_exact = other.published, True
        elif not self.published and other.published:
            self.published = other.published
        for attr in ("title", "channel", "channel_id", "channel_handle", "description", "live_status"):
            if not getattr(self, attr) and getattr(other, attr):
                setattr(self, attr, getattr(other, attr))
        if self.duration_seconds is None:
            self.duration_seconds = other.duration_seconds
        if len(other.description) > len(self.description):
            self.description = other.description
        self.tags = self.tags or list(other.tags)
        self.chapters = self.chapters or list(other.chapters)
        self.comments = self.comments or list(other.comments)
        self.is_short = self.is_short or other.is_short


def clean_tags(raw: Any) -> list[str]:
    """Tags from yt-dlp / a saved list: a list of non-empty strings (a CSV cell may hold "a; b")."""
    if isinstance(raw, str):
        raw = raw.split(";")
    if not isinstance(raw, (list, tuple)):
        return []
    out: list[str] = []
    for t in raw:
        t = str(t).strip() if t is not None else ""
        if t and t not in out:
            out.append(t)
    return out


def clean_comments(raw: Any) -> list[dict]:
    """Comments as [{"author": str, "text": str, "likes": int}], ignoring anything malformed."""
    if not isinstance(raw, (list, tuple)):
        return []
    out = []
    for c in raw:
        if not isinstance(c, dict):
            continue
        text = str(c.get("text") or "").strip()
        if not text:
            continue
        try:
            likes = int(c.get("likes", c.get("like_count")) or 0)
        except (TypeError, ValueError):
            likes = 0
        out.append({"author": str(c.get("author") or "").strip(), "text": text, "likes": likes})
    return out


def clean_chapters(raw: Any) -> list[dict]:
    """Chapters as [{"start": float, "title": str}], sorted, ignoring anything malformed."""
    if not isinstance(raw, (list, tuple)):
        return []
    out = []
    for c in raw:
        if not isinstance(c, dict):
            continue
        try:
            start = float(c.get("start", c.get("start_time")))
        except (TypeError, ValueError):
            continue
        title = str(c.get("title") or "").strip()
        if title and start >= 0:
            out.append({"start": start, "title": title})
    out.sort(key=lambda c: c["start"])
    return out


@dataclass
class Segment:
    start: float
    duration: float
    text: str

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass
class Transcript:
    video_id: str
    language: str
    language_name: str = ""
    kind: str = ""  # "manual" | "auto"
    method: str = ""  # which fetcher produced it
    segments: list[Segment] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)  # SponsorBlock segments known for this video
    removed: list[dict] = field(default_factory=list)  # ...the ones actually cut from this copy's text

    @property
    def text(self) -> str:
        return " ".join(s.text for s in self.segments if s.text)


def parse_iso(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    v = value.strip()
    try:
        if len(v) == 8 and v.isdigit():  # yt-dlp style YYYYMMDD
            d = dt.datetime.strptime(v, "%Y%m%d")
        else:
            d = dt.datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d
