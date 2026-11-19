import calendar
import html
import json
import re
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

sources = {
    "GitHub": "https://www.githubstatus.com",
    "Discord": "https://discordstatus.com",
    "Jira Software": "https://jira-software.status.atlassian.com",
}
keywords = re.compile(r"\b(?:ddos|dos attack|denial.of.service|malicious(?:ly)?|attack(?:s|er|ers|ed)?|ransomware|botnet|cyberattack|cyber.attack|unauthori[sz]ed)\b", re.I)

def fetch(job):
    provider, site, page = job
    url = f"{site}/history?page={page}"
    try:
        markup = subprocess.check_output(["curl.exe", "-fsSL", "--retry", "1", "--max-time", "12", url], stderr=subprocess.DEVNULL).decode()
        match = re.search(r'data-react-class="HistoryIndex" data-react-props="([^"]+)', markup)
        return provider, site, url, json.loads(html.unescape(match[1]))["months"], None
    except Exception as error:
        return provider, site, url, [], type(error).__name__

jobs = [(provider, site, page) for provider, site in sources.items() for page in range(1, 25)]
months_by_provider = {provider: {} for provider in sources}
issues = {}
missing_dates = Counter()
errors = []
with ThreadPoolExecutor(max_workers=9) as pool:
    for provider, site, url, months, error in pool.map(fetch, jobs):
        if error:
            errors.append([provider, url, error])
        for month in months:
            year = int(month["year"])
            number = list(calendar.month_name).index(month["name"])
            if (year, number) < (2021, 1) or (year, number) > (2026, 11):
                continue
            months_by_provider[provider][f"{year}-{number:02}"] = url
            for issue in month["incidents"]:
                stamp = html.unescape(issue["timestamp"])
                day = re.search(r"data-var=['\"]date['\"]>(\d+)", stamp)
                if not day:
                    missing_dates[provider] += 1
                    continue
                raw = re.sub("<[^>]*>", "", stamp).strip()
                first_month = re.match(r"([A-Za-z]{3})\b", raw)
                actual_month = list(calendar.month_abbr).index(first_month[1]) if first_month and first_month[1] in calendar.month_abbr else number
                displayed_date = date(year - int(actual_month > number), actual_month, int(day[1]))
                if date(2021, 1, 1) <= displayed_date <= date(2026, 11, 18):
                    issue_url = f"{site}/incidents/{issue['code']}"
                    matched = bool(keywords.search(issue["name"] + " " + (issue["message"] or "")))
                    issues[issue_url] = [provider, str(displayed_date), issue["impact"], issue["name"], issue_url, matched]
data = {"months": months_by_provider, "errors": errors, "missing_dates": missing_dates, "records": sorted(issues.values())}
Path("series-historicas.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
