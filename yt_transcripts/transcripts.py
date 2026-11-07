"""Fetch a transcript for one video.

Two methods, tried in the order given by ``settings.transcript_methods``:

* ``api``   - the youtube-transcript-api package. Fast (no JS runtime), but since
              2025 YouTube demands a proof-of-origin token for a growing share of
              caption tracks, which this package cannot make (PoTokenRequired).
* ``ytdlp`` - yt-dlp. Slower but actively maintained against YouTube changes and
              able to get captions through clients that don't need that token.
"""

from __future__ import annotations

import html
import json
import logging
import re
from dataclasses import dataclass
from typing import Callable

from .config import Settings
from .models import Segment, Transcript, Video

log = logging.getLogger("yt_transcripts")

# ---- statuses --------------------------------------------------------------
OK = "ok"
NO_TRANSCRIPT = "no_transcript"  # captions disabled / none in an acceptable language
UNAVAILABLE = "unavailable"  # private, removed, members-only, age-restricted ...
BLOCKED = "blocked"  # YouTube is rate-limiting / bot-checking us
ERROR = "error"  # anything else (network, parse) - worth retrying later
PO_TOKEN = "po_token"  # YouTube wants a proof-of-origin token for this video's captions - retried on a schedule

PERMANENT = {NO_TRANSCRIPT, UNAVAILABLE}


class FetchError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


# ---- language selection ---------------------------------------------------------
@dataclass
class Track:
    """A caption track offered for a video, independent of which library found it."""
    lang: str
    name: str = ""
    generated: bool = False
    translated: bool = False  # machine translation of another language's track
    handle: object = None  # library-specific object or URL list
    translatable: bool = False  # library can translate this track on request


def _lang_match(code: str, wanted: str) -> bool:
    code, wanted = code.lower(), wanted.lower()
    return code == wanted or code.split("-")[0] == wanted.split("-")[0] == wanted


def choose_track(tracks: list[Track], s: Settings) -> Track | None:
    """Pick the best track according to the user's language preferences."""
    native = [t for t in tracks if not t.translated]
    manual = [t for t in native if not t.generated]
    auto = [t for t in native if t.generated]

    def first(pool: list[Track], langs: list[str]) -> Track | None:
        for lang in langs:
            for t in pool:
                if _lang_match(t.lang, lang):
                    return t
        return None

    langs = s.languages or ["en"]
    order: list[tuple[list[Track], list[str]]] = []
    if s.prefer_manual:
        order += [(manual, langs), (auto, langs)]
    else:
        for lang in langs:
            order += [(manual, [lang]), (auto, [lang])]
    for pool, ls in order:
        t = first(pool, ls)
        if t:
            return t
    if s.translate:
        translated = [t for t in tracks if t.translated]
        t = first(translated, langs[:1])
        if t:
            return t
        # library tracks that can be translated on request (youtube-transcript-api)
        source = (manual or auto or [None])[0]
        if source is not None and getattr(source, "translatable", False):
            return Track(lang=langs[0], name=f"{source.name} >> {langs[0]}", generated=source.generated,
                         translated=True, handle=source.handle)
    if s.allow_other_languages:
        if manual:
            return manual[0]
        if auto:
            return auto[0]
    return None


