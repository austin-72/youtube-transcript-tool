"""The counting relay: forwards through HTTP and SOCKS proxies, counts bytes, enforces limits."""

import base64
import json
import socket
import struct
import threading

import pytest

from yt_transcripts import netmeter
from yt_transcripts.config import build_settings


def _serve(handler):
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(16)

    def loop():
        while True:
            try:
                c, _ = srv.accept()
            except OSError:
                return
            threading.Thread(target=handler, args=(c,), daemon=True).start()
    threading.Thread(target=loop, daemon=True).start()
    return srv, srv.getsockname()[1]


def _pipe(a, b):
    """Copy both ways; an end-of-data from one side is passed on as a half-close (like real proxies)."""
    def one(x, y):
        try:
            while True:
                d = x.recv(65536)
                if not d:
                    break
                y.sendall(d)
            y.shutdown(socket.SHUT_WR)
        except OSError:
            pass
    t = threading.Thread(target=one, args=(a, b), daemon=True)
    t.start()
    one(b, a)
    t.join(10)
    for s in (a, b):
        try:
            s.close()
        except OSError:
            pass


@pytest.fixture
def origin():
    """An HTTP 'website' that answers every request with a 50 kB body."""
    body = b"x" * 50_000

    def handle(c):
        buf = b""
        try:
            while True:
                while b"\r\n\r\n" not in buf:
                    d = c.recv(4096)
                    if not d:
                        return
                    buf += d
                _, _, buf = buf.partition(b"\r\n\r\n")
                c.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n" % len(body) + body)
        except OSError:
            pass
        finally:
            c.close()
    srv, port = _serve(handle)
    yield port
    srv.close()


@pytest.fixture
def http_proxy():
    """A CONNECT proxy that wants user 'u' / password 'p@ss:w/rd'."""
    seen = {"auth": [], "connects": 0}
    good = "Basic " + base64.b64encode(b"u:p@ss:w/rd").decode()

    def handle(c):
        buf = b""
        while b"\r\n\r\n" not in buf:
            d = c.recv(4096)
            if not d:
                c.close()
                return
            buf += d
        head, _, rest = buf.partition(b"\r\n\r\n")
        lines = head.decode().split("\r\n")
        auth = next((ln.split(":", 1)[1].strip() for ln in lines if ln.lower().startswith("proxy-authorization")), "")
        seen["auth"].append(auth)
        if auth != good:
            c.sendall(b"HTTP/1.1 407 Proxy Authentication Required\r\n\r\n")
            c.close()
            return
        method, target, _ = lines[0].split()
        if method == "CONNECT":
            host, port = target.rsplit(":", 1)
            up = socket.create_connection((host, int(port)))
            seen["connects"] += 1
            c.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
        else:
            from urllib.parse import urlsplit
            u = urlsplit(target)
            up = socket.create_connection((u.hostname, u.port))
            up.sendall(f"{method} {u.path or '/'} HTTP/1.1\r\n".encode() + b"\r\n".join(
                ln.encode() for ln in lines[1:] if not ln.lower().startswith("proxy-")) + b"\r\n\r\n" + rest)
        _pipe(c, up)
    srv, port = _serve(handle)
    yield f"http://u:p%40ss%3Aw%2Frd@127.0.0.1:{port}", seen
    srv.close()


@pytest.fixture
def socks_proxy():
    """A tiny SOCKS5 server with user/password auth (u / pw)."""
    def handle(c):
        try:
            ver, n = c.recv(2)
            methods = c.recv(n)
            assert 2 in methods
            c.sendall(b"\x05\x02")
            c.recv(1)
            ul = c.recv(1)[0]
            user = c.recv(ul)
            pl = c.recv(1)[0]
            pw = c.recv(pl)
            if (user, pw) != (b"u", b"pw"):
                c.sendall(b"\x01\x01")
                c.close()
                return
            c.sendall(b"\x01\x00")
            hdr = c.recv(4)
            if hdr[3] == 3:
                ln = c.recv(1)[0]
                host = c.recv(ln).decode()
            else:
                host = socket.inet_ntoa(c.recv(4))
            port = struct.unpack(">H", c.recv(2))[0]
            up = socket.create_connection((host, port))
            c.sendall(b"\x05\x00\x00\x01" + socket.inet_aton("127.0.0.1") + struct.pack(">H", port))
            _pipe(c, up)
        except Exception:
            c.close()
    srv, port = _serve(handle)
    yield f"socks5h://u:pw@127.0.0.1:{port}"
    srv.close()


