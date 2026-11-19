"""Export public incident indexes for the 2025–2026 measurement study."""
import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from statuspage import fetch_history_months, parse_issue_date, parse_month_key

SITES = {
    "GitHub": "www.githubstatus.com", "Cloudflare": "www.cloudflarestatus.com",
    "Anthropic": "status.claude.com", "Discord": "discordstatus.com",
    "DigitalOcean": "status.digitalocean.com", "Reddit": "www.redditstatus.com",
    "Zoom": "status.zoom.us", "Dropbox": "status.dropbox.com",
    "Twilio": "status.twilio.com", "Jira Software": "jira-software.status.atlassian.com",
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
    base_url = f"https://{domain}"
    url = f"{base_url}/history?page={page}"
    rows, coverage = [], []
    try:
        url, months = fetch_history_months(base_url, page, timeout=15, retries=1)
        for month in months:
            year, number = parse_month_key(month)
            if (year, number) < (2025, 1) or (year, number) > (2026, 11):
                continue
            issues = month["incidents"]
            coverage.append([provider, url, f"{year}-{number:02}", len(issues), "índice consultado"])
            for issue in issues:
                parsed = parse_issue_date(issue, year, number)
                if not parsed:
                    continue
                d, raw = parsed
                if START <= d <= END:
                    rows.append([provider, d.isoformat(), issue["impact"], issue["name"], f"{base_url}/incidents/{issue['code']}", raw])
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