# ---- method 1: youtube-transcript-api ------------------------------------------
class ApiFetcher:
    name = "api"

    def __init__(self, s: Settings):
        from youtube_transcript_api import YouTubeTranscriptApi

        proxy_config = http_client = None
        if s.proxy:
            import requests
            from youtube_transcript_api.proxies import GenericProxyConfig

            proxy_config = GenericProxyConfig(http_url=s.proxy, https_url=s.proxy)
            http_client = requests.Session()
            http_client.trust_env = False  # a Windows/system proxy must not silently replace the configured one
        self.settings = s
        self.api = YouTubeTranscriptApi(proxy_config=proxy_config, http_client=http_client)

    def fetch(self, video: Video) -> Transcript:
        import youtube_transcript_api as yta

        try:
            tl = self.api.list(video.video_id)
            tracks = [Track(lang=t.language_code, name=t.language, generated=t.is_generated, handle=t,
                            translatable=bool(getattr(t, "is_translatable", False)))
                      for t in tl]
            chosen = choose_track(tracks, self.settings)
            if chosen is None:
                have = ", ".join(sorted({t.lang for t in tracks})) or "none"
                raise FetchError(NO_TRANSCRIPT, f"no transcript in {self.settings.languages} (available: {have})")
            handle = chosen.handle
            if chosen.translated:
                handle = handle.translate(chosen.lang)
            fetched = handle.fetch()
        except FetchError:
            raise
        except yta.TranscriptsDisabled as e:
            raise FetchError(NO_TRANSCRIPT, "captions are disabled for this video") from e
        except yta.NoTranscriptFound as e:
            raise FetchError(NO_TRANSCRIPT, f"no transcript in {self.settings.languages}") from e
        except yta.AgeRestricted as e:
            raise FetchError(UNAVAILABLE, "age-restricted video") from e
        except (yta.VideoUnavailable, yta.InvalidVideoId) as e:
            raise FetchError(UNAVAILABLE, "video is unavailable") from e
        except yta.VideoUnplayable as e:
            raise _unplayable_error(e) from e
        except yta.RequestBlocked as e:  # includes IpBlocked
            raise FetchError(BLOCKED, "YouTube is blocking requests from this IP (RequestBlocked)") from e
        except yta.PoTokenRequired as e:
            raise FetchError(PO_TOKEN, "this caption track needs a PO token (will try yt-dlp)") from e
        except Exception as e:
            detail = ""
            if isinstance(e, getattr(yta, "CouldNotRetrieveTranscript", ())):
                try:  # the library's str() starts with boilerplate; .cause holds the real reason
                    detail = str(e.cause or "").strip()
                except Exception:
                    detail = ""
            text = (detail or str(e)).lower()
            short = detail.splitlines()[0][:200] if detail else _first_line(e)
            if "429" in text or "too many requests" in text or any(p in text for p in _BOT_PATTERNS):
                raise FetchError(BLOCKED, f"YouTube is rate-limiting this IP ({short})") from e
            raise FetchError(ERROR, f"{e.__class__.__name__}: {short}") from e

        segments = [Segment(start=float(sn.start), duration=float(sn.duration), text=_clean(sn.text))
                    for sn in fetched.snippets]
        segments = [sg for sg in segments if sg.text]
        if not segments:
            raise FetchError(ERROR, "transcript came back empty")
        return Transcript(
            video_id=video.video_id,
            language=fetched.language_code,
            language_name=fetched.language,
            kind="translated" if chosen.translated else ("auto" if fetched.is_generated else "manual"),
            method=self.name,
            segments=segments,
        )


# ---- method 2: yt-dlp --------------------------------------------------------------
_BOT_PATTERNS = (
    "not a bot", "sign in to confirm you", "http error 429", "too many requests", "rate-limit", "rate limit",
    "try again later", "captcha",
)
# not finished yet: retried on the next run (statuses other than no_transcript/unavailable are retried)
_NOT_YET_PATTERNS = ("premieres in", "premiere will begin", "live event will begin", "this live event will begin",
                     "is offline")
NOT_YET_MSG = "live stream or premiere that hasn't finished yet - will try again on the next run"
_AGE_PATTERNS = ("confirm your age", "inappropriate for some users", "age-restricted", "age restricted")
_UNAVAILABLE_PATTERNS = (
    "video unavailable", "private video", "members-only", "this video has been removed",
    "age-restricted", "confirm your age", "video is not available",
    "account associated with this video has been terminated", "copyright", "drm protected",
    "join this channel", "requires payment", "not made this video available in your country",
)


