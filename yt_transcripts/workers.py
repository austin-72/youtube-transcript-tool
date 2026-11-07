"""Run transcript downloads with one or more workers.

Workers only talk to YouTube; everything else (writing files, the manifest, statistics, the log) happens
in ONE place - the coordinator callback - so nothing on disk is ever written by two threads at once.
With a single worker no thread is started at all: the worker runs inline, exactly like the classic
one-video-at-a-time loop.

Each worker leases a "slot" (a proxy, or the direct connection) from the ProxyPool and has its own
Settings copy, its own yt-dlp instance and its own HTTP session. When YouTube blocks a slot - or a proxy
doesn't connect - the worker benches it, hands the video back to the queue and carries on with another
slot. For rotating proxy services (a new IP per connection) it first just reconnects and retries.
"""

from __future__ import annotations

import collections
import copy
import heapq
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Callable

from . import netmeter
from . import transcripts as tr
from .config import Settings
from .models import Transcript, Video
from .proxies import ProxyPool, Slot

log = logging.getLogger("yt_transcripts")

ROTATING_RETRIES = 3  # rotating service blocked: reconnect (= new IP) and retry this many times first
SWITCH_AUTO = 10  # with a long proxy list, move to the next proxy after this many videos
SWITCH_AUTO_MIN_PROXIES = 8  # ...when the list has at least this many
MAX_PROXIES_PER_VIDEO = 10  # a video blocked through this many proxies is given up for this run


def switch_after(s, pool) -> int:
    """Videos per proxy before a worker moves on (0 = stay until it's blocked). "auto": a list of 8+
    proxies is worked through round-robin, 10 videos each - each IP stays far under YouTube's limits."""
    v = str(getattr(s, "proxy_switch_after", "auto")).strip().lower()
    if v != "auto":
        try:
            return max(0, int(float(v)))
        except ValueError:
            return 0
    fixed = [x for x in pool.slots if x.url and not x.rotating]
    return SWITCH_AUTO if len(fixed) >= SWITCH_AUTO_MIN_PROXIES else 0


@dataclass(order=True)
class Job:
    index: int
    video: Video = field(compare=False)
    rec: dict = field(compare=False, default_factory=dict)
    requeues: int = field(compare=False, default=0)
    fresh: int = field(compare=False, default=0)


@dataclass
class Result:
    job: Job
    transcript: Transcript | None
    status: str
    message: str
    method: str
    via: str = ""


class JobQueue:
    """Priority queue (original list order) that knows when every job is finished - requeued jobs
    included - so idle workers know whether to wait or to stop."""

    def __init__(self, jobs: list[Job]):
        self._heap = list(jobs)
        heapq.heapify(self._heap)
        self._outstanding = len(jobs)
        self._cond = threading.Condition()

    def get_nowait(self) -> Job | None:
        with self._cond:
            return heapq.heappop(self._heap) if self._heap else None

    def get(self, stopping: Callable[[], bool]) -> Job | None:
        with self._cond:
            while True:
                if stopping() or self._outstanding <= 0:
                    return None
                if self._heap:
                    return heapq.heappop(self._heap)
                self._cond.wait(0.2)

    def put_back(self, job: Job) -> None:
        with self._cond:
            heapq.heappush(self._heap, job)
            self._cond.notify_all()

    def done(self) -> None:
        with self._cond:
            self._outstanding -= 1
            self._cond.notify_all()

    def remaining(self) -> int:
        with self._cond:
            return self._outstanding

    def wake(self) -> None:
        with self._cond:
            self._cond.notify_all()


