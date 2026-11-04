"""Parallel downloads: correctness under threads (outcomes, never timing)."""
import json
import threading

import pytest

from yt_transcripts import pipeline, proxies
from yt_transcripts import transcripts as tr
from yt_transcripts.config import build_settings
from yt_transcripts.models import Segment, Transcript, Video
from yt_transcripts.workers import Engine, Job


def _vids(n):
    return [Video(video_id=f"v{i:010d}", title=f"Video {i}", views=1000, keyword="k") for i in range(n)]


def _t(vid):
    return Transcript(vid, "en", "English", "auto", "ytdlp", [Segment(0, 1, f"text of {vid}")])


class Fetcher:
    """Behaviour scripted per proxy; records (proxy, video) calls from every thread."""
    name = "ytdlp"
    last_info = None
    calls: list = []
    lock = threading.Lock()
    behaviour = staticmethod(lambda proxy, vid: _t(vid))
    barrier = None

    def __init__(self, s):
        self.proxy = s.proxy

    def fetch(self, v):
        with Fetcher.lock:
            Fetcher.calls.append((self.proxy, v.video_id))
        if Fetcher.barrier is not None:
            Fetcher.barrier.wait()  # proves N fetches really run at the same time
        out = Fetcher.behaviour(self.proxy, v.video_id)
        if isinstance(out, Exception):
            raise out
        return out

    def close(self):
        pass


@pytest.fixture
def fake(monkeypatch, tmp_path):
    Fetcher.calls = []
    Fetcher.barrier = None
    Fetcher.behaviour = staticmethod(lambda proxy, vid: _t(vid))
    monkeypatch.setattr(pipeline, "build_fetchers", lambda s, ydl_factory=None: [Fetcher(s)])

    def settings(**kw):
        s = build_settings({"keywords": ["k"], "output_dir": str(tmp_path / "out"), "delay_seconds": 0,
                            "formats": ["txt", "json"], **kw})
        proxies.resolve(s, tmp_path)
        return s
    return settings