def _unplayable_error(e) -> FetchError:
    """youtube-transcript-api lumps every non-OK playability status into VideoUnplayable - including
    YouTube's rate-limit page ("This content isn't available, try again later") and bot checks. Only call
    it permanently unavailable when the reason really says so; otherwise let the next method try."""
    reason = " ".join([str(getattr(e, "reason", "") or "")] + [str(r) for r in (getattr(e, "sub_reasons", None) or [])])
    text = reason.replace("’", "'").lower()
    short = reason.strip().splitlines()[0][:160] if reason.strip() else "no reason given"
    if any(p in text for p in _AGE_PATTERNS):
        return FetchError(UNAVAILABLE, f"age-restricted video: {short}")
    if any(p in text for p in _BOT_PATTERNS):
        return FetchError(BLOCKED, f"YouTube is rate-limiting / bot-checking this IP: {short}")
    if any(p in text for p in _NOT_YET_PATTERNS):
        return FetchError(ERROR, NOT_YET_MSG)
    if any(p in text for p in _UNAVAILABLE_PATTERNS) or "private" in text or "members" in text:
        return FetchError(UNAVAILABLE, f"video is unplayable: {short}")
    return FetchError(ERROR, f"video is unplayable ({short}) - will try another method")


LEVELS = ("max", "lean", "full")  # data-saver profiles, smallest first


class _SaverHealth:
    """Shared by every worker in a run: if a data-saver profile misses captions that a fuller one then
    finds, more than now and then, use the next fuller profile for the rest of the run (correct beats
    cheap): max -> lean -> full."""

    def __init__(self) -> None:
        self.lock = __import__("threading").Lock()
        self.reset()

    def reset(self) -> None:
        self.hits = {lv: 0 for lv in LEVELS}
        self.misses = {lv: 0 for lv in LEVELS}
        self.no_caption_seen = 0
        self.floor = "max"  # the leanest profile still trusted this run

    @property
    def disabled(self) -> bool:
        return self.floor == "full"

    def cap(self, profile: str) -> str:
        """The profile to use: the wanted one, or a fuller one if the wanted one proved unreliable."""
        return LEVELS[max(LEVELS.index(profile), LEVELS.index(self.floor))]

    def check_no_captions(self) -> bool:
        """Should a "no captions" answer from the data saver be double-checked with the full method?
        The first 3 of a run, then every 10th - checking each one would double their cost."""
        with self.lock:
            self.no_caption_seen += 1
            return self.no_caption_seen <= 3 or self.no_caption_seen % 10 == 0

    def hit(self, profile: str = "lean") -> None:
        with self.lock:
            self.hits[profile] = self.hits.get(profile, 0) + 1

    def miss(self, profile: str = "lean") -> None:
        with self.lock:
            self.misses[profile] = n = self.misses.get(profile, 0) + 1
            if profile == "full" or LEVELS.index(self.floor) > LEVELS.index(profile):
                return  # already moved past it
            if n >= 3 and n * 10 > self.hits.get(profile, 0):
                self.floor = LEVELS[LEVELS.index(profile) + 1]
                if self.floor == "full":
                    log.warning("    Data saver switched off for this run: it missed captions that the full "
                                "method found (%d times). Set data_saver = \"off\" if this keeps happening.", n)
                else:
                    log.warning("    Data saver \"max\" missed captions %d times - using \"lean\" for the rest "
                                "of this run (it also loads the watch page). Set data_saver = \"lean\" if this "
                                "keeps happening.", n)


SAVER_HEALTH = _SaverHealth()


def saver_profile(s: Settings) -> str:
    """Which data-saver profile a fetcher with these settings uses (see ytdlp_common.SAVER_ARGS).
    "auto" = the smallest ("max") through proxies, nothing to save on your own connection."""
    mode = str(getattr(s, "data_saver", "auto")).lower()
    if mode == "off":
        return "full"
    if mode in ("on", "lean"):
        want = "lean"
    elif mode == "max" or (mode == "auto" and s.proxy):
        want = "max"
    else:
        return "full"
    if want == "max" and s.translate:
        want = "lean"  # without the watch page YouTube lists no translation languages
    return SAVER_HEALTH.cap(want)


