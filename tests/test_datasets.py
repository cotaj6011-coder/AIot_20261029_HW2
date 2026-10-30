from pathlib import Path
import socket

import pandas as pd
import pytest

from src.datasets import MAX_BYTES, MAX_COLUMNS, MAX_ROWS, load_builtin, load_csv_url, validate_public_https_url


def public_resolver(*args, **kwargs):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]


class Response:
    def __init__(self, body=b"a,target\n1,2\n3,4\n", url="https://example.com/data.csv", content_type="text/csv", status=200):
        self.body, self.url, self.status = body, url, status
        self.headers = {"Content-Type": content_type}

    def raise_for_status(self):
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    def iter_content(self, size):
        yield self.body


class Session:
    response = Response()

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.response


def test_builtin_registry_and_feature_counts():
    human, spec = load_builtin("human_ai")
    assert spec.target in human
    assert len(human) == 10_100
    assert len([c for c in human if c != spec.target]) == 20
    startup, spec2 = load_builtin("startups")
    assert spec2.target in startup and not startup.empty


@pytest.mark.parametrize("url", [
    "http://example.com/a.csv", "https://localhost/a.csv", "https://internal/a.csv",
    "https://127.0.0.1/a.csv", "https://10.0.0.1/a.csv", "https://169.254.1.1/a.csv",
])
def test_url_rejects_unsafe_hosts(url):
    with pytest.raises(ValueError):
        validate_public_https_url(url)


def test_url_accepts_public_https(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    validate_public_https_url("https://example.com/data.csv")


def test_csv_loader_valid_and_redirect_checked(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    frame = load_csv_url("https://example.com/data.csv", session=Session)
    assert frame.shape == (2, 2)


@pytest.mark.parametrize("response", [
    Response(b"<html>oops</html>", content_type="text/html"),
    Response(b"only\n1\n2\n", content_type="text/csv"),
    Response(b"", content_type="text/csv"),
])
def test_csv_loader_rejects_bad_content(monkeypatch, response):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    Session.response = response
    with pytest.raises((ValueError, pd.errors.ParserError)):
        load_csv_url("https://example.com/data.csv", session=Session)
    Session.response = Response()


def test_csv_loader_rejects_private_redirect(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    Session.response = Response(url="https://127.0.0.1/data.csv")
    with pytest.raises(ValueError):
        load_csv_url("https://example.com/data.csv", session=Session)
    Session.response = Response()


def test_csv_loader_timeout(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    class TimeoutSession:
        @staticmethod
        def get(*args, **kwargs):
            raise TimeoutError("timeout")
    with pytest.raises(TimeoutError):
        load_csv_url("https://example.com/data.csv", session=TimeoutSession)


def test_csv_loader_rejects_oversized_payload(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    Session.response = Response(body=b"a,target\n" + b"1,2\n" * (MAX_BYTES // 4 + 1))
    with pytest.raises(ValueError, match="10 MB"):
        load_csv_url("https://example.com/data.csv", session=Session)
    Session.response = Response()


@pytest.mark.parametrize("body,expected", [
    (b"feature,target\n" + b"1,2\n" * (MAX_ROWS + 1), "100,000"),
    (
        (",".join(f"c{i}" for i in range(MAX_COLUMNS + 1)) + "\n" +
         ",".join("1" for _ in range(MAX_COLUMNS + 1)) + "\n").encode(),
        "200",
    ),
])
def test_csv_loader_rejects_row_or_column_limit(monkeypatch, body, expected):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    Session.response = Response(body=body)
    with pytest.raises(ValueError, match=expected):
        load_csv_url("https://example.com/too-large.csv", session=Session)
    Session.response = Response()


def test_csv_loader_propagates_http_failure(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", public_resolver)
    Session.response = Response(status=404)
    with pytest.raises(RuntimeError, match="404"):
        load_csv_url("https://example.com/missing.csv", session=Session)
    Session.response = Response()

