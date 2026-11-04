import pytest

from yt_transcripts import pipeline, proxies
from yt_transcripts import transcripts as tr
from yt_transcripts.config import ConfigError, build_settings
from yt_transcripts.models import Segment, Transcript, Video


@pytest.mark.parametrize("raw,url", [
    ("http://u:p@1.2.3.4:8000", "http://u:p@1.2.3.4:8000"),
    ("1.2.3.4:8000", "http://1.2.3.4:8000"),
    ("u:p@1.2.3.4:8000", "http://u:p@1.2.3.4:8000"),
    ("1.2.3.4:8000:user:p@ss:word", "http://user:p%40ss%3Aword@1.2.3.4:8000"),
    ("socks5://h.example:1080", "socks5://h.example:1080"),
    ('  "p.webshare.io:80:me-rotate:secret" ', "http://me-rotate:secret@p.webshare.io:80"),
])
def test_normalize(raw, url):
    assert proxies.normalize(raw) == url and proxies.problem(url) == ""


@pytest.mark.parametrize("bad", ["ftp://h:21", "http://:8000", "http://host", "http://host:99999"])
def test_bad_proxies_are_reported(bad):
    assert proxies.problem(proxies.normalize(bad))
    assert build_settings({"keywords": ["x"], "proxy": bad}).validate()


def test_mask_hides_password():
    assert proxies.mask("http://bob:hunter2@h:1") == "http://bob:***@h:1"
    assert proxies.mask("http://h:1") == "http://h:1"


def test_resolve_merges_everything(tmp_path):
    f = tmp_path / "list.txt"
    f.write_text("# my proxies\n5.6.7.8:9000:u:p\n\nhttp://a:1\n", encoding="utf-8")
    s = build_settings({"proxy": "http://a:1  http://b:2", "proxies": ["c:3"], "proxy_file": str(f)})
    proxies.resolve(s, tmp_path)
    assert s.proxies == ["http://a:1", "http://b:2", "http://c:3", "http://u:p@5.6.7.8:9000"]
    assert s.proxy == "http://a:1"
    with pytest.raises(ConfigError, match="does not exist"):
        proxies.resolve(build_settings({"proxy_file": "missing.txt"}), tmp_path)


def test_proxy_reaches_ytdlp_and_transcript_api():
    from yt_transcripts.ytdlp_common import base_options

    s = build_settings({"proxy": "http://u:p@h:8"})
    assert base_options(s)["proxy"] == "http://u:p@h:8"
    session = tr.ApiFetcher(s).api._fetcher._http_client  # youtube-transcript-api's requests session
    assert session.proxies == {"http": "http://u:p@h:8", "https": "http://u:p@h:8"}
    from yt_transcripts.search_api import YouTubeApi

    assert YouTubeApi("KEY", proxy=s.proxy).session.proxies["https"] == "http://u:p@h:8"


class ProxyAwareFetcher:
    """Blocked on proxy A, fine on proxy B."""
    name = "ytdlp"
    last_info = None
    calls: list = []

    def __init__(self, s):
        self.s = s

    def fetch(self, v):
        ProxyAwareFetcher.calls.append(self.s.proxy)
        if self.s.proxy.endswith("a:1"):
            raise tr.FetchError(tr.BLOCKED, "Sign in to confirm you're not a bot")
        return Transcript(v.video_id, "en", "English", "auto", "ytdlp", [Segment(0, 1, "hello")])

    def close(self):
        pass


def test_blocked_proxy_is_swapped_without_waiting(tmp_path, monkeypatch):
    ProxyAwareFetcher.calls = []
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [ProxyAwareFetcher(s)])
    s = build_settings({"keywords": ["x"], "output_dir": str(tmp_path), "delay_seconds": 0,
                        "proxies": ["http://a:1", "http://b:2"]})
    proxies.resolve(s, tmp_path)
    waits = []
    stats = pipeline.download_all([Video(video_id="aaaaaaaaaaa", title="T"), Video(video_id="bbbbbbbbbbb", title="U")],
                                  s, sleep=waits.append)
    assert stats["ok"] == 2 and waits == []  # no rate-limit waiting needed
    assert ProxyAwareFetcher.calls == ["http://a:1", "http://b:2", "http://b:2"]