class YtDlpFetcher:
    name = "ytdlp"

    def __init__(self, s: Settings, ydl_factory: Callable | None = None):
        self.settings = s
        self._factory = ydl_factory
        self._ydls: dict[str, object] = {}
        self._loggers: dict[str, object] = {}
        self._logger = None
        self._ydl = None  # the instance used by the current attempt
        self.profile = "full"
        self.last_info: dict | None = None
        self.last_comments: list[dict] = []

    def _get_ydl(self, profile: str = "full"):
        if profile not in self._ydls:
            if self._factory:
                try:
                    self._ydls[profile] = self._factory(profile=profile)
                except TypeError:  # a factory that doesn't know about profiles
                    self._ydls[profile] = self._factory()
            else:
                from .ytdlp_common import YdlLogger, make_ydl

                self._loggers[profile] = YdlLogger()
                # The subtitle flags only make yt-dlp *report* captions it had to drop
                # (e.g. for a missing PO token); nothing is downloaded with download=False.
                extra = {"getcomments": True} if int(getattr(self.settings, "top_comments", 0) or 0) > 0 else {}
                self._ydls[profile] = make_ydl(self.settings, logger=self._loggers[profile], profile=profile,
                                               writesubtitles=True, writeautomaticsub=True, **extra)
        self._logger = self._loggers.get(profile)
        self._ydl = self._ydls[profile]
        return self._ydl

    def _warnings(self) -> list[str]:
        return list(self._logger.warnings) if self._logger else []

    def close(self) -> None:
        for ydl in self._ydls.values():
            try:
                ydl.close()
            except Exception:
                pass
        self._ydls.clear()
        self._ydl = None

    def fetch(self, video: Video) -> Transcript:
        profile = saver_profile(self.settings)
        if profile == "full":
            return self._fetch(video, "full")
        try:
            t = self._fetch(video, profile)
            SAVER_HEALTH.hit(profile)
            return t
        except FetchError as e:
            if e.status in (BLOCKED, UNAVAILABLE):
                raise  # a fuller profile would get the same answer
            if e.status == NO_TRANSCRIPT:
                if "no transcript in" in str(e):  # tracks exist, just not in the wanted languages
                    if profile != "max":
                        raise  # lean sees the same tracks as the full method
                    check = "lean"  # max lists one client's tracks; lean adds the watch page's
                elif SAVER_HEALTH.check_no_captions():
                    check = "full"  # "no captions at all": ask the most complete method
                else:
                    raise
            else:  # an error a leaner profile may have caused (missing visitor data, empty track...)
                check = "lean" if profile == "max" else "full"
            first = e
            log.debug("    data saver %s found nothing (%s) - checking with %s", profile, e, check)
        try:
            t = self._fetch(video, check)
        except FetchError as e2:
            if check == "full" or first.status == NO_TRANSCRIPT or e2.status in (BLOCKED, UNAVAILABLE, NO_TRANSCRIPT):
                raise
            t = self._fetch(video, "full")
        if first.status in (NO_TRANSCRIPT, PO_TOKEN):
            SAVER_HEALTH.miss(profile)  # the saver missed captions a fuller profile found
        return t

    def _fetch(self, video: Video, profile: str) -> Transcript:
        ydl = self._get_ydl(profile)
        self.profile = profile
        self.last_info = None
        self.last_comments = []
        if self._logger:
            self._logger.warnings.clear()
        try:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video.video_id}", download=False,
                                    process=False)
        except Exception as e:
            msg = _first_line(e)
            low = str(e).lower()
            if "confirm your age" in low or "age-restricted" in low:
                raise FetchError(UNAVAILABLE, "age-restricted video") from e
            if any(p in low for p in _BOT_PATTERNS):
                raise FetchError(BLOCKED, "YouTube asked for a bot check / rate-limited (" + msg[:120] + ")") from e
            if any(p in low for p in _NOT_YET_PATTERNS):
                raise FetchError(ERROR, NOT_YET_MSG) from e
            if any(p in low for p in _UNAVAILABLE_PATTERNS):
                raise FetchError(UNAVAILABLE, msg) from e
            if "cookie" in low and ("could not" in low or "failed" in low or "decrypt" in low):
                raise FetchError(ERROR, "couldn't read your browser's cookies - on Windows use "
                                        "cookies_from_browser = \"firefox\" (Chrome/Edge lock theirs)") from e
            raise FetchError(ERROR, msg) from e
        self.last_info = info
        warned = " ".join(self._warnings()).lower()
        rate_limited = any(p in warned for p in ("try again later", "rate-limited", "captcha", "not a bot"))

        def track_map(key: str) -> dict:  # {lang: [format dicts]}, ignoring anything malformed
            raw = info.get(key) if isinstance(info, dict) else None
            return {str(k): [f for f in v if isinstance(f, dict)] for k, v in (raw or {}).items()
                    if isinstance(v, list)} if isinstance(raw, dict) else {}

        subs = track_map("subtitles")
        tracks: list[Track] = []
        for lang, fmts in subs.items():
            if lang == "live_chat" or not fmts:
                continue
            tracks.append(Track(lang=lang, name=_track_name(fmts), generated=False, handle=fmts))
        auto = track_map("automatic_captions")
        manual_langs = set(subs)
        originals = {k[:-5] for k in auto if k.endswith("-orig")}
        for lang, fmts in auto.items():
            if lang.endswith("-orig") or not fmts:
                continue
            # machine translations: of an uploaded track ("de-en" = German from English), or,
            # when an "xx-orig" key exists, every other plain auto key
            from_manual = any(lang.endswith(f"-{m}") and lang != m for m in manual_langs)
            translated = from_manual or (bool(originals) and lang not in originals)
            tracks.append(Track(lang=lang, name=_track_name(fmts), generated=True,
                                translated=translated, handle=fmts))
        chosen = choose_track(tracks, self.settings)
        if chosen is None:
            # one player client being rate-limited while another returned captions is fine;
            # it's only a block when nothing usable came back
            if rate_limited and not tracks:
                raise FetchError(BLOCKED, "YouTube is rate-limiting this session (try again later)")
            pot_dropped = any("PO Token" in w or "PO token" in w for w in self._warnings())
            if pot_dropped:
                raise FetchError(PO_TOKEN, "YouTube wants a PO token for this video's captions, so yt-dlp "
                                           "dropped them (see README: PO token provider)")
            if info.get("live_status") in ("is_live", "is_upcoming"):
                raise FetchError(ERROR, NOT_YET_MSG)
            if not tracks:
                raise FetchError(NO_TRANSCRIPT, "video has no captions")
            have = ", ".join(sorted({t.lang for t in tracks if not t.translated})) or "none"
            raise FetchError(NO_TRANSCRIPT, f"no transcript in {self.settings.languages} (available: {have})")

        order = SMALL_FIRST if profile != "full" else FULL_ORDER
        try:
            segments = self._download_track(ydl, chosen.handle, order)
        except FetchError as e:
            fallback = self._untranslated_fallback(tracks) if chosen.translated and e.status == BLOCKED else None
            if fallback is None:
                raise
            # YouTube rate-limits machine-translated captions on their own (yt-dlp #13831): keep the original
            log.debug("    translated captions refused (%s) - using the original language instead", e)
            chosen = fallback
            segments = self._download_track(ydl, chosen.handle, order)
        if not segments:
            raise FetchError(PO_TOKEN, "caption track downloaded but was empty (YouTube may require a PO token)")
        self.last_comments = self._top_comments(info)
        return Transcript(
            video_id=video.video_id,
            language=chosen.lang,
            language_name=chosen.name,
            kind="translated" if chosen.translated else ("auto" if chosen.generated else "manual"),
            method=self.name,
            segments=segments,
        )

    def _top_comments(self, info) -> list[dict]:
        """The most-liked comments (only when top_comments is set): yt-dlp fetches them lazily, so the
        extra requests happen only here, after the transcript is safely in hand."""
        n = int(getattr(self.settings, "top_comments", 0) or 0)
        post = info.get("__post_extractor") if isinstance(info, dict) else None
        if n <= 0 or not callable(post):
            return []
        try:
            got = post() or {}
        except Exception as e:  # noqa: BLE001 - comments are a bonus; never lose the transcript over them
            log.debug("    comments not available: %s", _first_line(e))
            return []
        out = []
        for c in (got.get("comments") or [])[: n * 2]:
            if not isinstance(c, dict) or c.get("parent", "root") != "root":
                continue
            out.append({"author": str(c.get("author") or ""), "text": str(c.get("text") or "").strip(),
                        "likes": int(c.get("like_count") or 0)})
        out = [c for c in out if c["text"]]
        out.sort(key=lambda c: -c["likes"])
        return out[:n]

    def _untranslated_fallback(self, tracks: list[Track]) -> Track | None:
        import copy

        if not self.settings.allow_other_languages:
            return None
        s = copy.copy(self.settings)
        s.translate = False
        t = choose_track([t for t in tracks if not t.translated], s)
        return t if t is not None and not t.translated else None

    @staticmethod
    def _download_track(ydl, fmts: list[dict], order: tuple[str, ...] | None = None) -> list[Segment]:
        by_ext = {f.get("ext"): f for f in fmts if isinstance(f, dict) and isinstance(f.get("url"), str)}
        last_err: Exception | None = None
        parsers = {"json3": parse_json3, "vtt": parse_vtt, "srv1": parse_srv1}
        for ext in order or FULL_ORDER:
            parser = parsers[ext]
            f = by_ext.get(ext)
            if not f:
                continue
            try:
                raw = ydl.urlopen(_subtitle_request(ydl, f)).read().decode("utf-8", "replace")
            except Exception as e:  # try the next format
                last_err = e
                continue
            segs = parser(raw)
            if segs:
                return segs
        if last_err:
            low = str(last_err).lower()
            status = BLOCKED if any(p in low for p in _BOT_PATTERNS) else ERROR
            raise FetchError(status, f"could not download caption file: {_first_line(last_err)}")
        return []


