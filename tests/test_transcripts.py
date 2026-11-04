import pytest
from conftest import FIXTURES

from yt_transcripts import transcripts as tr
from yt_transcripts.config import build_settings
from yt_transcripts.models import Video


def test_parse_json3_auto_captions():
    segs = tr.parse_json3((FIXTURES / "captions_asr.json3").read_text(encoding="utf-8"))
    texts = [s.text for s in segs]
    assert texts == [
        "Today we are going to build",
        "a small web scraper in Python.",
        ">> Sounds good, let's go. if a < b",  # speaker marker kept, '<' in real text survives
        "[music]",
        "First install requests.",
    ]
    assert segs[0].start == 0 and segs[1].start == 1.12 and segs[-1].start == 40.0


def test_parse_json3_bad_input():
    assert tr.parse_json3("") == []
    assert tr.parse_json3("<html>") == []
    assert tr.parse_json3('{"events": []}') == []


def test_parse_vtt_rolling_captions_deduped():
    segs = tr.parse_vtt((FIXTURES / "captions_rolling.vtt").read_text(encoding="utf-8"))
    assert " ".join(s.text for s in segs) == "hello and welcome to the channel"


def test_parse_srv1():
    raw = '<transcript><text start="0.5" dur="1.5">Hi &amp; welcome, a &lt; b</text><text start="2">bye</text></transcript>'
    segs = tr.parse_srv1(raw)
    assert [(s.start, s.text) for s in segs] == [(0.5, "Hi & welcome, a < b"), (2.0, "bye")]


# ---- language choice -------------------------------------------------------------
def T(lang, generated=False, translated=False, translatable=False):
    return tr.Track(lang=lang, name=lang, generated=generated, translated=translated, translatable=translatable)


def S(**kw):
    return build_settings({"keywords": ["x"], **kw})


def test_prefers_manual_in_preferred_language():
    tracks = [T("en", generated=True), T("en-US"), T("de")]
    assert tr.choose_track(tracks, S()).lang == "en-US"


def test_prefer_manual_off_follows_language_order():
    tracks = [T("de"), T("en", generated=True)]
    s = S(languages=["en", "de"], prefer_manual=False)
    assert tr.choose_track(tracks, s).lang == "en"
    s = S(languages=["en", "de"], prefer_manual=True)
    assert tr.choose_track(tracks, s).lang == "de"  # any manual before any auto


def test_specific_regional_code_needs_exact_match():
    tracks = [T("en-GB")]
    assert tr.choose_track(tracks, S(languages=["en-US"], allow_other_languages=False)) is None
    assert tr.choose_track(tracks, S(languages=["en"], allow_other_languages=False)).lang == "en-GB"


def test_falls_back_to_original_language():
    tracks = [T("hi", generated=True), T("en", generated=True, translated=True)]
    assert tr.choose_track(tracks, S()).lang == "hi"
    assert tr.choose_track(tracks, S(allow_other_languages=False)) is None


def test_translate_option():
    tracks = [T("hi", generated=True), T("en", generated=True, translated=True)]
    chosen = tr.choose_track(tracks, S(translate=True))
    assert chosen.lang == "en" and chosen.translated
    # youtube-transcript-api style: only a translatable source track
    chosen = tr.choose_track([T("hi", generated=True, translatable=True)], S(translate=True))
    assert chosen.lang == "en" and chosen.translated


# ---- yt-dlp fetcher with a fake YoutubeDL ------------------------------------------
class FakeResp:
    def __init__(self, body):
        self.body = body

    def read(self):
        return self.body.encode()


class FakeYDL:
    def __init__(self, info=None, exc=None, bodies=None, warnings=None):
        self.info, self.exc, self.bodies = info, exc, bodies or {}
        self.warnings, self.logger = warnings or [], None

    def extract_info(self, url, download=False, process=True):
        if self.logger is not None:
            self.logger.warnings.extend(self.warnings)
        if self.exc:
            raise self.exc
        return self.info

    def urlopen(self, url):
        if url not in self.bodies:
            raise OSError("HTTP Error 404")
        return FakeResp(self.bodies[url])

    def close(self):
        pass


