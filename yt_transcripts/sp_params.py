"""Build the ``sp`` filter parameter used by youtube.com/results.

YouTube encodes search filters as a small base64 protobuf. The layout below
was verified against the live search page in October 2026:

    field 1 (varint)  sort / "Prioritize":   0 = Relevance, 3 = Popularity
                      (2 = upload date and 1 = rating still parse, but YouTube
                      no longer honours them -- results come back by relevance)
    field 2 (message) filters
        field 1  upload date: 2 = today, 3 = this week, 4 = this month, 5 = this year
        field 2  type:        1 = video, 2 = channel, 3 = playlist, 4 = movie, 9 = shorts
        field 3  duration:    4 = under 3 min, 5 = 3-20 min, 2 = over 20 min
        field 5  subtitles/CC (1 = only videos with uploaded captions)
"""

from __future__ import annotations

import base64

SORT = {"relevance": 0, "popularity": 3, "views": 3}
UPLOAD_DATE = {"today": 2, "day": 2, "week": 3, "month": 4, "year": 5}
TYPE = {"video": 1, "channel": 2, "playlist": 3, "movie": 4, "shorts": 9}
DURATION = {"short": 4, "under3": 4, "medium": 5, "3-20": 5, "long": 2, "over20": 2}


def _varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _field_varint(field: int, value: int) -> bytes:
    return _varint(field << 3) + _varint(value)


def _field_bytes(field: int, value: bytes) -> bytes:
    return _varint((field << 3) | 2) + _varint(len(value)) + value


def build_sp(
    sort: str = "relevance",
    upload_date: str | None = None,
    content_type: str | None = "video",
    duration: str | None = None,
    subtitles_only: bool = False,
) -> str:
    """Return the (un-URL-encoded) base64 ``sp`` value for the given filters."""
    try:
        sort_v = SORT[sort.lower()]
    except KeyError:
        raise ValueError(f"Unknown sort {sort!r}; choose from {sorted(SORT)}") from None

    filters = b""
    if upload_date:
        try:
            filters += _field_varint(1, UPLOAD_DATE[upload_date.lower()])
        except KeyError:
            raise ValueError(
                f"Unknown upload date window {upload_date!r}; choose from {sorted(UPLOAD_DATE)}"
            ) from None
    if content_type:
        filters += _field_varint(2, TYPE[content_type.lower()])
    if duration:
        try:
            filters += _field_varint(3, DURATION[duration.lower()])
        except KeyError:
            raise ValueError(f"Unknown duration {duration!r}; choose from {sorted(DURATION)}") from None
    if subtitles_only:
        filters += _field_varint(5, 1)

    msg = _field_varint(1, sort_v) + _field_bytes(2, filters)
    return base64.b64encode(msg).decode("ascii")
