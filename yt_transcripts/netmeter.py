"""Count the data that goes through your proxies - and stop at a limit you set.

Every proxied connection goes through a tiny relay on this PC (127.0.0.1, one per proxy). The relay
opens the real connection to the proxy, so yt-dlp, youtube-transcript-api and the API search never see
the proxy password, and it counts every byte in both directions - which is what proxy services bill.
It works the same for HTTP, HTTPS and SOCKS proxies, and for rotating services: each new connection
from the tool becomes a new connection to the proxy (so a new IP), exactly as before.

    with netmeter.Session(settings) as session:      # one per run
        url = netmeter.route(proxy_url)               # what to give the downloaders instead
        ...
    # the bytes are added to output/proxy_usage.json (per month, per proxy) when the session ends

Limits: `proxy_limit_run_mb` (per run) and `proxy_limit_month_mb` (per calendar month, counted across
runs). When a limit is reached no new video is started; connections already open may finish (a small
overrun), and anything more than 10% (at least 2 MB) over the limit is cut off.
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import logging
import select
import socket
import threading
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

log = logging.getLogger("yt_transcripts")

MB = 1_000_000  # proxy services count in decimal units
GB = 1_000_000_000
HEAD_LIMIT = 65536
CONNECT_TIMEOUT = 30
IDLE_TIMEOUT = 300
USAGE_FILE = "proxy_usage.json"
KEEP_RUNS = 200


def fmt_bytes(n: float) -> str:
    if n >= GB:
        return f"{n / GB:.2f} GB"
    if n >= 10 * MB:
        return f"{n / MB:.0f} MB"
    if n >= MB:
        return f"{n / MB:.1f} MB"
    return f"{n / 1000:.0f} KB"


def proxy_key(url: str) -> str:
    """host:port - how a proxy is named in the usage file (never with its password)."""
    try:
        u = urlsplit(url)
        return f"{u.hostname}:{u.port}" if u.hostname else "?"
    except ValueError:
        return "?"


# ---- counting ---------------------------------------------------------------------------------
class Meter:
    """Thread-safe byte counter with an optional limit."""

    def __init__(self, limit_bytes: int = 0):
        self.lock = threading.Lock()
        self.up = 0
        self.down = 0
        self.by_proxy: dict[str, int] = {}
        self.limit = max(0, int(limit_bytes))
        self.exhausted = False  # a monthly limit that was already used up before this run
        self.refused = 0

    def add(self, key: str, up: int = 0, down: int = 0) -> None:
        if not (up or down):
            return
        with self.lock:
            self.up += up
            self.down += down
            self.by_proxy[key] = self.by_proxy.get(key, 0) + up + down

    @property
    def total(self) -> int:
        with self.lock:
            return self.up + self.down

    def over_limit(self) -> bool:
        return self.exhausted or (bool(self.limit) and self.total >= self.limit)

    def far_over_limit(self) -> bool:
        return self.exhausted or (bool(self.limit) and self.total >= self.limit + max(self.limit // 10, 2 * MB))


class UpstreamError(Exception):
    def __init__(self, status: int, reason: str):
        super().__init__(f"{status} {reason}")
        self.status, self.reason = status, reason


def _read_head(sock: socket.socket) -> tuple[bytes, bytes]:
    """Read up to the end of an HTTP head. Returns (head, bytes already read past it)."""
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            break
        buf += chunk
        if len(buf) > HEAD_LIMIT:
            raise UpstreamError(431, "request head too large")
    head, sep, rest = buf.partition(b"\r\n\r\n")
    return (head + sep, rest) if sep else (buf, b"")


class Relay:
    """Listens on 127.0.0.1 and forwards every connection through one upstream proxy, counting bytes.

    It only serves this run: clients must send the relay's own one-time password (part of its URL), so
    other programs on the PC can't use your paid proxy through it."""

    def __init__(self, upstream: str, meter: Meter):
        import secrets

        self.upstream = upstream
        self.key = proxy_key(upstream)
        self.meter = meter
        u = urlsplit(upstream)
        self.scheme = (u.scheme or "http").lower()
        self.host, self.port = u.hostname or "", u.port or (1080 if self.scheme.startswith("socks") else 8080)
        self.user = unquote(u.username) if u.username else None
        self.password = unquote(u.password) if u.password else None
        self._token = secrets.token_hex(12)
        self._expect = "Basic " + base64.b64encode(f"ytt:{self._token}".encode()).decode()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):  # Windows: no other program may bind the same port
            self._server.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        self._server.bind(("127.0.0.1", 0))
        self._server.listen(128)
        self.url = f"http://ytt:{self._token}@127.0.0.1:{self._server.getsockname()[1]}"
        self._open: set[socket.socket] = set()
        self._lock = threading.Lock()
        self._closed = False
        threading.Thread(target=self._accept_loop, name=f"relay {self.key}", daemon=True).start()

    # -- lifecycle --
    def close(self) -> None:
        self._closed = True
        try:
            self._server.close()
        except OSError:
            pass
        with self._lock:
            socks_ = list(self._open)
            self._open.clear()
        for s in socks_:
            _close(s)

    def _track(self, *socks_: socket.socket) -> None:
        with self._lock:
            self._open.update(socks_)

    def _untrack(self, *socks_: socket.socket) -> None:
        with self._lock:
            for s in socks_:
                self._open.discard(s)

    def _accept_loop(self) -> None:
        while not self._closed:
            try:
                client, _ = self._server.accept()
            except OSError:
                return
            threading.Thread(target=self._handle, args=(client,), daemon=True).start()

    # -- one connection --
    def _handle(self, client: socket.socket) -> None:
        upstream = None
        self._track(client)
        try:
            client.settimeout(CONNECT_TIMEOUT)
            head, extra = _read_head(client)
            if not head:
                return
            lines = head.decode("latin-1").split("\r\n")
            parts = lines[0].split()
            if len(parts) < 3:
                _reply(client, 400, "Bad Request")
                return
            method, target = parts[0].upper(), parts[1]
            auth = next((ln.split(":", 1)[1].strip() for ln in lines[1:]
                         if ln.lower().startswith("proxy-authorization:")), "")
            if auth != self._expect:
                _reply(client, 407, "Proxy Authentication Required")
                return
            # the run stops starting new videos at the limit; connections of a video already running may
            # still open (so its data isn't wasted) - only far over the limit is everything refused
            if self.meter.far_over_limit():
                self.meter.refused += 1
                _reply(client, 403, "Proxy data limit reached")
                return
            if method == "CONNECT":
                host, _, port = target.rpartition(":")
                upstream, early = self._open_tunnel(host.strip("[]"), int(port or 443))
                self._track(upstream)
                client.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
                if early:
                    client.sendall(early)
                if extra:  # client spoke before our 200 (unusual): pass it on
                    upstream.sendall(extra)
                    self.meter.add(self.key, up=len(extra))
            else:
                upstream = self._open_plain(method, target, lines, extra)
                self._track(upstream)
            self._pump(client, upstream)
        except UpstreamError as e:
            _reply(client, e.status if 400 <= e.status < 600 else 502, e.reason)
        except Exception as e:  # noqa: BLE001 - never let one connection kill the relay thread silently
            log.debug("relay %s: %s", self.key, e)
            _reply(client, 502, "Could not connect through the proxy")
        finally:
            for s in (client, upstream):
                if s is not None:
                    self._untrack(s)
                    _close(s)

    def _connect_proxy(self) -> socket.socket:
        sock = socket.create_connection((self.host, self.port), timeout=CONNECT_TIMEOUT)
        if self.scheme == "https":
            import ssl

            sock = ssl.create_default_context().wrap_socket(sock, server_hostname=self.host)
        return sock

    def _auth_header(self) -> bytes:
        if self.user is None:
            return b""
        token = base64.b64encode(f"{self.user}:{self.password or ''}".encode()).decode()
        return f"Proxy-Authorization: Basic {token}\r\n".encode()

    def _open_tunnel(self, host: str, port: int) -> tuple[socket.socket, bytes]:
        if self.scheme.startswith("socks"):
            return self._open_socks(host, port), b""
        sock = self._connect_proxy()
        try:
            hp = f"[{host}]:{port}" if ":" in host else f"{host}:{port}"  # IPv6 addresses need brackets
            req = f"CONNECT {hp} HTTP/1.1\r\nHost: {hp}\r\n".encode() + self._auth_header() + b"\r\n"
            sock.sendall(req)
            self.meter.add(self.key, up=len(req))
            head, early = _read_head(sock)
            self.meter.add(self.key, down=len(head) + len(early))
            status_line = head.split(b"\r\n", 1)[0].decode("latin-1", "replace")
            bits = status_line.split(None, 2)
            status = int(bits[1]) if len(bits) > 1 and bits[1].isdigit() else 502
            if status != 200:
                raise UpstreamError(status, bits[2] if len(bits) > 2 else "proxy refused the connection")
            return sock, early
        except BaseException:
            _close(sock)
            raise

    def _open_socks(self, host: str, port: int) -> socket.socket:
        try:
            import socks  # PySocks, installed with requests[socks]
        except ImportError:
            raise UpstreamError(502, "SOCKS proxies need PySocks - run update.bat") from None

        kind = socks.SOCKS4 if self.scheme.startswith("socks4") else socks.SOCKS5
        s = socks.socksocket()
        s.set_proxy(kind, self.host, self.port, rdns=self.scheme in ("socks5h", "socks4a"),
                    username=self.user, password=self.password)
        s.settimeout(CONNECT_TIMEOUT)
        try:
            s.connect((host, port))
        except BaseException as e:
            _close(s)
            raise UpstreamError(502, f"SOCKS proxy refused the connection ({e})") from None
        self.meter.add(self.key, up=10 + len(host), down=10)  # the small SOCKS handshake
        return s

    def _open_plain(self, method: str, target: str, lines: list[str], extra: bytes) -> socket.socket:
        """A plain http:// request (YouTube uses https, so this is rare). One request per connection
        ("Connection: close"), so a second request can never go out without the proxy's password."""
        drop = ("proxy-authorization:", "proxy-connection:", "connection:", "keep-alive:")
        keep = [ln for ln in lines[1:] if ln and not ln.lower().startswith(drop)] + ["Connection: close"]
        version = lines[0].split()[-1]
        if self.scheme.startswith("socks"):
            u = urlsplit(target)
            sock = self._open_socks(u.hostname or "", u.port or 80)
            path = (u.path or "/") + (f"?{u.query}" if u.query else "")
            out = (f"{method} {path} {version}\r\n".encode("latin-1")
                   + "".join(f"{ln}\r\n" for ln in keep).encode("latin-1") + b"\r\n" + extra)
        else:
            sock = self._connect_proxy()
            out = (f"{method} {target} {version}\r\n".encode("latin-1")
                   + "".join(f"{ln}\r\n" for ln in keep).encode("latin-1") + self._auth_header() + b"\r\n" + extra)
        sock.sendall(out)
        self.meter.add(self.key, up=len(out))
        return sock

    def _pump(self, client: socket.socket, upstream: socket.socket) -> None:
        client.settimeout(None)
        upstream.settimeout(None)
        peers = {client: upstream, upstream: client}
        reading = [client, upstream]  # a side that finished sending is half-closed, the other keeps going
        last = time.monotonic()
        while reading:
            if self.meter.far_over_limit():
                log.debug("relay %s: cut off - far over the data limit", self.key)
                return
            pending = [s for s in reading if hasattr(s, "pending") and s.pending()]
            if pending:
                ready = pending
            else:
                try:
                    ready, _, _ = select.select(reading, [], [], 1.0)
                except (OSError, ValueError):
                    return
            if not ready:
                if time.monotonic() - last > IDLE_TIMEOUT:
                    return
                continue
            last = time.monotonic()
            for s in ready:
                try:
                    data = s.recv(65536)
                except (BlockingIOError, InterruptedError):
                    continue
                except OSError as e:
                    if type(e).__name__ in ("SSLWantReadError", "SSLWantWriteError"):
                        continue  # an HTTPS proxy's TLS layer needs more bytes first
                    return
                if not data:
                    reading.remove(s)
                    try:
                        peers[s].shutdown(socket.SHUT_WR)  # pass the end-of-data on
                    except OSError:
                        return
                    continue
                # count first: once the bytes are passed on, the run may already be reading the total
                if s is client:
                    self.meter.add(self.key, up=len(data))
                else:
                    self.meter.add(self.key, down=len(data))
                try:
                    peers[s].sendall(data)
                except OSError:
                    return


