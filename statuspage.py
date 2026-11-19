"""Shared utilities for fetching and parsing Statuspage incident history pages."""

import calendar
import html
import json
import re
import urllib.error
import urllib.request
from datetime import date

HISTORY_PROPS_RE = re.compile(r'data-react-class="HistoryIndex" data-react-props="([^"]+)')
DAY_RE = re.compile(r"data-var=['\"]date['\"]>(\d+)")
TAG_RE = re.compile(r"<[^>]*>")
MONTH_ABBR_RE = re.compile(r"([A-Za-z]{3})\b")
USER_AGENT = "security-analysis/1.0"


def fetch_history_months(base_url: str, page: int, timeout: int = 15, retries: int = 1) -> tuple[str, list[dict]]:
    """Fetch a Statuspage history page and return its URL and parsed month entries."""
    url = f"{base_url.rstrip('/')}/history?page={page}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_exc: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read().decode(charset)
            break
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code < 500 or attempt >= retries:
                raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_exc = exc
            if attempt >= retries:
                raise
    else:
        assert last_exc is not None
        raise last_exc

    match = HISTORY_PROPS_RE.search(body)
    if not match:
        raise ValueError("HistoryIndex payload not found in page markup")
    months = json.loads(html.unescape(match[1]))["months"]
    return url, months


def parse_month_key(month: dict) -> tuple[int, int]:
    """Return (year, month_number) for a Statuspage month entry."""
    return int(month["year"]), list(calendar.month_name).index(month["name"])


def parse_issue_date(issue: dict, year: int, month_number: int) -> tuple[date, str] | None:
    """Extract the displayed start date and clean timestamp text from an incident entry."""
    stamp = html.unescape(issue["timestamp"])
    day_match = DAY_RE.search(stamp)
    if not day_match:
        return None

    raw = TAG_RE.sub("", stamp).strip()
    first_month = MONTH_ABBR_RE.match(raw)
    if first_month and first_month[1] in calendar.month_abbr:
        actual_month = list(calendar.month_abbr).index(first_month[1])
    else:
        actual_month = month_number

    # An incident spanning year-end can display December inside January's section.
    displayed_date = date(year - int(actual_month > month_number), actual_month, int(day_match[1]))
    return displayed_date, raw