def _info(subs=None, auto=None):
    return {"id": "abcdefghijk", "title": "x", "upload_date": "20261027", "view_count": 1234,
            "subtitles": subs or {}, "automatic_captions": auto or {}}


def test_ytdlp_fetcher_prefers_original_auto_over_translation():
    asr = (FIXTURES / "captions_asr.json3").read_text(encoding="utf-8")
    auto = {
        "en-orig": [{"ext": "json3", "url": "u-orig", "name": "English (Original)"}],
        "en": [{"ext": "json3", "url": "u-en", "name": "English"}],
        "fr": [{"ext": "json3", "url": "u-fr", "name": "French"}],
    }
    ydl = FakeYDL(_info(auto=auto), bodies={"u-en": asr})
    f = tr.YtDlpFetcher(S(), ydl_factory=lambda: ydl)
    t = f.fetch(Video(video_id="abcdefghijk"))
    assert t.language == "en" and t.kind == "auto" and t.method == "ytdlp"
    assert f.last_info["upload_date"] == "20261027"


def test_ytdlp_fetcher_falls_back_to_vtt_when_json3_empty():
    vtt = (FIXTURES / "captions_rolling.vtt").read_text(encoding="utf-8")
    subs = {"en": [{"ext": "json3", "url": "j"}, {"ext": "vtt", "url": "v"}]}
    ydl = FakeYDL(_info(subs=subs), bodies={"j": "", "v": vtt})
    t = tr.YtDlpFetcher(S(), ydl_factory=lambda: ydl).fetch(Video(video_id="abcdefghijk"))
    assert t.kind == "manual" and t.text == "hello and welcome to the channel"


def test_ytdlp_fetcher_empty_track_is_a_token_wall():
    subs = {"en": [{"ext": "json3", "url": "j"}]}
    ydl = FakeYDL(_info(subs=subs), bodies={"j": ""})
    try:
        tr.YtDlpFetcher(S(), ydl_factory=lambda: ydl).fetch(Video(video_id="abcdefghijk"))
    except tr.FetchError as e:
        assert e.status == tr.PO_TOKEN
    else:
        raise AssertionError("expected FetchError")


def test_ytdlp_fetcher_no_captions():
    ydl = FakeYDL(_info())
    try:
        tr.YtDlpFetcher(S(), ydl_factory=lambda: ydl).fetch(Video(video_id="abcdefghijk"))
    except tr.FetchError as e:
        assert e.status == tr.NO_TRANSCRIPT
    else:
        raise AssertionError


def test_ytdlp_error_classification():
    cases = {
        "ERROR: [youtube] abc: Sign in to confirm you're not a bot. Use --cookies": tr.BLOCKED,
        "ERROR: [youtube] abc: Private video. Sign in if you've been granted access": tr.UNAVAILABLE,
        "ERROR: [youtube] abc: Video unavailable. This video has been removed by the uploader": tr.UNAVAILABLE,
        "ERROR: Unable to download webpage: <urlopen error timed out>": tr.ERROR,
        ("ERROR: [youtube] abc: This content isn't available, try again later. The current session has been "
         "rate-limited by YouTube for up to an hour."): tr.BLOCKED,
        "ERROR: [youtube] abc: Sign in to confirm your age. This video may be inappropriate": tr.UNAVAILABLE,
        "ERROR: [youtube] abc: The uploader has not made this video available in your country": tr.UNAVAILABLE,
        "ERROR: [youtube] abc: Join this channel to get access to members-only content": tr.UNAVAILABLE,
        "ERROR: [youtube] abc: Premieres in 3 hours": tr.ERROR,  # retried next run, not given up on
        "ERROR: [youtube] abc: This live event will begin in a few moments.": tr.ERROR,
    }
    for msg, status in cases.items():
        ydl = FakeYDL(exc=Exception(msg))
        try:
            tr.YtDlpFetcher(S(), ydl_factory=lambda ydl=ydl: ydl).fetch(Video(video_id="abcdefghijk"))
        except tr.FetchError as e:
            assert e.status == status, msg