def _get_via(relay_url, port, n=1):
    """n HTTP requests to the origin through the relay, over one CONNECT tunnel (like keep-alive HTTPS)."""
    from urllib.parse import urlsplit

    u = urlsplit(relay_url)
    auth = ""
    if u.username:
        auth = "Proxy-Authorization: Basic " + base64.b64encode(f"{u.username}:{u.password}".encode()).decode() + "\r\n"
    s = socket.create_connection(("127.0.0.1", u.port), timeout=5)
    s.sendall(f"CONNECT 127.0.0.1:{port} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n{auth}\r\n".encode())
    head = b""
    while b"\r\n\r\n" not in head:
        d = s.recv(1)
        if not d:
            raise ConnectionResetError("closed")
        head += d
    status = int(head.split()[1])
    if status != 200:
        s.close()
        return status, 0
    got = 0
    for _ in range(n):
        s.sendall(b"GET / HTTP/1.1\r\nHost: x\r\n\r\n")
        buf = b""
        while b"\r\n\r\n" not in buf:
            d = s.recv(4096)
            if not d:
                raise ConnectionResetError("closed")
            buf += d
        h, _, body = buf.partition(b"\r\n\r\n")
        length = int([ln for ln in h.split(b"\r\n") if ln.lower().startswith(b"content-length")][0].split(b":")[1])
        while len(body) < length:
            d = s.recv(65536)
            if not d:
                raise ConnectionResetError("closed")
            body += d
        got += len(body)
    s.close()
    return 200, got


def _settings(tmp_path, **kw):
    return build_settings({"output_dir": str(tmp_path), **kw})


def test_relay_counts_tunnel_bytes_and_adds_the_password(tmp_path, origin, http_proxy):
    url, seen = http_proxy
    with netmeter.Session(_settings(tmp_path)) as sess:
        local = netmeter.route(url)
        assert "@127.0.0.1:" in local and "p%40ss" not in local
        # only this run may use the relay: no (or a wrong) relay password is refused
        assert _get_via(local.replace(local.split("//")[1].split("@")[0] + "@", ""), origin)[0] == 407
        assert _get_via(local.replace("ytt:", "ytt:x"), origin)[0] == 407
        status, got = _get_via(local, origin, n=3)
        assert status == 200 and got == 150_000
        total = sess.meter.total
        assert 150_000 < total < 152_000  # bodies + small heads, both directions
    assert seen["auth"] == ["Basic " + base64.b64encode(b"u:p@ss:w/rd").decode()]
    usage = json.loads((tmp_path / "proxy_usage.json").read_text())
    month = netmeter.month_key()
    assert usage["months"][month]["bytes"] == total
    assert list(usage["months"][month]["proxies"]) == [f"127.0.0.1:{url.rsplit(':', 1)[1]}"]
    assert "p@ss" not in json.dumps(usage) and "u:" not in json.dumps(usage)
    assert netmeter.route(url) == url  # no session: unchanged


def test_relay_through_socks5_and_plain_http(tmp_path, origin, socks_proxy, http_proxy):
    import requests

    with netmeter.Session(_settings(tmp_path)) as sess:
        status, got = _get_via(netmeter.route(socks_proxy), origin)
        assert status == 200 and got == 50_000
        # a plain http:// request (no CONNECT), the way requests sends one through an HTTP proxy
        local = netmeter.route(http_proxy[0])
        sess_ = requests.Session()
        sess_.trust_env = False
        r = sess_.get(f"http://127.0.0.1:{origin}/", proxies={"http": local}, timeout=5)
        assert r.status_code == 200 and len(r.content) == 50_000
        assert sess.meter.total > 100_000
        assert len(sess.meter.by_proxy) == 2