# caption file formats, in the order tried: srv1 (plain timed text) is the smallest - often a third of
# json3, which carries word-level timing we don't use - so the data saver asks for it first
FULL_ORDER = ("json3", "vtt", "srv1")
SMALL_FIRST = ("srv1", "json3", "vtt")


def _subtitle_request(ydl, fmt: dict):
    """Build the request the way yt-dlp's own downloader does: YouTube caption formats ask for
    browser impersonation, which is used when available (needs the optional curl_cffi package)."""
    if not fmt.get("impersonate"):
        return fmt["url"]
    try:
        from yt_dlp.networking import Request

        target, _ = ydl._parse_impersonate_targets(fmt["impersonate"])
        if target:
            return Request(fmt["url"], extensions={"impersonate": target})
    except Exception:  # older/newer yt-dlp internals, or a test double
        pass
    return fmt["url"]


def _track_name(fmts: list[dict]) -> str:
    for f in fmts or []:
        if f.get("name"):
            return f["name"]
    return ""


# ---- caption file parsers -----------------------------------------------------------
def _clean(text: str) -> str:
    """Whitespace normalisation only - caption text may legitimately contain < and > (code, maths)."""
    text = (text or "").replace("\u200b", "").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


_VTT_TAG = re.compile(r"</?(?:c|i|b|u|v|ruby|rt|lang)(?:[.\s][^>]*)?>|<\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3}>")