def _reply(sock: socket.socket, status: int, reason: str) -> None:
    reason = reason.replace("\r", " ").replace("\n", " ")[:200]
    try:
        sock.sendall(f"HTTP/1.1 {status} {reason}\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".encode(
            "latin-1", "replace"))
    except OSError:
        pass


def _close(sock: socket.socket) -> None:
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    try:
        sock.close()
    except OSError:
        pass


# ---- usage book (output/proxy_usage.json) --------------------------------------------------------
def month_key(now: dt.datetime | None = None) -> str:
    return (now or dt.datetime.now()).strftime("%Y-%m")


class UsageUnreadable(OSError):
    """proxy_usage.json exists but can't be read right now (locked by a sync tool/antivirus) - never
    overwrite it then, or the history would be lost."""


def _valid_usage(data) -> dict | None:
    if not isinstance(data, dict):
        return None
    months, runs = data.get("months", {}), data.get("runs", [])
    if not isinstance(months, dict) or not isinstance(runs, list):
        return None
    clean = {}
    for k, v in months.items():
        if isinstance(v, dict):
            try:
                v["bytes"] = int(v.get("bytes", 0))
                v["videos"] = int(v.get("videos", 0))
            except (TypeError, ValueError):
                return None
            if not isinstance(v.get("proxies", {}), dict):
                v["proxies"] = {}
            clean[str(k)] = v
    data["months"] = clean
    data["runs"] = [r for r in runs if isinstance(r, dict)]
    return data


