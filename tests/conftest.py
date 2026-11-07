import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
FIXTURES = Path(__file__).resolve().parent / "fixtures"


import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _no_sponsorblock_network(monkeypatch):
    """Tests never call SponsorBlock; the ones about it pass their own answers in."""
    from yt_transcripts import sponsorblock

    real = sponsorblock.fetch_segments
    monkeypatch.setattr(sponsorblock, "fetch_segments",
                        lambda vid, cats, duration=None, *, get=None: real(vid, cats, duration, get=get) if get else [])


@pytest.fixture(autouse=True)
def _no_feed_network(monkeypatch):
    """Tests never download channel feeds; the ones about them pass their own `get`."""
    from yt_transcripts import feeds

    real = feeds.FeedDates._download
    monkeypatch.setattr(feeds.FeedDates, "_download",
                        lambda self, cid: real(self, cid) if self._get is not None else {})