def parse_json3(raw: str) -> list[Segment]:
    try:
        data = json.loads(raw)
    except ValueError:
        return []
    out: list[Segment] = []
    events = data.get("events") if isinstance(data, dict) else None
    for ev in events if isinstance(events, list) else []:  # tolerate odd/broken caption data
        if not isinstance(ev, dict) or not isinstance(ev.get("segs"), list):
            continue
        text = _clean("".join(str(s.get("utf8") or "") for s in ev["segs"] if isinstance(s, dict)))
        if not text:
            continue
        start, dur = _ms(ev.get("tStartMs")), _ms(ev.get("dDurationMs"))
        out.append(Segment(start, dur, text))
    return _dedupe_rolling(out)


def _ms(value) -> float:
    try:
        return max(0.0, float(value) / 1000)
    except (TypeError, ValueError):
        return 0.0


_VTT_TS = re.compile(r"(\d+:)?(\d{2}):(\d{2})[.,](\d{3})")


def _vtt_seconds(ts: str) -> float:
    m = _VTT_TS.match(ts.strip())
    if not m:
        return 0.0
    h = int(m.group(1)[:-1]) if m.group(1) else 0
    return h * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4)) / 1000


def parse_vtt(raw: str) -> list[Segment]:
    out: list[Segment] = []
    for block in re.split(r"\r?\n\r?\n", raw):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        for i, ln in enumerate(lines):
            if "-->" in ln:
                a, b = ln.split("-->", 1)
                start, end = _vtt_seconds(a), _vtt_seconds(b.split()[0] if b.split() else "")
                text = _clean(html.unescape(_VTT_TAG.sub("", " ".join(lines[i + 1:]))))
                if text:
                    out.append(Segment(start, max(0.0, end - start), text))
                break
    return _dedupe_rolling(out)


