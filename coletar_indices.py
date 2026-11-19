"""Export public incident indexes for the 2025–2026 measurement study."""
import calendar
import csv
import html
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

SITES = {
    "GitHub": "www.githubstatus.com", "Cloudflare": "www.cloudflarestatus.com",
    "Anthropic": "status.claude.com", "Discord": "discordstatus.com",
    "DigitalOcean": "status.digitalocean.com", "Reddit": "www.redditstatus.com",
    "Zoom": "status.zoom.us", "Dropbox": "status.dropbox.com",
    "Twilio": "status.twilio.com", "Atlassian Jira": "jira-software.status.atlassian.com",
}
START, END = date(2025, 1, 1), date(2026, 11, 18)
ROOT = Path(__file__).resolve().parent

def write(name, headers, rows):
    with (ROOT / name).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def collect(job):
    provider, domain, page = job
    url = f"https://{domain}/history?page={page}"
    rows, coverage = [], []
    try:
        body = subprocess.check_output(["curl.exe", "-fsSL", "--retry", "1", "--max-time", "15", url], stderr=subprocess.DEVNULL).decode()
        match = re.search(r'data-react-class="HistoryIndex" data-react-props="([^"]+)', body)
        data = json.loads(html.unescape(match[1]))
        for month in data["months"]:
            year, number = int(month["year"]), list(calendar.month_name).index(month["name"])
            if (year, number) < (2025, 1) or (year, number) > (2026, 11):
                continue
            issues = month["incidents"]
            coverage.append([provider, url, f"{year}-{number:02}", len(issues), "índice consultado"])
            for issue in issues:
                stamp = html.unescape(issue["timestamp"])
                day = re.search(r"data-var=['\"]date['\"]>(\d+)", stamp)
                if not day:
                    continue
                # The first displayed month may differ for an incident spanning months.
                raw = re.sub("<[^>]*>", "", stamp).strip()
                first_month = re.match(r"([A-Za-z]{3})\b", raw)
                actual_month = list(calendar.month_abbr).index(first_month[1]) if first_month and first_month[1] in calendar.month_abbr else number
                d = date(year - int(actual_month > number), actual_month, int(day[1]))
                if START <= d <= END:
                    rows.append([provider, d.isoformat(), issue["impact"], issue["name"], f"https://{domain}/incidents/{issue['code']}", raw])
    except Exception as exc:
        coverage.append([provider, url, "", "", f"falha de consulta ou leitura ({type(exc).__name__})"])
    return rows, coverage

if __name__ == "__main__":
    jobs = [(name, host, page) for name, host in SITES.items() for page in range(1, 9)]
    records, audit = {}, []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for rows, coverage in pool.map(collect, jobs):
            audit.extend(coverage)
            for row in rows:
                records[row[4]] = row
    write("indice-publico.csv", ["provedor","data_exibida","impacto_declarado","titulo_original","url","periodo_exibido"], sorted(records.values()))
    write("cobertura.csv", ["provedor","pagina","mes","registros_exibidos_antes_da_triagem","resultado"], sorted(audit))