# ---- youtube-transcript-api fetcher with a fake API object ----------------------------
class FakeSnippet:
    def __init__(self, text, start, duration):
        self.text, self.start, self.duration = text, start, duration


class FakeFetched:
    def __init__(self, lang, generated):
        self.language_code, self.language, self.is_generated = lang, lang.upper(), generated
        self.snippets = [FakeSnippet("hello", 0, 1), FakeSnippet("  ", 1, 1), FakeSnippet("world", 2, 1)]


class FakeTrack:
    def __init__(self, lang, generated, translatable=True):
        self.language_code, self.language, self.is_generated = lang, lang, generated
        self.is_translatable = translatable
        self.translated_to = None

    def fetch(self):
        return FakeFetched(self.translated_to or self.language_code, self.is_generated)

    def translate(self, lang):
        t = FakeTrack(self.language_code, self.is_generated)
        t.translated_to = lang
        return t


def test_api_fetcher(monkeypatch):
    f = tr.ApiFetcher(S())
    monkeypatch.setattr(f.api, "list", lambda vid: [FakeTrack("de", False), FakeTrack("en", True)])
    t = f.fetch(Video(video_id="abcdefghijk"))
    assert t.language == "en" and t.kind == "auto" and t.text == "hello world"

    f2 = tr.ApiFetcher(S(translate=True))
    monkeypatch.setattr(f2.api, "list", lambda vid: [FakeTrack("hi", True)])
    t = f2.fetch(Video(video_id="abcdefghijk"))
    assert t.language == "en" and t.kind == "translated"


def test_api_fetcher_maps_library_errors(monkeypatch):
    import youtube_transcript_api as yta

    f = tr.ApiFetcher(S())
    cases = [
        (yta.TranscriptsDisabled("abcdefghijk"), tr.NO_TRANSCRIPT),
        (yta.VideoUnavailable("abcdefghijk"), tr.UNAVAILABLE),
        (yta.IpBlocked("abcdefghijk"), tr.BLOCKED),
        (yta.PoTokenRequired("abcdefghijk"), tr.PO_TOKEN),
        (RuntimeError("boom"), tr.ERROR),
        # VideoUnplayable is used for everything: rate-limit pages and bot checks must not be "permanent"
        (yta.VideoUnplayable("abcdefghijk", "This content isn't available, try again later.", []), tr.BLOCKED),
        (yta.VideoUnplayable("abcdefghijk", "Sign in to confirm you're not a bot", []), tr.BLOCKED),
        (yta.VideoUnplayable("abcdefghijk", "Private video", ["Sign in if you've been granted access"]),
         tr.UNAVAILABLE),
        (yta.VideoUnplayable("abcdefghijk", "Join this channel to get access to members-only content", []),
         tr.UNAVAILABLE),
        (yta.VideoUnplayable("abcdefghijk", None, []), tr.ERROR),
        (yta.VideoUnplayable("abcdefghijk", "Sign in to confirm your age", []), tr.UNAVAILABLE),
        (yta.VideoUnplayable("abcdefghijk", "The following content is not available on this app.", []), tr.ERROR),
        (yta.YouTubeRequestFailed("abcdefghijk", Exception("429 Client Error: Too Many Requests")), tr.BLOCKED),
    ]
    for exc, status in cases:
        def boom(vid, exc=exc):
            raise exc
        monkeypatch.setattr(f.api, "list", boom)
        try:
            f.fetch(Video(video_id="abcdefghijk"))
        except tr.FetchError as e:
            assert e.status == status, exc
        else:
            raise AssertionError


def test_ytdlp_captions_dropped_for_po_token_is_a_token_wall():
    from yt_transcripts.ytdlp_common import YdlLogger

    warn = "abc: There are missing subtitles languages because a PO token was not provided."
    ydl = FakeYDL(_info(), warnings=[warn])
    f = tr.YtDlpFetcher(S(), ydl_factory=lambda: ydl)
    f._get_ydl()
    f._loggers["full"] = ydl.logger = YdlLogger()
    try:
        f.fetch(Video(video_id="abcdefghijk"))
    except tr.FetchError as e:
        assert e.status == tr.PO_TOKEN and "PO token" in str(e)
    else:
        raise AssertionError


