"""Proxy handling: parse the formats proxy sellers hand out, hide passwords in logs, rotate on blocks."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote, urlsplit

SCHEMES = ("http", "https", "socks5", "socks5h", "socks4", "socks4a")


def normalize(raw: str) -> str:
    """Turn any common proxy notation into a URL.

    Accepted:  http://user:pass@host:port   socks5://host:port   host:port   user:pass@host:port
               host:port:user:pass (the "IP:Port:Username:Password" lists many proxy shops export)
    """
    p = (raw or "").strip().strip('"').strip("'")
    if not p:
        return ""
    if "://" in p:
        return _encode_userinfo(p)
    parts = p.split(":")
    # host:port:user:pass  (numeric port in the second place; the password may contain : or @)
    if len(parts) >= 4 and parts[1].isdigit() and "@" not in parts[0]:
        host, port, user, pw = parts[0], parts[1], parts[2], ":".join(parts[3:])
        return f"http://{quote(user, safe='')}:{quote(pw, safe='')}@{host}:{port}"
    return _encode_userinfo(f"http://{p}")


def _encode_userinfo(url: str) -> str:
    """Percent-encode special characters (/ @ : # ...) in the user name and password, so a password like
    'p@ss/word' still works. Already-encoded parts (%40) are left alone."""
    scheme, rest = url.split("://", 1)
    at = rest.rfind("@")  # the LAST @ ends the credentials: passwords may contain @
    if at < 0:
        return url
    userinfo, hostpart = rest[:at], rest[at + 1:]
    user, sep, pw = userinfo.partition(":")
    enc = quote(user, safe="%") + (sep + quote(pw, safe="%") if sep else "")
    return f"{scheme}://{enc}@{hostpart}"


def problem(url: str) -> str:
    """Why a (normalized) proxy URL can't be used, or ''."""
    try:
        u = urlsplit(url)
        port = u.port
    except ValueError:
        return f"proxy {mask(url)!r} has an invalid port (format: http://user:password@host:port)"
    if u.scheme.lower() not in SCHEMES:
        return f"proxy {mask(url)!r} must start with one of: {', '.join(s + '://' for s in SCHEMES)}"
    if not u.hostname:
        return f"proxy {mask(url)!r} has no host name"
    if port is None:
        return f"proxy {mask(url)!r} needs a port, e.g. http://host:8080"
    return ""


def mask(url: str) -> str:
    """Hide the password for logs and messages (a user name alone, which may be a token, is hidden too)."""
    url = url or ""
    if "://" not in url or "@" not in url:
        return url
    scheme, rest = url.split("://", 1)
    at = rest.rfind("@")
    userinfo, hostpart = rest[:at], rest[at + 1:]
    user, sep, _ = userinfo.partition(":")
    return f"{scheme}://{user + ':***' if sep else '***'}@{hostpart}"


def split_entries(text: str) -> list[str]:
    """Several proxies in one string, separated by spaces or new lines (not commas: passwords may have them)."""
    return [x for x in re.split(r"\s+", text or "") if x and not x.startswith("#")]


def read_proxy_file(path: str | Path) -> list[str]:
    from .config import ConfigError, read_text_any

    p = Path(path)
    if not p.is_file():
        raise ConfigError(f"The proxy file {p} does not exist.")
    out = []
    for line in read_text_any(p).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def proxy_list(proxy: str = "", proxies: list[str] | None = None, file_entries: list[str] | None = None) -> list[str]:
    """All configured proxies, normalized and de-duplicated, in order."""
    seen, out = set(), []
    for raw in split_entries(proxy) + list(proxies or []) + list(file_entries or []):
        url = normalize(str(raw))
        if url and url not in seen:
            seen.add(url)
            out.append(url)
    return out


def resolve(s, base_dir: Path) -> None:
    """Collect proxy, proxies and proxy_file into s.proxies (normalized); s.proxy becomes the first one."""
    entries: list[str] = []
    if s.proxy_file:
        f = Path(s.proxy_file)
        entries = read_proxy_file(f if f.is_absolute() else Path(base_dir) / f)
    s.proxies = proxy_list(s.proxy, s.proxies, entries)
    s.proxy = s.proxies[0] if s.proxies else ""


# ---- proxy pool for parallel workers ------------------------------------------------------------
# Rotating ("backconnect") services hand out a new IP per connection from ONE address.
ROTATING_HOSTS = ("p.webshare.io", "gate.smartproxy.com", "gate.decodo.com", "pr.oxylabs.io",
                  "brd.superproxy.io", "geo.iproyal.com", "rotating.proxyempire.io", "proxy.packetstream.io")


def looks_rotating(url: str) -> bool:
    from urllib.parse import unquote

    try:
        u = urlsplit(url)
    except ValueError:
        return False
    return "-rotate" in unquote(u.username or "").lower() or (u.hostname or "").lower() in ROTATING_HOSTS


BENCH_BLOCKED_SECONDS = 600  # a blocked proxy rests 10 min (doubling, max 1 h) while others work
BENCH_DEAD_SECONDS = 120  # a proxy that didn't connect rests 2 min; 3 strikes and it's out for this run
MAX_BENCH_SECONDS = 3600


class Slot:
    """One way out to YouTube: a proxy, or the direct connection when no proxy is configured."""

    def __init__(self, url: str, rotating: bool, capacity: int):
        import collections

        self.url = url
        self.rotating = rotating
        self.capacity = max(1, capacity)
        self.leases = 0
        self.benched_until = 0.0
        self.blocks = 0
        self.dead = 0
        self.retired = False
        self.starts: collections.deque[float] = collections.deque()  # fetch start times (hourly budget)

    @property
    def label(self) -> str:
        return f"proxy {mask(self.url)}" if self.url else "the direct connection"


class ProxyPool:
    """Hands slots to workers, benches blocked/dead proxies, and runs the shared back-off rounds when
    nothing is usable. Thread-safe. With one direct slot and one worker this reproduces the classic
    'wait 60 s, 180 s, 420 s, then stop' behaviour."""

    def __init__(self, urls: list[str], *, per_proxy: int = 1, direct_capacity: int = 1,
                 rotating: str | bool = "auto", clock=None):
        import threading
        import time

        self.clock = clock or time.monotonic
        self.cond = threading.Condition()
        if urls:
            def is_rot(u: str) -> bool:
                return looks_rotating(u) if rotating == "auto" else bool(rotating)

            self.slots = [Slot(u, is_rot(u), per_proxy) for u in urls]
        else:
            self.slots = [Slot("", False, direct_capacity)]
        self.round = 0
        self.backing_off = False
        self.stopped = ""  # "blocked" / "dead" once the pool gives up

    # -- leasing ---------------------------------------------------------------------------------------
    def _free(self, now: float) -> list[Slot]:
        return [s for s in self.slots if not s.retired and s.leases < s.capacity and s.benched_until <= now]

    def try_lease(self, prefer: Slot | None = None) -> Slot | None:
        with self.cond:
            free = self._free(self.clock())
            if not free or self.stopped:
                return None
            pick = prefer if prefer in free else min(free, key=lambda s: (s.leases, s.blocks + s.dead,
                                                                         self.slots.index(s)))
            pick.leases += 1
            return pick

    def release(self, slot: Slot) -> None:
        with self.cond:
            slot.leases = max(0, slot.leases - 1)
            self.cond.notify_all()

    # -- health ----------------------------------------------------------------------------------------
    def ok(self, slot: Slot) -> None:
        with self.cond:
            slot.blocks = slot.dead = 0
            self.round = 0

    def trouble(self, slot: Slot, dead: bool) -> None:
        with self.cond:
            if dead:
                slot.dead += 1
                rest = BENCH_DEAD_SECONDS * 2 ** (slot.dead - 1)
                if slot.url and slot.dead >= 3:
                    slot.retired = True
            else:
                slot.blocks += 1
                rest = BENCH_BLOCKED_SECONDS * 2 ** (slot.blocks - 1)
            slot.benched_until = self.clock() + min(rest, MAX_BENCH_SECONDS)
            self.cond.notify_all()

    def total_capacity(self) -> int:
        """How many workers can be busy at once (more would only wait for a free slot)."""
        with self.cond:
            return sum(s.capacity for s in self.slots if not s.retired)

    def usable_count(self) -> int:
        with self.cond:
            return sum(1 for s in self.slots if not s.retired)

    # -- waiting for a slot ------------------------------------------------------------------------
    def acquire(self, *, prefer: Slot | None, backoff: list[int], max_rounds: int, wait, stopping) -> Slot | None:
        """A slot to use, waiting if needed. `wait(seconds)` sleeps (and returns early on Stop);
        `stopping()` says Stop was pressed. Returns None when the run should end."""
        while True:
            if stopping():
                return None
            slot = self.try_lease(prefer)
            if slot is not None:
                return slot
            with self.cond:
                if self.stopped:
                    return None
                live = [s for s in self.slots if not s.retired]
                if not live:
                    self.stopped = "dead"
                    self.cond.notify_all()
                    return None
                now = self.clock()
                busy_but_fine = any(s.benched_until <= now for s in live)  # all leased by other workers
                if busy_but_fine or self.backing_off:
                    self.cond.wait(0.2)
                    continue
                r = self.round
                if r >= len(backoff) or r + 1 >= max_rounds:
                    self.stopped = "blocked"
                    self.cond.notify_all()
                    return None
                self.round += 1
                self.backing_off = True
            try:
                import logging

                logging.getLogger("yt_transcripts").warning(
                    "YouTube is rate-limiting %s. Waiting %d s before retrying...",
                    "every proxy" if len(self.slots) > 1 else "us", backoff[r])
                wait(backoff[r])
            finally:
                with self.cond:
                    self.backing_off = False
                    benched = [s for s in self.slots if not s.retired and s.benched_until > self.clock()]
                    if benched:  # give the one that has rested longest another go
                        min(benched, key=lambda s: s.benched_until).benched_until = 0.0
                    self.cond.notify_all()

    # -- hourly budget -------------------------------------------------------------------------------
    def budget_wait_seconds(self, starts, per_hour: int) -> float:
        """How long to wait before the next fetch to stay under per_hour fetches in any 60 minutes
        (0 = go now, and the fetch is recorded). `starts` is the slot's history - or, for a rotating
        service where every connection has its own IP, the worker's own history."""
        if per_hour <= 0:
            return 0.0
        with self.cond:
            now = self.clock()
            while starts and now - starts[0] >= 3600:
                starts.popleft()
            if len(starts) >= per_hour:
                return starts[0] + 3600 - now
            starts.append(now)
            return 0.0
