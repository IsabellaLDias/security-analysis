"""Shared utilities for fetching and parsing Statuspage incident history pages."""

import calendar
import gzip
import html
import http.client
import json
import random
import re
import time
import urllib.error
import urllib.parse
import zlib
from datetime import date

HISTORY_PROPS_RE = re.compile(r'data-react-class="HistoryIndex" data-react-props="([^"]+)')
DAY_RE = re.compile(r"data-var=['\"]date['\"]>(\d+)")
TAG_RE = re.compile(r"<[^>]*>")
MONTH_ABBR_RE = re.compile(r"([A-Za-z]{3})\b")
USER_AGENT = "security-analysis/1.0"
ACCEPT_ENCODING = "gzip, deflate"

MONTH_NUMBERS = {name: idx for idx, name in enumerate(calendar.month_name) if name}
MONTH_ABBRS = {abbr: idx for idx, abbr in enumerate(calendar.month_abbr) if abbr}

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
REDIRECT_STATUS = {301, 302, 303, 307, 308}


def _decode_body(raw_bytes: bytes, content_encoding: str | None, charset: str) -> str:
    encoding = (content_encoding or "").lower()
    if "gzip" in encoding:
        raw_bytes = gzip.decompress(raw_bytes)
    elif "deflate" in encoding:
        try:
            raw_bytes = zlib.decompress(raw_bytes)
        except zlib.error:
            raw_bytes = zlib.decompress(raw_bytes, -zlib.MAX_WBITS)
    return raw_bytes.decode(charset)


class StatuspageClient:
    """Persistent HTTP/HTTPS client with Keep-Alive, gzip, redirects, and retry backoff."""

    def __init__(self, timeout: int = 15, retries: int = 1, backoff: float = 0.25):
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self._connections: dict[tuple[str, str], http.client.HTTPConnection] = {}

    def close(self) -> None:
        for conn in self._connections.values():
            conn.close()
        self._connections.clear()

    def __enter__(self) -> "StatuspageClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def _get_connection(self, scheme: str, netloc: str) -> http.client.HTTPConnection:
        key = (scheme, netloc)
        conn = self._connections.get(key)
        if conn is None:
            cls = http.client.HTTPSConnection if scheme == "https" else http.client.HTTPConnection
            conn = cls(netloc, timeout=self.timeout)
            self._connections[key] = conn
        return conn

    def _drop_connection(self, scheme: str, netloc: str) -> None:
        conn = self._connections.pop((scheme, netloc), None)
        if conn is not None:
            conn.close()

    def _get(self, url: str, max_redirects: int = 3) -> str:
        current_url = url
        for _ in range(max_redirects + 1):
            parts = urllib.parse.urlsplit(current_url)
            path = parts.path or "/"
            if parts.query:
                path = f"{path}?{parts.query}"
            headers = {
                "User-Agent": USER_AGENT,
                "Accept-Encoding": ACCEPT_ENCODING,
                "Connection": "keep-alive",
            }
            conn = self._get_connection(parts.scheme, parts.netloc)
            try:
                conn.request("GET", path, headers=headers)
                response = conn.getresponse()
                raw_bytes = response.read()
            except Exception:
                self._drop_connection(parts.scheme, parts.netloc)
                raise

            if response.will_close:
                self._drop_connection(parts.scheme, parts.netloc)

            if response.status in REDIRECT_STATUS:
                location = response.getheader("Location")
                if not location:
                    raise urllib.error.HTTPError(
                        current_url, response.status, response.reason, response.headers, None
                    )
                current_url = urllib.parse.urljoin(current_url, location)
                continue

            if response.status >= 400:
                raise urllib.error.HTTPError(
                    current_url, response.status, response.reason, response.headers, None
                )

            charset = response.headers.get_content_charset() or "utf-8"
            return _decode_body(raw_bytes, response.getheader("Content-Encoding"), charset)

        raise urllib.error.URLError("Too many redirects")

    def fetch_history_months(self, base_url: str, page: int) -> tuple[str, list[dict]]:
        """Fetch a Statuspage history page and return its URL and parsed month entries."""
        url = f"{base_url.rstrip('/')}/history?page={page}"
        last_exc: Exception | None = None

        for attempt in range(self.retries + 1):
            try:
                body = self._get(url)
                break
            except urllib.error.HTTPError as exc:
                last_exc = exc
                if exc.code not in RETRYABLE_STATUS or attempt >= self.retries:
                    raise
            except (http.client.HTTPException, urllib.error.URLError, TimeoutError, OSError) as exc:
                last_exc = exc
                if attempt >= self.retries:
                    raise
            time.sleep(self.backoff * (2 ** attempt) + random.uniform(0, 0.1))
        else:
            assert last_exc is not None
            raise last_exc

        match = HISTORY_PROPS_RE.search(body)
        if not match:
            raise ValueError("HistoryIndex payload not found in page markup")
        months = json.loads(html.unescape(match[1]))["months"]
        return url, months


def fetch_history_months(base_url: str, page: int, timeout: int = 15, retries: int = 1) -> tuple[str, list[dict]]:
    """Fetch a single Statuspage history page using a temporary client."""
    with StatuspageClient(timeout=timeout, retries=retries) as client:
        return client.fetch_history_months(base_url, page)


def parse_month_key(month: dict) -> tuple[int, int]:
    """Return (year, month_number) for a Statuspage month entry."""
    return int(month["year"]), MONTH_NUMBERS[month["name"]]


def parse_issue_date(
    issue: dict, year: int, month_number: int, include_raw: bool = True
) -> tuple[date, str] | None:
    """Extract the displayed start date and optional clean timestamp text from an incident entry."""
    stamp = html.unescape(issue["timestamp"])
    day_match = DAY_RE.search(stamp)
    if not day_match:
        return None

    if include_raw:
        raw = TAG_RE.sub("", stamp).strip()
        prefix = raw
    else:
        raw = ""
        stripped = stamp.lstrip()
        prefix = TAG_RE.sub("", stripped).lstrip() if stripped.startswith("<") else stripped

    first_month = MONTH_ABBR_RE.match(prefix)
    actual_month = MONTH_ABBRS.get(first_month[1], month_number) if first_month else month_number

    # An incident spanning year-end can display December inside January's section.
    displayed_date = date(year - int(actual_month > month_number), actual_month, int(day_match[1]))
    return displayed_date, raw
