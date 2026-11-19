"""Export public incident indexes for the 2025–2026 measurement study."""
import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from statuspage import StatuspageClient, parse_issue_date, parse_month_key

SITES = {
    "GitHub": "www.githubstatus.com", "Cloudflare": "www.cloudflarestatus.com",
    "Anthropic": "status.claude.com", "Discord": "discordstatus.com",
    "DigitalOcean": "status.digitalocean.com", "Reddit": "www.redditstatus.com",
    "Zoom": "status.zoom.us", "Dropbox": "status.dropbox.com",
    "Twilio": "status.twilio.com", "Jira Software": "jira-software.status.atlassian.com",
}
START, END = date(2025, 1, 1), date(2026, 11, 18)
START_YM, END_YM = (2025, 1), (2026, 11)
MAX_PAGES = 8
ROOT = Path(__file__).resolve().parent


def write(name, headers, rows):
    with (ROOT / name).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def collect_provider(provider: str, domain: str) -> tuple[dict[str, list], list[list]]:
    base_url = f"https://{domain}"
    records: dict[str, list] = {}
    coverage: list[list] = []
    seen_months: set[tuple[int, int]] = set()

    with StatuspageClient(timeout=15, retries=1) as client:
        for page in range(1, MAX_PAGES + 1):
            url = f"{base_url}/history?page={page}"
            try:
                url, months = client.fetch_history_months(base_url, page)
            except Exception as exc:
                coverage.append([provider, url, "", "", f"falha de consulta ou leitura ({type(exc).__name__})"])
                break

            page_months = [(month, parse_month_key(month)) for month in months]
            if not page_months or all(ym in seen_months for _, ym in page_months):
                break
            seen_months.update(ym for _, ym in page_months)

            for month, ym in page_months:
                if ym < START_YM or ym > END_YM:
                    continue
                year, number = ym
                issues = month["incidents"]
                coverage.append([provider, url, f"{year}-{number:02}", len(issues), "índice consultado"])
                for issue in issues:
                    issue_url = f"{base_url}/incidents/{issue['code']}"
                    if issue_url in records:
                        continue
                    parsed = parse_issue_date(issue, year, number)
                    if not parsed:
                        continue
                    d, raw = parsed
                    if START <= d <= END:
                        records[issue_url] = [provider, d.isoformat(), issue["impact"], issue["name"], issue_url, raw]

            if min(ym for _, ym in page_months) < START_YM:
                break

    return records, coverage


def main():
    records, audit = {}, []
    with ThreadPoolExecutor(max_workers=min(8, len(SITES))) as pool:
        for prov_records, coverage in pool.map(lambda item: collect_provider(*item), SITES.items()):
            records.update(prov_records)
            audit.extend(coverage)
    write("indice-publico.csv", ["provedor", "data_exibida", "impacto_declarado", "titulo_original", "url", "periodo_exibido"], sorted(records.values()))
    write("cobertura.csv", ["provedor", "pagina", "mes", "registros_exibidos_antes_da_triagem", "resultado"], sorted(audit))


if __name__ == "__main__":
    main()