def test_ytdlp_upcoming_stream_is_retried_later():
    info = _info()
    info["live_status"] = "is_upcoming"
    try:
        tr.YtDlpFetcher(S(), ydl_factory=lambda: FakeYDL(info)).fetch(Video(video_id="abcdefghijk"))
    except tr.FetchError as e:
        assert e.status == tr.ERROR and "next run" in str(e)
    else:
        raise AssertionError


def test_strip_sound_tags():
    from yt_transcripts.models import Segment, Transcript

    t = Transcript("x", "en", segments=[Segment(0, 1, "[Music]"), Segment(1, 1, "hello [Applause] there (laughs)"),
                                        Segment(2, 1, "♪♪ la la ♪♪"), Segment(3, 1, "keep [sic] short"),
                                        Segment(4, 1, "see [3] and the [EU] [upbeat music] [MUSIC]")])
    tr.strip_sound_tags(t)
    # short bracketed words are content (citations, abbreviations), not sound labels
    assert [s.text for s in t.segments] == ["hello there", "la la", "keep [sic] short", "see [3] and the [EU]"]


def test_rate_limit_reported_as_warning_is_blocked_not_no_captions():
    from yt_transcripts.ytdlp_common import YdlLogger

    ydl = FakeYDL(_info(), warnings=["abc: This content isn't available, try again later."])
    f = tr.YtDlpFetcher(S(), ydl_factory=lambda: ydl)
    f._get_ydl()
    f._loggers["full"] = ydl.logger = YdlLogger()
    try:
        f.fetch(Video(video_id="abcdefghijk"))
    except tr.FetchError as e:
        assert e.status == tr.BLOCKED
    else:
        raise AssertionError


def test_translations_of_uploaded_captions_are_not_native():
    subs = {"en": [{"ext": "json3", "url": "en"}]}
    auto = {"de-en": [{"ext": "json3", "url": "de"}], "fr-en": [{"ext": "json3", "url": "fr"}]}
    body = '{"events":[{"tStartMs":0,"dDurationMs":1000,"segs":[{"utf8":"hello"}]}]}'
    ydl = FakeYDL(_info(subs=subs, auto=auto), bodies={"en": body, "de": body})
    t = tr.YtDlpFetcher(S(languages=["de"]), ydl_factory=lambda: ydl).fetch(Video(video_id="abcdefghijk"))
    assert t.language == "en" and t.kind == "manual"  # original, not the German machine translation
    ydl2 = FakeYDL(_info(subs=subs, auto=auto), bodies={"en": body, "de": body})
    t2 = tr.YtDlpFetcher(S(languages=["de"], translate=True), ydl_factory=lambda: ydl2).fetch(Video(video_id="abcdefghijk"))
    assert t2.language == "de-en" and t2.kind == "translated"


def test_vtt_tags_stripped_but_text_angle_brackets_kept():
    raw = "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\n<c.colorE5E5E5>if x &lt; 3</c><00:00:01.000><c> and y > 2</c>\n"
    assert tr.parse_vtt(raw)[0].text == "if x < 3 and y > 2"


def test_subtitle_request_uses_impersonation_when_available():
    from yt_dlp import YoutubeDL

    fmt = {"url": "https://www.youtube.com/api/timedtext?v=x&fmt=json3", "impersonate": True}
    req = tr._subtitle_request(YoutubeDL({"quiet": True}), fmt)
    # without curl_cffi installed there is no target, so a plain URL is used; with it, a Request
    assert req == fmt["url"] or req.extensions.get("impersonate")
    assert tr._subtitle_request(object(), fmt) == fmt["url"]  # anything unexpected -> plain URL
    assert tr._subtitle_request(None, {"url": "u"}) == "u"


@pytest.mark.parametrize("raw", ["null", "[]", '{"events": null}', '{"events": [null, 1, {"segs": "x"}]}',
                                 '{"events": [{"segs": [{"utf8": null}, 5], "tStartMs": "abc"}]}'])
