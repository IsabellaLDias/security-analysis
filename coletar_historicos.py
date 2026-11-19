"""Export full 2021–2026 historical incident series for core Statuspage providers."""
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from statuspage import StatuspageClient, parse_issue_date, parse_month_key

SOURCES = {
    "GitHub": "https://www.githubstatus.com",
    "Discord": "https://discordstatus.com",
    "Jira Software": "https://jira-software.status.atlassian.com",
}
START, END = date(2021, 1, 1), date(2026, 11, 18)
START_YM, END_YM = (2021, 1), (2026, 11)
MAX_PAGES = 24
KEYWORDS = re.compile(
    r"\b(?:ddos|dos attack|denial.of.service|malicious(?:ly)?|attack(?:s|er|ers|ed)?|ransomware|botnet|cyberattack|cyber.attack|unauthori[sz]ed)\b",
    re.I,
)
ROOT = Path(__file__).resolve().parent


def _matches_keywords(issue: dict) -> bool:
    if KEYWORDS.search(issue["name"]):
        return True
    message = issue.get("message")
    return bool(message and KEYWORDS.search(message))


def collect_provider(provider: str, site: str) -> tuple[str, dict[str, str], dict[str, list], int, list[list]]:
    months_map: dict[str, str] = {}
    issues: dict[str, list] = {}
    missing_dates = 0
    errors: list[list] = []
    seen_months: set[tuple[int, int]] = set()

    with StatuspageClient(timeout=12, retries=1) as client:
        for page in range(1, MAX_PAGES + 1):
            url = f"{site}/history?page={page}"
            try:
                url, months = client.fetch_history_months(site, page)
            except Exception as error:
                errors.append([provider, url, type(error).__name__])
                break

            page_months = [(month, parse_month_key(month)) for month in months]
            if not page_months or all(ym in seen_months for _, ym in page_months):
                break
            seen_months.update(ym for _, ym in page_months)

            for month, ym in page_months:
                if ym < START_YM or ym > END_YM:
                    continue
                year, number = ym
                months_map[f"{year}-{number:02}"] = url
                for issue in month["incidents"]:
                    issue_url = f"{site}/incidents/{issue['code']}"
                    if issue_url in issues:
                        continue
                    parsed = parse_issue_date(issue, year, number, include_raw=False)
                    if not parsed:
                        missing_dates += 1
                        continue
                    displayed_date, _ = parsed
                    if START <= displayed_date <= END:
                        issues[issue_url] = [
                            provider,
                            str(displayed_date),
                            issue["impact"],
                            issue["name"],
                            issue_url,
                            _matches_keywords(issue),
                        ]

            if min(ym for _, ym in page_months) < START_YM:
                break

    return provider, months_map, issues, missing_dates, errors


def main():
    months_by_provider = {provider: {} for provider in SOURCES}
    issues = {}
    missing_dates = Counter()
    errors = []
    with ThreadPoolExecutor(max_workers=len(SOURCES)) as pool:
        for provider, months_map, prov_issues, prov_missing, prov_errors in pool.map(
            lambda item: collect_provider(*item), SOURCES.items()
        ):
            months_by_provider[provider] = months_map
            issues.update(prov_issues)
            if prov_missing:
                missing_dates[provider] = prov_missing
            errors.extend(prov_errors)
    data = {"months": months_by_provider, "errors": errors, "missing_dates": missing_dates, "records": sorted(issues.values())}
    (ROOT / "series-historicas.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