def test_all_proxies_blocked_falls_back_to_waiting(tmp_path, monkeypatch):
    class AlwaysBlocked(ProxyAwareFetcher):
        def fetch(self, v):
            ProxyAwareFetcher.calls.append(self.s.proxy)
            raise tr.FetchError(tr.BLOCKED, "429")

    ProxyAwareFetcher.calls = []
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [AlwaysBlocked(s)])
    s = build_settings({"keywords": ["x"], "output_dir": str(tmp_path), "delay_seconds": 0,
                        "proxies": ["http://a:1", "http://b:2", "http://c:3"]})
    proxies.resolve(s, tmp_path)
    waits = []
    stats = pipeline.download_all([Video(video_id="aaaaaaaaaaa", title="T")], s, sleep=waits.append)
    assert stats["stopped_blocked"] == 1
    assert ProxyAwareFetcher.calls[:3] == ["http://a:1", "http://b:2", "http://c:3"]  # each proxy tried once
    assert waits == pipeline.BACKOFF_SECONDS[: len(waits)] and waits  # then the usual back-off


def test_search_retries_a_keyword_through_the_next_proxy(monkeypatch):
    from yt_transcripts import search as search_mod
    from yt_transcripts import search_ytdlp as sy

    used = []

    def fake_search(kw, settings, ydl_factory=None, should_stop=None):
        used.append(settings.proxy)
        if settings.proxy.endswith("a:1"):
            raise sy.SearchFailed("no connection to YouTube (Unable to connect to proxy)")
        return [Video(video_id="aaaaaaaaaaa", title="T", views=50_000)]

    monkeypatch.setattr(sy, "search_keyword", fake_search)
    s = build_settings({"keywords": ["x"], "within": "any", "proxies": ["http://a:1", "http://b:2"]})
    proxies.resolve(s, ".")
    vids = search_mod.run_search(s)
    assert used == ["http://a:1", "http://b:2"] and len(vids) == 1 and s.proxy == "http://b:2"


def test_dead_proxy_is_swapped_too(tmp_path, monkeypatch):
    class DeadA(ProxyAwareFetcher):
        def fetch(self, v):
            ProxyAwareFetcher.calls.append(self.s.proxy)
            if self.s.proxy.endswith("a:1"):
                raise tr.FetchError(tr.ERROR, "no connection to YouTube (Unable to connect to proxy)")
            return Transcript(v.video_id, "en", "English", "auto", "ytdlp", [Segment(0, 1, "hello")])

    ProxyAwareFetcher.calls = []
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [DeadA(s)])
    s = build_settings({"keywords": ["x"], "output_dir": str(tmp_path), "delay_seconds": 0,
                        "proxies": ["http://a:1", "http://b:2"]})
    proxies.resolve(s, tmp_path)
    stats = pipeline.download_all([Video(video_id="aaaaaaaaaaa", title="T")], s, sleep=lambda x: None)
    assert stats["ok"] == 1 and ProxyAwareFetcher.calls == ["http://a:1", "http://b:2"]


@pytest.mark.parametrize("raw,masked", [
    ("http://user:pa/ss@h:8080", "http://user:***@h:8080"),
    ("http://user:p@ss@h:8080", "http://user:***@h:8080"),
    ("http://token@h:8080", "http://***@h:8080"),
    ("user:p;w@h:1", "http://user:***@h:1"),
])
def test_special_characters_in_passwords_work_and_never_leak(raw, masked):
    url = proxies.normalize(raw)
    assert proxies.problem(url) == "" and proxies.mask(url) == masked


def test_system_proxy_cannot_override_the_configured_one(monkeypatch):
    from yt_transcripts.search_api import YouTubeApi

    monkeypatch.setenv("HTTPS_PROXY", "http://system-proxy:3128")
    s = build_settings({"proxy": "http://mine:8080"})
    for session in (tr.ApiFetcher(s).api._fetcher._http_client, YouTubeApi("K", proxy=s.proxy).session):
        settings = session.merge_environment_settings("https://www.youtube.com/", {}, None, None, None)
        assert settings["proxies"]["https"] == "http://mine:8080"


def test_command_line_proxy_replaces_config_proxies(tmp_path):
    from yt_transcripts import cli

    cfg = tmp_path / "c.toml"
    cfg.write_text('proxies = ["http://cfg1:1", "http://cfg2:2"]\n', encoding="utf-8")
    s = cli.settings_from_args(cli.build_parser().parse_args(["status", "-c", str(cfg), "--proxy", "http://cli:9"]))
    assert s.proxies == ["http://cli:9"] and s.proxy == "http://cli:9"
    s = cli.settings_from_args(cli.build_parser().parse_args(["status", "-c", str(cfg)]))
    assert s.proxies == ["http://cfg1:1", "http://cfg2:2"]