def load_usage(out_dir: Path, attempts: int = 5) -> dict:
    """The usage book. A missing file is an empty book; a damaged one is set aside (renamed) and a new
    one started; a file that can't be read right now raises UsageUnreadable after a few retries."""
    p = Path(out_dir) / USAGE_FILE
    for i in range(attempts):
        try:
            text = p.read_text(encoding="utf-8")
            break
        except FileNotFoundError:
            return {"months": {}, "runs": []}
        except OSError as e:
            if i == attempts - 1:
                raise UsageUnreadable(f"{p} can't be read ({e})") from e
            time.sleep(0.2 * (i + 1))
    try:
        data = _valid_usage(json.loads(text))
    except ValueError:
        data = None
    if data is None:
        bad = p.with_name(f"proxy_usage.damaged-{dt.datetime.now():%Y%m%d-%H%M%S}.json")
        try:
            p.replace(bad)
            log.warning("%s was damaged - kept it as %s and started a new one.", p.name, bad.name)
        except OSError as e:
            raise UsageUnreadable(f"{p} is damaged and can't be moved aside ({e})") from e
        return {"months": {}, "runs": []}
    return data


def month_used(out_dir: Path, month: str | None = None) -> int:
    rec = load_usage(out_dir)["months"].get(month or month_key(), {})
    return int(rec.get("bytes", 0)) if isinstance(rec, dict) else 0