def test_json3_parser_tolerates_odd_data(raw):
    assert tr.parse_json3(raw) == []


def _fetcher_with_warnings(info, warnings, bodies, **settings):
    from yt_transcripts.ytdlp_common import YdlLogger

    ydl = FakeYDL(info, warnings=warnings, bodies=bodies)
    f = tr.YtDlpFetcher(S(**settings), ydl_factory=lambda: ydl)
    f._get_ydl()
    f._loggers["full"] = ydl.logger = YdlLogger()
    return f


def test_rate_limit_warning_is_ignored_when_captions_came_back():
    asr = (FIXTURES / "captions_asr.json3").read_text(encoding="utf-8")
    f = _fetcher_with_warnings(_info(auto={"en": [{"ext": "json3", "url": "u", "name": "English"}]}),
                               ["[youtube] abc: web client: This content isn't available, try again later"],
                               {"u": asr})
    assert f.fetch(Video(video_id="abcdefghijk")).segments  # another client delivered the captions


def test_rate_limit_warning_without_captions_is_a_block():
    f = _fetcher_with_warnings(_info(), ["This content isn't available, try again later"], {})
    with pytest.raises(tr.FetchError) as e:
        f.fetch(Video(video_id="abcdefghijk"))
    assert e.value.status == tr.BLOCKED


def test_refused_translation_falls_back_to_the_original_language():
    class Refuse429(FakeYDL):
        def urlopen(self, url):
            if url == "u-en":
                raise OSError("HTTP Error 429: Too Many Requests")
            return super().urlopen(url)

    asr = (FIXTURES / "captions_asr.json3").read_text(encoding="utf-8")
    auto = {"de-orig": [{"ext": "json3", "url": "u-de", "name": "German (Original)"}],
            "de": [{"ext": "json3", "url": "u-de", "name": "German"}],
            "en": [{"ext": "json3", "url": "u-en", "name": "English"}]}
    ydl = Refuse429(_info(auto=auto), bodies={"u-de": asr})
    t = tr.YtDlpFetcher(S(translate=True, allow_other_languages=True), ydl_factory=lambda: ydl).fetch(
        Video(video_id="abcdefghijk"))
    assert t.language == "de" and t.kind == "auto"
    ydl = Refuse429(_info(auto=auto), bodies={"u-de": asr})
    with pytest.raises(tr.FetchError) as e:  # without the fallback allowed it stays a (retryable) block
        tr.YtDlpFetcher(S(translate=True, allow_other_languages=False), ydl_factory=lambda: ydl).fetch(
            Video(video_id="abcdefghijk"))
    assert e.value.status == tr.BLOCKED


# ---- data saver ----------------------------------------------------------------------------------------
SRV1 = '<?xml version="1.0"?><transcript><text start="0" dur="2">Hello &amp;amp; welcome</text>' \
       '<text start="2" dur="2">to the show</text></transcript>'


def _saver_settings(**kw):
    from yt_transcripts.config import build_settings

    return build_settings({"languages": ["en"], **kw})


def test_saver_profile_choice():
    tr.SAVER_HEALTH.reset()
    assert tr.saver_profile(_saver_settings()) == "full"  # own connection: nothing to save
    assert tr.saver_profile(_saver_settings(proxy="http://127.0.0.1:9")) == "lean"
    assert tr.saver_profile(_saver_settings(proxy="http://x:1", data_saver="off")) == "full"
    assert tr.saver_profile(_saver_settings(data_saver="on")) == "lean"
    assert tr.saver_profile(_saver_settings(data_saver="max")) == "max"


def test_saver_options_ask_for_one_client_and_respect_user_overrides():
    from yt_transcripts.ytdlp_common import base_options

    lean = base_options(_saver_settings(), profile="lean")["extractor_args"]["youtube"]
    assert lean["player_client"] == ["visionos"] and lean["skip"] == ["dash", "hls"]
    mx = base_options(_saver_settings(), profile="max")["extractor_args"]["youtube"]
    assert mx["player_skip"] == ["webpage", "initial_data"]
    assert "player_client" not in base_options(_saver_settings(), profile="full")["extractor_args"]["youtube"]
    mine = base_options(_saver_settings(ytdlp_extractor_args=["youtube:player_client=tv"]), profile="lean")
    assert mine["extractor_args"]["youtube"]["player_client"] == ["tv"]