class Engine:
    def __init__(self, jobs: list[Job], s: Settings, pool: ProxyPool, *, build_fetchers: Callable,
                 fetch_one: Callable, breaker, looks_offline: Callable[[str], bool], backoff: list[int],
                 on_result: Callable[[Result], str | None], ydl_factory: Callable | None = None,
                 sleep: Callable[[float], None] = time.sleep, should_stop: Callable[[], bool] | None = None):
        self.s = s
        self.pool = pool
        self.jobs = JobQueue(jobs)
        self.build_fetchers = build_fetchers
        self.fetch_one = fetch_one
        self.breaker = breaker
        self.looks_offline = looks_offline
        self.backoff = backoff
        self.on_result = on_result
        self.ydl_factory = ydl_factory
        self.sleep = sleep
        self.should_stop = should_stop
        self.halt = threading.Event()
        self.halt_reason = ""
        self.results: collections.deque[Result] = collections.deque()
        self.results_lock = threading.Lock()
        self.inline = True
        self.error: BaseException | None = None
        self._said_hourly = False
        self.switch_after = switch_after(s, pool)
        pool.per_hour = int(s.videos_per_hour_per_ip or 0)

    # -- stopping & waiting --------------------------------------------------------------------------
    def stopping(self) -> bool:
        if self.halt.is_set():
            return True
        if self.should_stop and self.should_stop():
            self.stop("interrupted")
            return True
        return False

    def stop(self, reason: str) -> None:
        if not self.halt_reason:
            self.halt_reason = reason
        self.halt.set()
        self.jobs.wake()

    def wait(self, seconds: float) -> None:
        """Sleep, but wake up promptly on Stop (tests inject their own `sleep`)."""
        if seconds <= 0:
            return
        if self.sleep is not time.sleep:
            self.sleep(seconds)
            return
        end = time.monotonic() + seconds
        while not self.stopping():
            left = end - time.monotonic()
            if left <= 0:
                return
            self.halt.wait(min(0.5, left))

    def _polite_gap(self) -> None:
        import random

        d = self.s.delay_seconds
        if d > 0:
            self.wait(max(0.0, d * (1 + random.uniform(-0.5, 0.5))) if self.sleep is time.sleep else d)

    # -- results -----------------------------------------------------------------------------------------
    def _emit(self, result: Result) -> None:
        if self.inline:
            reason = self.on_result(result)
            if reason:
                self.stop(reason)
        else:
            with self.results_lock:
                self.results.append(result)

    # -- one worker --------------------------------------------------------------------------------------
    def _fetchers_for(self, slot: Slot) -> list:
        ws = copy.copy(self.s)  # own copy: workers must never see each other's proxy
        ws.proxy = netmeter.route(slot.url, hold=True)  # through the data meter's relay, which counts the bytes
        return self.build_fetchers(ws, self.ydl_factory)

    def _retire(self, fetchers, slot: Slot | None) -> None:
        """Done with this slot's fetchers: close them, then give its relay back."""
        self._close(fetchers)
        if fetchers is not None and slot is not None and slot.url:
            netmeter.drop(slot.url)

    @staticmethod
    def _close(fetchers) -> None:
        for f in fetchers or []:
            close = getattr(f, "close", None)
            if close:
                try:
                    close()
                except Exception:
                    pass

    def worker(self, prefer_url: str = "") -> None:
        slot: Slot | None = None
        fetchers: list | None = None
        own_starts: collections.deque[float] = collections.deque()  # hourly budget for rotating services
        held = 0  # videos done through the current slot
        prefer = next((x for x in self.pool.slots if x.url == prefer_url), None) if prefer_url else None
        try:
            while not self.stopping():
                job = self.jobs.get_nowait()
                if job is None:
                    if self.jobs.remaining() <= 0:
                        break
                    if slot is not None:
                        # nothing to do right now (other workers hold the last videos): hand the slot
                        # back, so a worker whose own slot is resting or dead can use it meanwhile
                        self._retire(fetchers, slot)
                        self.pool.release(slot)
                        slot, fetchers = None, None
                    job = self.jobs.get(self.stopping)
                    if job is None:
                        break
                if slot is None:
                    slot = self.pool.acquire(prefer=prefer, backoff=self.backoff,
                                             max_rounds=self.s.max_consecutive_blocks,
                                             wait=self.wait, stopping=self.stopping)
                    prefer = None
                    if slot is None:
                        self.jobs.put_back(job)
                        self.stop(self.pool.stopped or "interrupted")
                        break
                    fetchers = self._fetchers_for(slot)
                    held = 0
                sess = netmeter.active()
                if slot.url and sess is not None and sess.limit_reached():
                    self.jobs.put_back(job)
                    self.stop("data_limit")
                    break
                budget = self._within_budget(slot, own_starts)
                if budget == "switch":  # this proxy's hourly budget is used up, another one is free
                    self._retire(fetchers, slot)
                    self.pool.release(slot)
                    slot, fetchers = None, None
                    self.jobs.put_back(job)
                    continue
                if not budget:
                    self.jobs.put_back(job)
                    break
                fs = self.breaker.prune(fetchers)
                # videos from a bare link list have no title/date yet: yt-dlp returns them with the captions
                order = fs if job.video.title else sorted(fs, key=lambda f: f.name != "ytdlp")
                t, status, msg, method = self.fetch_one(job.video, order, self.breaker)

                dead = status == tr.ERROR and bool(slot.url) and self.looks_offline(msg)
                if status == tr.BLOCKED or dead:
                    if slot.rotating and job.fresh < ROTATING_RETRIES and not dead:
                        job.fresh += 1  # a rotating service: a new connection is a new IP - just retry
                        log.info("    %s was blocked - reconnecting for a fresh IP (try %d of %d)",
                                 slot.label, job.fresh, ROTATING_RETRIES)
                        self._retire(fetchers, slot)
                        fetchers = self._fetchers_for(slot)
                        self.jobs.put_back(job)
                        continue
                    self.pool.trouble(slot, dead=dead)
                    others = self.pool.usable_count() > 1
                    log.warning("    %s %s%s", "Could not connect through" if dead else "YouTube blocked",
                                slot.label, " - switching" if others else "")
                    self._retire(fetchers, slot)
                    self.pool.release(slot)
                    used, slot, fetchers = slot, None, None
                    job.requeues += 1
                    if job.requeues > min(len(self.pool.slots), MAX_PROXIES_PER_VIDEO) + len(self.backoff) + 2:
                        self._count(used)
                        self._emit(Result(job, None, status, msg, method))  # give this one up for now
                        self.jobs.done()
                    else:
                        self.jobs.put_back(job)
                    continue

                if status in (tr.OK, tr.NO_TRANSCRIPT, tr.UNAVAILABLE, tr.PO_TOKEN):
                    self.pool.ok(slot)  # YouTube answered normally through this slot
                self._count(slot)
                self._emit(Result(job, t, status, msg, method, slot.label if slot.url else ""))
                self.jobs.done()
                held += 1
                if (self.switch_after and slot.url and not slot.rotating and held >= self.switch_after
                        and self.pool.has_free(besides=slot)):
                    # a long list: move on to the proxy that has rested longest, so no IP does too much
                    self._retire(fetchers, slot)
                    self.pool.release(slot)
                    slot, fetchers = None, None
                if self.jobs.remaining() > 0 and not self.stopping():
                    self._polite_gap()
        except BaseException as e:  # noqa: BLE001 - surfaced by run()
            if self.inline:
                raise
            self.error = e
            self.stop("error")
        finally:
            self._retire(fetchers, slot)
            if slot is not None:
                self.pool.release(slot)

    @staticmethod
    def _count(slot: Slot | None) -> None:
        """One finished video through a proxy (retries of the same video aren't counted again)."""
        sess = netmeter.active()
        if slot is not None and slot.url and sess is not None:
            sess.count_video()

    def _within_budget(self, slot: Slot, own_starts) -> bool | str:
        """True = go; "switch" = this proxy's hour is used up but another one is free; False = stopped."""
        per_hour = self.s.videos_per_hour_per_ip
        hist = own_starts if slot.rotating else slot.starts
        while True:
            w = self.pool.budget_wait_seconds(hist, per_hour)
            if w <= 0:
                return True
            if slot.url and not slot.rotating and self.pool.has_free(besides=slot):
                return "switch"
            if not self._said_hourly:
                self._said_hourly = True
                log.info("    Hourly limit reached (%d videos per hour per IP, see videos_per_hour_per_ip) - "
                         "pausing about %d min so YouTube doesn't block us.", per_hour, max(1, round(w / 60)))
            self.wait(min(w, 60.0))
            if self.stopping():
                return False

    # -- run -------------------------------------------------------------------------------------------
    def run(self, n_workers: int, prefer_url: str = "") -> str:
        """Process every job. Returns why it ended early ("" = finished)."""
        if n_workers <= 1:
            self.inline = True
            self.worker(prefer_url)
            return self.halt_reason
        self.inline = False
        threads = []
        for k in range(n_workers):
            th = threading.Thread(target=self.worker, name=f"worker{k + 1}", daemon=True,
                                  args=(prefer_url if k == 0 else "",))
            threads.append(th)
            th.start()
            if k < n_workers - 1 and self.s.delay_seconds > 0:
                self.wait(self.s.delay_seconds / n_workers)  # staggered start: no burst of N requests
        try:
            while True:
                self._drain()
                alive = any(th.is_alive() for th in threads)
                if not alive:
                    break
                if self.should_stop and self.should_stop():
                    self.stop("interrupted")
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop("interrupted")
            for th in threads:
                th.join(timeout=self.s.request_sleep + 35)
            self._drain()
            raise
        except BaseException:
            # saving a result failed (disk full, file locked...): stop the workers instead of letting
            # them download videos nobody will save
            self.stop("error")
            for th in threads:
                th.join(timeout=self.s.request_sleep + 35)
            raise
        self._drain()
        if self.error is not None:
            raise self.error
        return self.halt_reason

    def _drain(self) -> None:
        while True:
            with self.results_lock:
                if not self.results:
                    return
                r = self.results.popleft()
            reason = self.on_result(r)
            if reason:
                self.stop(reason)
