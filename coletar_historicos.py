"""Export full 2021–2026 historical incident series for core Statuspage providers."""
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from statuspage import fetch_history_months, parse_issue_date, parse_month_key

SOURCES = {
    "GitHub": "https://www.githubstatus.com",
    "Discord": "https://discordstatus.com",
    "Jira Software": "https://jira-software.status.atlassian.com",
}
START, END = date(2021, 1, 1), date(2026, 11, 18)
KEYWORDS = re.compile(
    r"\b(?:ddos|dos attack|denial.of.service|malicious(?:ly)?|attack(?:s|er|ers|ed)?|ransomware|botnet|cyberattack|cyber.attack|unauthori[sz]ed)\b",
    re.I,
)
ROOT = Path(__file__).resolve().parent


def fetch(job):
    provider, site, page = job
    url = f"{site}/history?page={page}"
    try:
        url, months = fetch_history_months(site, page, timeout=12, retries=1)
        return provider, site, url, months, None
    except Exception as error:
        return provider, site, url, [], type(error).__name__


def main():
    jobs = [(provider, site, page) for provider, site in SOURCES.items() for page in range(1, 25)]
    months_by_provider = {provider: {} for provider in SOURCES}
    issues = {}
    missing_dates = Counter()
    errors = []
    with ThreadPoolExecutor(max_workers=9) as pool:
        for provider, site, url, months, error in pool.map(fetch, jobs):
            if error:
                errors.append([provider, url, error])
            for month in months:
                year, number = parse_month_key(month)
                if (year, number) < (2021, 1) or (year, number) > (2026, 11):
                    continue
                months_by_provider[provider][f"{year}-{number:02}"] = url
                for issue in month["incidents"]:
                    parsed = parse_issue_date(issue, year, number)
                    if not parsed:
                        missing_dates[provider] += 1
                        continue
                    displayed_date, _ = parsed
                    if START <= displayed_date <= END:
                        issue_url = f"{site}/incidents/{issue['code']}"
                        matched = bool(KEYWORDS.search(issue["name"] + " " + (issue["message"] or "")))
                        issues[issue_url] = [provider, str(displayed_date), issue["impact"], issue["name"], issue_url, matched]
    data = {"months": months_by_provider, "errors": errors, "missing_dates": missing_dates, "records": sorted(issues.values())}
    (ROOT / "series-historicas.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