def _manifest(s):
    return json.loads((pipeline.Path(s.output_dir) / "manifest.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("attempt", range(5))
def test_three_proxies_download_in_parallel(fake, attempt):
    s = fake(proxies=["http://a:1", "http://b:2", "http://c:3"])
    assert s.resolved_workers() == 3
    Fetcher.barrier = threading.Barrier(3, timeout=10)  # would time out if the work were sequential
    vids = _vids(6)
    stats = pipeline.download_all(vids, s)
    assert stats["ok"] == 6
    assert {p for p, _ in Fetcher.calls} == {"http://a:1", "http://b:2", "http://c:3"}
    assert {r["status"] for r in _manifest(s).values()} == {"ok"}
    assert all(v.transcript_status == "ok" for v in vids)
    combined = list((pipeline.Path(s.output_dir) / "combined").glob("*.md"))[0].read_text(encoding="utf-8")
    positions = [combined.index(f"text of {v.video_id}") for v in vids]
    assert positions == sorted(positions)  # combined file keeps list order, not finishing order


@pytest.mark.parametrize("attempt", range(5))
def test_blocked_proxy_is_benched_and_its_video_finished_elsewhere(fake, attempt):
    Fetcher.behaviour = staticmethod(
        lambda proxy, vid: tr.FetchError(tr.BLOCKED, "not a bot") if proxy == "http://a:1" else _t(vid))
    s = fake(proxies=["http://a:1", "http://b:2", "http://c:3"])
    stats = pipeline.download_all(_vids(9), s)
    assert stats["ok"] == 9 and stats["stopped_blocked"] == 0
    assert sum(1 for p, _ in Fetcher.calls if p == "http://a:1") <= 2  # benched after its first block


def test_all_proxies_blocked_in_parallel_backs_off_then_stops(fake):
    Fetcher.behaviour = staticmethod(lambda proxy, vid: tr.FetchError(tr.BLOCKED, "429"))
    s = fake(proxies=["http://a:1", "http://b:2"])
    waits = []
    stats = pipeline.download_all(_vids(4), s, sleep=waits.append)
    assert stats["stopped_blocked"] == 1 and stats["ok"] == 0
    assert waits and waits == pipeline.BACKOFF_SECONDS[: len(waits)]
    assert _manifest(s) == {} or all(r.get("status") != "ok" for r in _manifest(s).values())


@pytest.mark.parametrize("attempt", range(3))
def test_stop_partway_keeps_finished_work(fake, attempt):
    s = fake(proxies=["http://a:1", "http://b:2"])
    done = []
    Fetcher.behaviour = staticmethod(lambda proxy, vid: done.append(vid) or _t(vid))
    stats = pipeline.download_all(_vids(40), s, should_stop=lambda: len(done) >= 5)
    assert stats["interrupted"] == 1 and 5 <= stats["ok"] < 40
    m = _manifest(s)
    assert len(m) == stats["ok"] and {r["status"] for r in m.values()} == {"ok"}


def test_rotating_service_reconnects_instead_of_benching(fake):
    tries = {}

    def behaviour(proxy, vid):
        tries[vid] = tries.get(vid, 0) + 1
        return tr.FetchError(tr.BLOCKED, "429") if tries[vid] == 1 else _t(vid)  # first IP blocked, next fine

    Fetcher.behaviour = staticmethod(behaviour)
    s = fake(proxy="http://me-rotate:pw@p.webshare.io:80", workers_per_proxy=3)
    assert s.resolved_workers() == 3
    waits = []
    stats = pipeline.download_all(_vids(6), s, sleep=waits.append)
    assert stats["ok"] == 6 and waits == []  # no back-off waits: a reconnect means a new IP


def test_cookies_force_one_worker(fake):
    s = fake(proxies=["http://a:1", "http://b:2"], cookies_from_browser="firefox")
    assert s.resolved_workers() == 1
    stats = pipeline.download_all(_vids(3), s)
    assert stats["ok"] == 3 and {p for p, _ in Fetcher.calls} == {"http://a:1"}


def test_max_transcripts_per_run_is_exact_with_workers(fake):
    s = fake(proxies=["http://a:1", "http://b:2", "http://c:3"], max_transcripts_per_run=4)
    stats = pipeline.download_all(_vids(10), s)
    assert stats["ok"] == 4 and stats["left_for_next_run"] == 6 and len(Fetcher.calls) == 4


def test_worker_crash_is_reported_not_swallowed(fake):
    Fetcher.behaviour = staticmethod(lambda proxy, vid: RuntimeError("bug in a fetcher"))
    s = fake(proxies=["http://a:1", "http://b:2"])
    # unexpected exceptions inside fetch_one are turned into ERROR results, so the run completes
    stats = pipeline.download_all(_vids(3), s)
    assert stats["error"] == 3


def test_hourly_budget_pauses_instead_of_overrunning():
    clock = [0.0]
    pool = proxies.ProxyPool([], clock=lambda: clock[0])
    s = build_settings({"keywords": ["k"], "delay_seconds": 0, "videos_per_hour_per_ip": 2})
    waits = []

    def sleep(sec):
        waits.append(sec)
        clock[0] += sec

    class F:
        name = "ytdlp"
        last_info = None

        def fetch(self, v):
            return _t(v.video_id)

    results = []
    jobs = [Job(i, v) for i, v in enumerate(_vids(5))]
    eng = Engine(jobs, s, pool, build_fetchers=lambda ws, f=None: [F()], fetch_one=pipeline.fetch_one,
                 breaker=pipeline.MethodBreaker(), looks_offline=pipeline._looks_offline,
                 backoff=pipeline.BACKOFF_SECONDS, on_result=lambda r: results.append(r) or None, sleep=sleep)
    assert eng.run(1) == ""
    assert len(results) == 5
    assert sum(waits) >= 3600 * 2 - 1  # 5 videos at 2 per hour: two full-hour pauses


def test_proxy_pool_unit_behaviour():
    clock = [1000.0]
    pool = proxies.ProxyPool(["http://a:1", "http://b:2"], clock=lambda: clock[0])
    a = pool.try_lease()
    b = pool.try_lease()
    assert {a.url, b.url} == {"http://a:1", "http://b:2"} and pool.try_lease() is None  # 1 per proxy
    pool.trouble(a, dead=False)
    pool.release(a)
    assert pool.try_lease() is None  # a is benched, b is leased
    clock[0] += proxies.BENCH_BLOCKED_SECONDS + 1
    assert pool.try_lease() is a  # rested
    for _ in range(3):
        pool.trouble(b, dead=True)
    assert b.retired and pool.usable_count() == 1


# ---- parallel keyword searches ------------------------------------------------------------------------
def _fake_search(monkeypatch, behaviour):
    from yt_transcripts import search_ytdlp as sy

    calls = []
    lock = threading.Lock()

    def fake(kw, settings, ydl_factory=None, should_stop=None):
        with lock:
            calls.append((settings.proxy, kw))
        return behaviour(kw, settings)

    monkeypatch.setattr(sy, "search_keyword", fake)
    return calls


def _hits(kw, n=3):
    import datetime as dt

    base = dt.datetime(2026, 10, 28, tzinfo=dt.timezone.utc)
    return [Video(video_id=f"{kw[:3]}{j:08d}", title=f"{kw} {j}", views=50_000 + j, keyword=kw,
                  published=(base - dt.timedelta(hours=j * 7 + len(kw))).isoformat(), published_exact=True,
                  duration_seconds=600) for j in range(n)] + \
        [Video(video_id="shared00001", title="in every keyword", views=99_999, keyword=kw,
               published=base.isoformat(), published_exact=True, duration_seconds=600)]


@pytest.mark.parametrize("attempt", range(3))
def test_keywords_are_searched_in_parallel(monkeypatch, attempt):
    from yt_transcripts.search import run_search

    barrier = threading.Barrier(2, timeout=10)

    def behaviour(kw, settings):
        barrier.wait()  # two searches at once, or this times out
        return _hits(kw)

    calls = _fake_search(monkeypatch, behaviour)
    s = build_settings({"keywords": ["alpha", "beta", "gamma", "delta"], "within": "any", "min_views": 0,
                        "proxies": ["http://a:1", "http://b:2"]})
    proxies.resolve(s, ".")
    vids = run_search(s)
    assert len(calls) == 4 and {p for p, _ in calls} == {"http://a:1", "http://b:2"}
    shared = [v for v in vids if v.video_id == "shared00001"][0]
    assert shared.keyword == "alpha; beta; gamma; delta"  # merged in keyword order


def test_parallel_search_gives_exactly_the_sequential_result(monkeypatch):
    import random
    import time as _time

    from yt_transcripts.search import run_search

    def behaviour(kw, settings):
        _time.sleep(random.uniform(0, 0.02))  # finish in random order
        return _hits(kw, 5)

    _fake_search(monkeypatch, behaviour)
    kws = ["one", "two", "three", "four", "five", "six"]

    def run(**kw):
        s = build_settings({"keywords": kws, "within": "any", "min_views": 0, **kw})
        proxies.resolve(s, ".")
        return [(v.video_id, v.keyword, v.published) for v in run_search(s)]

    expected = run()
    for _ in range(20):
        assert run(proxies=["http://a:1", "http://b:2", "http://c:3"]) == expected


def test_a_failed_search_is_retried_through_another_proxy(monkeypatch):
    from yt_transcripts import search_ytdlp as sy
    from yt_transcripts.search import run_search

    def behaviour(kw, settings):
        if settings.proxy == "http://a:1":
            raise sy.SearchFailed("no connection to YouTube (Unable to connect to proxy)")
        return _hits(kw)

    calls = _fake_search(monkeypatch, behaviour)
    s = build_settings({"keywords": ["alpha", "beta"], "within": "any", "min_views": 0,
                        "proxies": ["http://a:1", "http://b:2"]})
    proxies.resolve(s, ".")
    vids = run_search(s)
    assert {v.keyword for v in vids if v.video_id != "shared00001"} == {"alpha", "beta"}
    assert sum(1 for p, _ in calls if p == "http://a:1") == 1  # benched after failing once
    assert s.proxy == "http://b:2"  # downloads will start with the proxy that worked


# ---- regressions found by the independent review -------------------------------------------------
def _within(fn, secs=10):
    """Run fn in a thread; fail (instead of hanging the test suite) if it doesn't finish."""
    out = {}

    def go():
        try:
            out["r"] = fn()
        except BaseException as e:  # noqa: BLE001
            out["e"] = e
    th = threading.Thread(target=go, daemon=True)
    th.start()
    th.join(secs)
    assert not th.is_alive(), "run hung"
    if "e" in out:
        raise out["e"]
    return out["r"]


def test_more_workers_than_proxy_slots_neither_hangs_nor_waits(fake):
    import time

    s = fake(proxies=["http://a:1"], workers=4)
    Fetcher.behaviour = staticmethod(lambda p, v: (time.sleep(0.02), _t(v))[1])
    stats = _within(lambda: pipeline.download_all(_vids(6), s))
    assert stats["ok"] == 6


def test_dead_proxy_does_not_strand_its_video(fake):
    import time

    s = fake(proxies=["http://a:1", "http://b:2"])

    def beh(proxy, vid):
        if proxy == "http://b:2":
            return tr.FetchError(tr.ERROR, "No connection: connection refused")
        time.sleep(0.02)
        return _t(vid)
    Fetcher.behaviour = staticmethod(beh)
    stats = _within(lambda: pipeline.download_all(_vids(4), s, sleep=lambda x: None))
    assert stats["ok"] == 4


def test_blocked_proxys_video_moves_to_the_idle_one_at_once(fake, monkeypatch):
    import time

    monkeypatch.setattr(proxies, "BENCH_BLOCKED_SECONDS", 30)  # waiting this out would fail the test
    s = fake(proxies=["http://a:1", "http://b:2"])

    def beh(proxy, vid):
        time.sleep(0.02)
        return tr.FetchError(tr.BLOCKED, "429") if proxy == "http://b:2" else _t(vid)
    Fetcher.behaviour = staticmethod(beh)
    stats = _within(lambda: pipeline.download_all(_vids(2), s, sleep=lambda x: None), 10)
    assert stats["ok"] == 2


def test_saving_failure_stops_the_workers(fake, monkeypatch):
    import time

    s = fake(proxies=["http://a:1", "http://b:2"])
    Fetcher.behaviour = staticmethod(lambda p, v: (time.sleep(0.02), _t(v))[1])

    def boom(*a, **k):
        raise OSError(28, "No space left on device")
    monkeypatch.setattr(pipeline, "write_transcript", boom)
    with pytest.raises(OSError):
        pipeline.download_all(_vids(40), s)
    n = len(Fetcher.calls)
    time.sleep(0.3)
    assert len(Fetcher.calls) == n < 40  # nobody keeps downloading videos that can't be saved
    assert not [t for t in threading.enumerate() if t.name.startswith("worker") and t.is_alive()]


def test_api_unavailable_does_not_override_ytdlp_blocked():
    class F:
        def __init__(self, name, status):
            self.name, self.status = name, status

        def fetch(self, v):
            raise tr.FetchError(self.status, f"{self.name} says {self.status}")
    v = _vids(1)[0]
    for ytdlp_status in (tr.BLOCKED, tr.PO_TOKEN, tr.ERROR):
        _, status, _, _ = pipeline.fetch_one(v, [F("ytdlp", ytdlp_status), F("api", tr.UNAVAILABLE)], None)
        assert status == ytdlp_status
    _, status, _, _ = pipeline.fetch_one(v, [F("api", tr.UNAVAILABLE)], None)  # api alone: believed
    assert status == tr.UNAVAILABLE


def test_po_token_schedule_counts_token_hits_not_all_attempts(fake):
    s = fake()
    vids = _vids(1)
    Fetcher.behaviour = staticmethod(lambda p, v: tr.FetchError(tr.ERROR, "network glitch"))
    for _ in range(3):
        pipeline.download_all(vids, s, sleep=lambda x: None)
    Fetcher.behaviour = staticmethod(lambda p, v: tr.FetchError(tr.PO_TOKEN, "needs a token"))
    pipeline.download_all(vids, s, sleep=lambda x: None)
    rec = _manifest(s)[vids[0].video_id]
    assert rec["po_token_hits"] == 1 and rec["attempts"] == 4
    import datetime as dt

    due = pipeline.parse_retry_time(rec["next_retry"])
    hours = (due - dt.datetime.now(due.tzinfo)).total_seconds() / 3600
    assert 5 < hours <= 6  # first token wall: retry in 6 h, not a week


def test_search_waits_for_a_busy_proxy_instead_of_dropping_keywords(monkeypatch):
    import time

    from yt_transcripts import search_ytdlp as sy
    from yt_transcripts.search import run_search

    def beh(kw, settings):
        if settings.proxy == "http://a:1":
            raise sy.SearchFailed("HTTP Error 429: too many requests")
        time.sleep(0.2)
        return _hits(kw)
    calls = _fake_search(monkeypatch, beh)
    s = build_settings({"keywords": ["alpha", "beta", "gamma", "delta"], "within": "any", "min_views": 0,
                        "proxies": ["http://a:1", "http://b:2"]})
    proxies.resolve(s, ".")
    vids = _within(lambda: run_search(s), 20)
    assert {"alpha", "beta", "gamma", "delta"} <= {k for v in vids for k in v.keyword.split("; ")}
    s = build_settings({"keywords": ["alpha", "beta", "gamma"], "within": "any", "min_views": 0,
                        "proxies": ["http://b:2"], "workers": 4})
    proxies.resolve(s, ".")
    calls.clear()
    vids = _within(lambda: run_search(s), 20)
    assert len(calls) == 3 and {k for v in vids for k in v.keyword.split("; ")} == {"alpha", "beta", "gamma"}