def parse_srv1(raw: str) -> list[Segment]:
    out = []
    for m in re.finditer(r'<text start="([\d.]+)"(?: dur="([\d.]+)")?[^>]*>(.*?)</text>', raw, re.S):
        text = _clean(html.unescape(m.group(3)))  # srv1 is XML: unescape exactly once
        if text:
            out.append(Segment(float(m.group(1)), float(m.group(2) or 0), text))
    return _dedupe_rolling(out)


_SOUND_WORDS = (r"music|applause|laughter|laughs?|laughing|cheering|cheers|inaudible|silence|sighs?|coughs?|"
                r"foreign|noise|background noise|crosstalk|bleep|whistling|clapping|gasps?|groans?|chuckles?|"
                r"sound effects?|indistinct chatter|upbeat music|dramatic music|music playing")
# [Music], (laughs), [upbeat music]... but not "[3]", "[EU]" or "[sic]"-style text that's really content
_SOUND_TAG = re.compile(rf"\[(?:{_SOUND_WORDS})\]|\((?:{_SOUND_WORDS})\)|"
                        r"\[(?=[^\]]*(?-i:[a-z]))[A-Za-z][A-Za-z ,'&-]{3,29}\]|♪+", re.I)


def strip_sound_tags(t: Transcript) -> Transcript:
    """Remove [Music], [Applause], (laughs), ♪ ... and drop segments that become empty."""
    segs = []
    for sg in t.segments:
        text = re.sub(r"\s+", " ", _SOUND_TAG.sub(" ", sg.text)).strip()
        if text:
            segs.append(Segment(sg.start, sg.duration, text))
    t.segments = segs
    return t


# lower case or Capitalised only: "UM" (a university) and "mm" (millimetres) are real words
_FILLER = re.compile(r"(?<![\w'-])(?:[Uu]m+|[Uu]h+m*|[Ee]rm+|[Hh]m+)(?![\w'-])[,.]?")


def remove_filler_words(t: Transcript) -> Transcript:
    """Remove um, uh, erm, hmm (not words like "umbrella" or "hum"); drop segments that become empty."""
    segs = []
    for sg in t.segments:
        text = re.sub(r"\s+([,.?!])", r"\1", re.sub(r"\s+", " ", _FILLER.sub(" ", sg.text))).strip(" ,")
        if text:
            segs.append(Segment(sg.start, sg.duration, text[:1].upper() + text[1:] if sg.text[:1].isupper()
                                else text))
    t.segments = segs
    return t


def _dedupe_rolling(segs: list[Segment]) -> list[Segment]:
    """Auto-captions repeat the previous line in each cue ("rolling" captions). Strip that."""
    out: list[Segment] = []
    for s in segs:
        if out:
            prev = out[-1].text
            if s.text == prev:
                continue
            if s.text.startswith(prev + " "):
                s = Segment(s.start, s.duration, s.text[len(prev) + 1:])
        out.append(s)
    return out


def _first_line(e: Exception) -> str:
    from .utils import short_error

    return short_error(e)