class _BookLock:
    """Only one program at a time updates proxy_usage.json (a scheduled run and the window may overlap)."""

    def __init__(self, out_dir: Path, timeout: float = 10.0):
        self.path = Path(out_dir) / (USAGE_FILE + ".lock")
        self.timeout = timeout
        self.fd = None

    def __enter__(self):
        import os

        self.path.parent.mkdir(parents=True, exist_ok=True)
        end = time.monotonic() + self.timeout
        while True:
            try:
                self.fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                try:  # a lock left behind by a crashed program
                    if time.time() - self.path.stat().st_mtime > 60:
                        self.path.unlink()
                        continue
                except OSError:
                    pass
                if time.monotonic() > end:
                    raise UsageUnreadable(f"{self.path.name} is held by another program") from None
                time.sleep(0.05)

    def __exit__(self, *exc):
        import os

        try:
            os.close(self.fd)
        finally:
            try:
                self.path.unlink()
            except OSError:
                pass


def _save_usage(out_dir: Path, data: dict) -> None:
    import os

    from .utils import replace_file

    p = Path(out_dir) / USAGE_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(f"{p.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(json.dumps(data, indent=1), encoding="utf-8")
    try:
        replace_file(tmp, p)
    except OSError:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise


# ---- one run ------------------------------------------------------------------------------------
_active: "Session | None" = None
_active_lock = threading.Lock()


def active() -> "Session | None":
    return _active


def route(proxy_url: str) -> str:
    """The URL the downloaders should use for this proxy: its counting relay while a session is
    running, otherwise the proxy itself. "" (direct connection) stays ""."""
    sess = _active
    if not proxy_url or sess is None or not sess.enabled:
        return proxy_url
    return sess.relay_url(proxy_url)


class Session:
    """Counting (and the data limits) for one run. Use as a context manager."""

    def __init__(self, s, label: str = "run"):
        self.s = s
        self.out_dir = Path(s.output_dir)
        self.enabled = bool(getattr(s, "proxy_meter", True))
        self.label = label
        run_mb = float(getattr(s, "proxy_limit_run_mb", 0) or 0)
        month_mb = float(getattr(s, "proxy_limit_month_mb", 0) or 0)
        self.month = month_key()
        self.can_save = self.enabled
        self.month_before = 0
        if self.enabled:
            try:
                self.month_before = month_used(self.out_dir, self.month)
            except UsageUnreadable as e:
                self.can_save = False  # don't overwrite a history we couldn't read
                log.warning("Proxy data history not available (%s) - this run's data is counted but not "
                            "saved%s.", e, ", and the monthly limit can't be checked" if month_mb > 0 else "")
        limits = []
        if run_mb > 0:
            limits.append(int(run_mb * MB))
        if month_mb > 0 and self.can_save:
            limits.append(max(0, int(month_mb * MB) - self.month_before))
        self.limit_reason = ""
        if limits:
            self.limit_reason = ("this month's" if month_mb > 0 and limits[-1] == min(limits) else "this run's")
        self.meter = Meter(min(limits) if limits else 0)
        self.meter.exhausted = bool(limits) and min(limits) == 0  # nothing left: refuse at once
        self.relays: dict[str, Relay] = {}
        self.closed = False
        self.videos = 0
        self.download_base: int | None = None  # bytes counted before downloads started (search etc.)
        self._saved_bytes = 0
        self._saved_videos = 0
        self._saved_by: dict[str, int] = {}
        self._lock = threading.Lock()
        self._save_lock = threading.Lock()
        self.started = dt.datetime.now()
        self._prev = None

    # -- context --
    def __enter__(self) -> "Session":
        global _active
        with _active_lock:
            self._prev = _active
            _active = self
        return self

    def __exit__(self, *exc) -> None:
        global _active
        with _active_lock:  # first stop handing out relays, then close them
            if _active is self:
                _active = self._prev
        self.close()

    def close(self) -> None:
        with self._lock:
            self.closed = True
            relays = list(self.relays.values())
            self.relays.clear()
        for r in relays:
            r.close()
        self.save()

    # -- routing --
    def relay_url(self, proxy_url: str) -> str:
        with self._lock:
            if self.closed:
                return proxy_url  # the run is over (a straggler): go direct to the proxy, uncounted
            r = self.relays.get(proxy_url)
            if r is None:
                r = self.relays[proxy_url] = Relay(proxy_url, self.meter)
                self._ever_relayed = True
            return r.url

    @property
    def used_proxies(self) -> bool:
        return bool(self.relays) or getattr(self, "_ever_relayed", False)

    # -- limits --
    def limit_reached(self) -> bool:
        return self.enabled and self.meter.over_limit()

    def limit_message(self) -> str:
        if self.meter.exhausted:
            return (f"this month's proxy data limit is used up ({fmt_bytes(self.month_before)} of "
                    f"{self.s.proxy_limit_month_mb:g} MB) - raise proxy_limit_month_mb or wait for next month")
        return (f"{self.limit_reason} proxy data limit reached ({fmt_bytes(self.meter.total)} used this run"
                + (f", {fmt_bytes(self.month_before + self.meter.total)} this month" if self.month_before else "")
                + ")")

    # -- reporting --
    def downloads_starting(self) -> None:
        """Called when transcript downloads begin, so 'per video' leaves out the search traffic."""
        if self.download_base is None:
            self.download_base = self.meter.total

    def count_video(self) -> None:
        with self._lock:
            self.videos += 1

    def per_video(self) -> float | None:
        if not self.videos:
            return None
        return (self.meter.total - (self.download_base or 0)) / self.videos

    def cost(self, nbytes: float) -> float | None:
        price = float(getattr(self.s, "proxy_price_per_gb", 0) or 0)
        return nbytes / GB * price if price > 0 else None

    def summary(self) -> str:
        total = self.meter.total
        if not self.enabled or not (total or self.used_proxies):
            return ""
        bits = [f"Proxy data this run: {fmt_bytes(total)}"]
        pv = self.per_video()
        if pv:
            bits.append(f"about {fmt_bytes(pv)} per video")
        bits.append(f"{fmt_bytes(self.month_before + total)} this month")
        c = self.cost(total)
        if c is not None:
            bits.append(f"~${c:.2f} this run")
        return ", ".join(bits)

    def save(self) -> None:
        """Add what was counted since the last save to output/proxy_usage.json."""
        if not self.enabled or not self.can_save:
            return
        with self._save_lock:
            with self.meter.lock:
                total = self.meter.up + self.meter.down
                by = dict(self.meter.by_proxy)
            videos = self.videos
            d_bytes = total - self._saved_bytes
            d_videos = videos - self._saved_videos
            d_by = {k: v - self._saved_by.get(k, 0) for k, v in by.items() if v - self._saved_by.get(k, 0)}
            if d_bytes <= 0 and d_videos <= 0:
                return
            try:
                with _BookLock(self.out_dir):
                    data = load_usage(self.out_dir)
                    month = month_key()  # a run that goes past midnight at the month's end books the rest anew
                    m = data["months"].setdefault(month, {"bytes": 0, "videos": 0, "proxies": {}})
                    m["bytes"] = int(m.get("bytes", 0)) + d_bytes
                    m["videos"] = int(m.get("videos", 0)) + d_videos
                    px = m.setdefault("proxies", {})
                    for k, v in d_by.items():
                        px[k] = int(px.get(k, 0)) + v
                    runs = data["runs"]
                    stamp = self.started.isoformat(timespec="seconds")
                    entry = next((r for r in reversed(runs) if r.get("started") == stamp), None)
                    if entry is None:
                        entry = {"started": stamp, "what": self.label, "bytes": 0, "videos": 0}
                        runs.append(entry)
                    entry["bytes"] = total
                    entry["videos"] = videos
                    data["runs"] = runs[-KEEP_RUNS:]
                    _save_usage(self.out_dir, data)
            except OSError as e:  # includes UsageUnreadable: try again at the next save
                log.debug("could not save %s: %s", USAGE_FILE, e)
                return
            self._saved_bytes, self._saved_videos, self._saved_by = total, videos, by


def usage_report(out_dir: Path, s=None, months: int = 6) -> list[str]:
    """Plain lines for `yt.py status` / the window: data through proxies per month."""
    try:
        data = load_usage(out_dir)
    except UsageUnreadable as e:
        return [f"Data through proxies: {e}"]
    if not data["months"]:
        return []
    price = float(getattr(s, "proxy_price_per_gb", 0) or 0) if s is not None else 0
    month_limit = float(getattr(s, "proxy_limit_month_mb", 0) or 0) if s is not None else 0
    lines = ["Data through proxies (counted on this PC; your provider's numbers may differ a little):"]
    for m in sorted(data["months"], reverse=True)[:months]:
        rec = data["months"][m]
        b, n = int(rec.get("bytes", 0)), int(rec.get("videos", 0))
        line = f"  {m}: {fmt_bytes(b)}"
        if n:
            line += f" for {n} videos ({fmt_bytes(b / n)} each)"
        if price:
            line += f", ~${b / GB * price:.2f}"
        if month_limit and m == month_key():
            line += f"  - limit {month_limit:g} MB, {max(0.0, month_limit - b / MB):.0f} MB left"
        lines.append(line)
    return lines