def test_wrong_password_comes_back_as_a_proxy_error(tmp_path, origin, http_proxy):
    url, _ = http_proxy
    with netmeter.Session(_settings(tmp_path)):
        status, _ = _get_via(netmeter.route(url.replace("p%40ss", "nope")), origin)
    assert status == 407


def test_run_limit_is_soft_then_hard(tmp_path, origin, http_proxy, monkeypatch):
    url, seen = http_proxy
    monkeypatch.setattr(netmeter, "MB", 10_000)  # so the 2 MB "hard" margin is 20 kB here
    with netmeter.Session(_settings(tmp_path, proxy_limit_run_mb=8)) as sess:  # 80 kB
        local = netmeter.route(url)
        assert _get_via(local, origin)[0] == 200
        assert not sess.limit_reached()
        assert _get_via(local, origin)[0] == 200  # crosses 80 kB: no NEW video would start now...
        assert sess.limit_reached()
        # ...but a video already running may still open its next connection (its data isn't wasted)
        assert sess.meter.total < sess.meter.limit + 20_000 or _get_via(local, origin)[0] == 403
        assert "this run's proxy data limit reached" in sess.limit_message()
        while not sess.meter.far_over_limit():
            _get_via(local, origin)
        assert _get_via(local, origin)[0] == 403  # far over: everything refused
    assert seen["connects"] >= 2


def test_monthly_limit_counts_earlier_runs(tmp_path, origin, http_proxy):
    url, _ = http_proxy
    s = _settings(tmp_path, proxy_limit_month_mb=0.12, proxy_price_per_gb=4.0)
    with netmeter.Session(s) as sess:
        _get_via(netmeter.route(url), origin, n=2)
        sess.count_video()
        assert "per video" in sess.summary() and "$" in sess.summary()
    with netmeter.Session(s) as sess:  # ~100 kB already used this month: 20 kB left
        assert sess.meter.limit < 25_000
        _get_via(netmeter.route(url), origin)
        assert sess.limit_reached()
    with netmeter.Session(s) as sess:  # nothing left
        assert sess.limit_reached() or _get_via(netmeter.route(url), origin)[0] == 403
        assert "used up" in sess.limit_message()
    lines = netmeter.usage_report(tmp_path, s)
    assert lines and "MB left" in lines[1] and "$" in lines[1]


def test_meter_can_be_switched_off(tmp_path, http_proxy):
    with netmeter.Session(_settings(tmp_path, proxy_meter=False)):
        assert netmeter.route(http_proxy[0]) == http_proxy[0]
    assert not (tmp_path / "proxy_usage.json").exists()


def test_far_over_limit_cuts_an_open_tunnel(tmp_path, origin, http_proxy):
    url, _ = http_proxy
    with netmeter.Session(_settings(tmp_path, proxy_limit_run_mb=0.03)) as sess:
        # one long keep-alive tunnel: 80 x 50 kB = 4 MB; the relay cuts it once it's 2 MB over the limit
        with pytest.raises((OSError, IndexError, ValueError)):
            _get_via(netmeter.route(url), origin, n=80)
        assert 2_000_000 < sess.meter.total < 2_300_000
        assert sess.limit_reached()


def test_missing_pysocks_is_a_clear_proxy_error(tmp_path, origin, monkeypatch):
    import sys

    monkeypatch.setitem(sys.modules, "socks", None)  # as if PySocks weren't installed
    with netmeter.Session(_settings(tmp_path)):
        assert _get_via(netmeter.route("socks5://127.0.0.1:9"), origin)[0] == 502


def test_dead_upstream_proxy_gives_502(tmp_path, origin):
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    port = srv.getsockname()[1]
    srv.close()  # nothing listens there now
    with netmeter.Session(_settings(tmp_path)):
        assert _get_via(netmeter.route(f"http://127.0.0.1:{port}"), origin)[0] == 502


