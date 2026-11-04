import datetime as dt

import pytest

from yt_transcripts.models import Video
from yt_transcripts.utils import format_duration, format_ts, parse_count, parse_relative_time, safe_filename, slug


@pytest.mark.parametrize("text,expected", [
    ("163,850 views", 163_850),
    ("1.2M views", 1_200_000),
    ("9.5K", 9_500),
    ("641", 641),
    ("No views", 0),
    ("1,2 Mio.", 1_200_000),
    ("", None),
    (None, None),
    (42, 42),
])
def test_parse_count(text, expected):
    assert parse_count(text) == expected


NOW = dt.datetime(2026, 10, 29, 12, 0, tzinfo=dt.timezone.utc)


@pytest.mark.parametrize("text,delta", [
    ("2d ago", dt.timedelta(days=2)),
    ("15h ago", dt.timedelta(hours=15)),
    ("30m ago", dt.timedelta(minutes=30)),
    ("Streamed 4d ago", dt.timedelta(days=4)),
    ("3 weeks ago", dt.timedelta(weeks=3)),
    ("1 month ago", dt.timedelta(days=30)),
    ("2y ago", dt.timedelta(days=730)),
])
def test_parse_relative_time(text, delta):
    assert parse_relative_time(text, NOW) == NOW - delta


def test_parse_relative_time_garbage():
    assert parse_relative_time("Premieres tomorrow", NOW) is None


@pytest.mark.parametrize("raw,expected", [
    ('What is AI? | "Explained" <2026>', "What is AI   Explained  2026".replace("   ", " ").replace("  ", " ")),
    ("CON", "_CON"),
    ("   ...   ", "untitled"),
    ("a/b\\c:d*e", "a b c d e"),
])
def test_safe_filename(raw, expected):
    assert safe_filename(raw) == expected


def test_safe_filename_truncates():
    assert len(safe_filename("x" * 500, 50)) == 50


def test_slug():
    assert slug("Claude Code: Tutorial!") == "claude-code-tutorial"


def test_formatting():
    assert format_duration(65) == "1:05"
    assert format_duration(38787) == "10:46:27"
    assert format_duration(None) == ""
    assert format_ts(3725.5, srt=True) == "01:02:05,500"
    assert format_ts(65) == "01:05"


def test_video_roundtrip_and_merge():
    v = Video(video_id="abcdefghijk", title="T", views=10, keyword="a", published="2026-10-01", published_exact=False)
    assert v.url.endswith("abcdefghijk")
    d = v.to_dict()
    d["views"] = "12"
    d["published_exact"] = "False"
    d["unknown_col"] = "x"
    v2 = Video.from_dict(d)
    assert v2.views == 12 and v2.published_exact is False
    other = Video(video_id="abcdefghijk", views=99, keyword="b", published="2026-10-02T10:00:00+00:00",
                  published_exact=True)
    v.merge(other)
    assert v.keyword == "a; b" and v.views == 99 and v.published_exact


def test_run_lock_is_exclusive(tmp_path):
    import subprocess
    import sys

    from yt_transcripts.utils import RunLock

    with RunLock(tmp_path):
        # a second process must fail to take the same lock
        code = ("import sys; sys.path.insert(0, %r); from yt_transcripts.utils import RunLock; "
                "print(RunLock(%r).acquire())") % (str(__import__('pathlib').Path(__file__).resolve().parent.parent),
                                                   str(tmp_path))
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout.strip()
        assert out == "False"
    lock = RunLock(tmp_path)
    assert lock.acquire()
    lock.release()


def test_config_values_are_coerced():
    from yt_transcripts.config import build_settings

    s = build_settings({"min_views": "10,000", "max_results": 5.0, "include_shorts": "yes", "languages": "en, es",
                        "delay_seconds": "3", "combine": "false", "max_age_days": "2.5", "keywords": ["a"]})
    assert s.min_views == 10_000 and s.max_results == 5 and s.include_shorts is True
    assert s.languages == ["en", "es"] and s.delay_seconds == 3.0 and s.combine is False and s.max_age_days == 2.5
    bad = build_settings({"min_views": "lots"})
    assert bad.min_views == 10_000 and "min_views" in bad._coerce_problems[0]


def test_config_file_mistakes_give_friendly_errors(tmp_path):
    import pytest

    from yt_transcripts.config import ConfigError, build_settings, load_config, read_keywords_file

    bad = tmp_path / "bad.toml"
    bad.write_text('keywords = ["x"]\noutput_dir = "C:\\Users\\you\\Documents"\n', encoding="utf-8")
    with pytest.raises(ConfigError, match="single quotes"):
        load_config(bad)
    bom = tmp_path / "bom.toml"
    bom.write_bytes('\ufeffkeywords = ["café"]\n'.encode("utf-8"))
    assert load_config(bom)["keywords"] == ["café"]
    ansi = tmp_path / "ansi.toml"
    ansi.write_bytes('keywords = ["café"]\n'.encode("cp1252"))
    assert load_config(ansi)["keywords"] == ["café"]
    uni = tmp_path / "unicode.toml"
    uni.write_text('keywords = ["café"]\n', encoding="utf-16")
    assert load_config(uni)["keywords"] == ["café"]
    with pytest.raises(ConfigError, match="does not exist"):
        read_keywords_file(tmp_path / "missing.txt")
    s = build_settings({"keywords": ["x"], "keyword_settings": [{"keyword": "x", "within": "Week",
                                                                 "sorts": ["Popularity"]}]})
    assert s.validate() == [] and s.for_keyword("x").within == "week"


def test_short_error_strips_ytdlp_boilerplate():
    from yt_transcripts.utils import short_error

    e = Exception('ERROR: [youtube:search] query "x" page 1: Unable to download API page: '
                  "('Unable to connect to proxy', OSError('Tunnel connection failed')) (caused by ProxyError(...)); "
                  "please report this issue on  https://github.com/yt-dlp/yt-dlp/issues")
    msg = short_error(e)
    assert msg.startswith("no connection to YouTube") and "report this issue" not in msg and "caused by" not in msg
    assert short_error(Exception("ERROR: [youtube] abc: Private video")) == "abc: Private video"


def test_ytdlp_age():
    import datetime as dt

    from yt_dlp.version import __version__ as ver

    from yt_transcripts.ytdlp_common import ytdlp_age_days

    y, m, d = (int(x) for x in ver.split(".")[:3])
    assert ytdlp_age_days(dt.date(y, m, d) + dt.timedelta(days=90)) == 90


def test_cookie_errors_get_cookie_advice():
    from yt_transcripts.utils import short_error

    for msg in ("ERROR: Could not copy Chrome cookie database. See https://github.com/yt-dlp/yt-dlp/issues/7271",
                "ERROR: Failed to decrypt with DPAPI. See https://github.com/yt-dlp/yt-dlp/issues/10927"):
        assert "firefox" in short_error(Exception(msg))


def test_replace_file_retries_briefly_locked_target(tmp_path, monkeypatch):
    import os

    from yt_transcripts import utils

    src, dst = tmp_path / "a.tmp", tmp_path / "a.json"
    src.write_text("new", encoding="utf-8")
    real, fails = os.replace, [2]

    def flaky(a, b):
        if fails[0]:
            fails[0] -= 1
            raise PermissionError(13, "in use by OneDrive")
        return real(a, b)

    monkeypatch.setattr(utils.os if hasattr(utils, "os") else os, "replace", flaky)
    monkeypatch.setattr(utils.time, "sleep", lambda s: None)
    utils.replace_file(src, dst)
    assert dst.read_text(encoding="utf-8") == "new"