def test_lean_downloads_the_small_caption_format_first():
    tr.SAVER_HEALTH.reset()
    auto = {"en": [{"ext": "json3", "url": "u-json3"}, {"ext": "srv1", "url": "u-srv1"}]}
    ydl = FakeYDL(_info(auto=auto), bodies={"u-srv1": SRV1, "u-json3": "{}"})
    asked = []
    real = ydl.urlopen
    ydl.urlopen = lambda u: (asked.append(u), real(u))[1]
    profiles = []
    f = tr.YtDlpFetcher(_saver_settings(proxy="http://127.0.0.1:9"),
                        ydl_factory=lambda profile="full": (profiles.append(profile), ydl)[1])
    t = f.fetch(Video(video_id="abcdefghijk"))
    assert profiles == ["lean"] and asked == ["u-srv1"]
    assert [s.text for s in t.segments] == ["Hello &amp; welcome", "to the show"]


def test_lean_miss_is_checked_with_the_full_method_and_switches_off():
    tr.SAVER_HEALTH.reset()
    auto = {"en": [{"ext": "srv1", "url": "u"}]}
    lean = FakeYDL(_info())  # the lean client saw no captions...
    full = FakeYDL(_info(auto=auto), bodies={"u": SRV1})  # ...the full method finds them
    made = []

    def factory(profile="full"):
        made.append(profile)
        return lean if profile == "lean" else full
    s = _saver_settings(proxy="http://127.0.0.1:9")
    for _ in range(3):
        f = tr.YtDlpFetcher(s, ydl_factory=factory)
        assert f.fetch(Video(video_id="abcdefghijk")).segments
    assert made == ["lean", "full"] * 3
    assert tr.SAVER_HEALTH.disabled and tr.saver_profile(s) == "full"
    tr.SAVER_HEALTH.reset()


def test_lean_does_not_double_fetch_blocked_or_wrong_language():
    tr.SAVER_HEALTH.reset()
    made = []
    blocked = FakeYDL(exc=Exception("Sign in to confirm you're not a bot"))
    f = tr.YtDlpFetcher(_saver_settings(proxy="http://127.0.0.1:9"),
                        ydl_factory=lambda profile="full": (made.append(profile), blocked)[1])
    with pytest.raises(tr.FetchError) as e:
        f.fetch(Video(video_id="abcdefghijk"))
    assert e.value.status == tr.BLOCKED and made == ["lean"]
    made.clear()
    fr = FakeYDL(_info(auto={"fr": [{"ext": "srv1", "url": "u"}]}), bodies={"u": SRV1})
    f = tr.YtDlpFetcher(_saver_settings(proxy="http://127.0.0.1:9", allow_other_languages=False),
                        ydl_factory=lambda profile="full": (made.append(profile), fr)[1])
    with pytest.raises(tr.FetchError) as e:
        f.fetch(Video(video_id="abcdefghijk"))
    assert e.value.status == tr.NO_TRANSCRIPT and made == ["lean"]


def test_no_captions_is_only_sampled_not_always_double_checked():
    tr.SAVER_HEALTH.reset()
    made = []
    nocap = FakeYDL(_info())

    def factory(profile="full"):
        made.append(profile)
        return nocap
    s = _saver_settings(proxy="http://127.0.0.1:9")
    for _ in range(12):
        f = tr.YtDlpFetcher(s, ydl_factory=factory)
        with pytest.raises(tr.FetchError):
            f.fetch(Video(video_id="abcdefghijk"))
    assert made.count("full") == 4  # videos 1-3 and 10 are double-checked, not all 12
    assert not tr.SAVER_HEALTH.disabled  # the full method agreed: no misses
    tr.SAVER_HEALTH.reset()


def test_max_saver_uses_lean_when_translating():
    tr.SAVER_HEALTH.reset()
    assert tr.saver_profile(_saver_settings(data_saver="max", translate=True)) == "lean"