# ---- regressions from the review -----------------------------------------------------------------------
def test_unreadable_usage_file_is_never_overwritten(tmp_path, monkeypatch):
    from pathlib import Path

    book = tmp_path / "proxy_usage.json"
    history = {"months": {"2026-01": {"bytes": 123, "videos": 1}}, "runs": [{"started": "x"}]}
    book.write_text(json.dumps(history), encoding="utf-8")
    real = Path.read_text

    def locked(self, *a, **k):
        if self.name == "proxy_usage.json":
            raise PermissionError(13, "locked by OneDrive")
        return real(self, *a, **k)
    monkeypatch.setattr(Path, "read_text", locked)
    monkeypatch.setattr(netmeter.time, "sleep", lambda x: None)
    with netmeter.Session(_settings(tmp_path, proxy_limit_month_mb=5)) as sess:
        assert not sess.can_save
        sess.meter.add("x:1", down=1000)
    monkeypatch.setattr(Path, "read_text", real)
    assert json.loads(book.read_text(encoding="utf-8")) == history  # untouched


def test_damaged_usage_file_is_set_aside(tmp_path):
    (tmp_path / "proxy_usage.json").write_text('{"months": [], "runs": {}}', encoding="utf-8")
    with netmeter.Session(_settings(tmp_path)) as sess:
        sess.meter.add("x:1", down=500)
        sess._ever_relayed = True
    assert list(tmp_path.glob("proxy_usage.damaged-*.json"))
    data = json.loads((tmp_path / "proxy_usage.json").read_text(encoding="utf-8"))
    assert data["months"][netmeter.month_key()]["bytes"] == 500


def test_two_sessions_saving_at_once_lose_nothing(tmp_path):
    sessions = [netmeter.Session(_settings(tmp_path)) for _ in range(6)]
    for i, sess in enumerate(sessions):
        sess.started = sess.started.replace(microsecond=i)  # distinct run entries

    def work(sess):
        for _ in range(20):
            sess.meter.add("x:1", down=100)
            sess.save()
    threads = [threading.Thread(target=work, args=(s_,)) for s_ in sessions]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    data = json.loads((tmp_path / "proxy_usage.json").read_text(encoding="utf-8"))
    assert data["months"][netmeter.month_key()]["bytes"] == 6 * 20 * 100
    assert not list(tmp_path.glob("*.tmp")) and not (tmp_path / "proxy_usage.json.lock").exists()


def test_ipv6_target_is_bracketed(tmp_path, http_proxy):
    url, _ = http_proxy
    relay = netmeter.Relay(url, netmeter.Meter())
    sent = []

    class FakeSock:
        def sendall(self, b):
            sent.append(b)

        def recv(self, n):
            return b"HTTP/1.1 200 OK\r\n\r\n" if not sent[1:] else b""
    relay._connect_proxy = lambda: FakeSock()
    relay._open_tunnel("2001:db8::1", 443)
    assert sent[0].startswith(b"CONNECT [2001:db8::1]:443 HTTP/1.1")
    relay.close()


def test_half_close_still_delivers_the_answer(tmp_path, http_proxy):
    """A client that sends its request and then closes its sending side still gets the whole reply."""
    body = b"y" * 300_000

    def handle(c):
        buf = b""
        while True:
            d = c.recv(4096)
            if not d:
                break
            buf += d
        c.sendall(body)
        c.close()
    srv, port = _serve(handle)
    from urllib.parse import urlsplit

    url, _ = http_proxy
    with netmeter.Session(_settings(tmp_path)):
        u = urlsplit(netmeter.route(url))
        auth = base64.b64encode(f"{u.username}:{u.password}".encode()).decode()
        s = socket.create_connection(("127.0.0.1", u.port), timeout=5)
        s.sendall(f"CONNECT 127.0.0.1:{port} HTTP/1.1\r\nProxy-Authorization: Basic {auth}\r\n\r\n".encode())
        head = b""
        while b"\r\n\r\n" not in head:
            head += s.recv(1)
        s.sendall(b"request")
        s.shutdown(socket.SHUT_WR)
        got = b""
        while True:
            d = s.recv(65536)
            if not d:
                break
            got += d
        s.close()
    srv.close()
    assert got == body


def test_route_after_session_end_goes_straight_to_the_proxy(tmp_path):
    sess = netmeter.Session(_settings(tmp_path))
    with sess:
        pass
    assert sess.relay_url("http://u:p@h:1") == "http://u:p@h:1" and not sess.relays
