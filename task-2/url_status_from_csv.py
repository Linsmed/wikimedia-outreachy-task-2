import csv
import sys
from urllib.parse import urlparse

import requests


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    # Skip empty lines
    if not url:
        return ""
    # If someone put a bare domain, add scheme (not expected here, but safe)
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url
    return url


def iter_urls_from_csv(csv_path: str, column_name: str = "urls"):
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or column_name not in reader.fieldnames:
            raise ValueError(
                f"CSV must contain a column named '{column_name}'. Found columns: {reader.fieldnames}"
            )
        for row in reader:
            url = normalize_url(row.get(column_name, ""))
            if url:
                yield url


def main():
    if len(sys.argv) < 2:
        print("Usage: python url_status_from_csv.py 'Task 2 - Intern.csv'")
        sys.exit(1)

    csv_path = sys.argv[1]

    session = requests.Session()
    # Identify yourself a bit; some sites block default python UA
    session.headers.update(
        {"User-Agent": "url-status-checker/1.0 (+https://github.com/)"}
    )

    timeout_seconds = 15

    for url in iter_urls_from_csv(csv_path, column_name="urls"):
        try:
            # Try HEAD first (faster, less bandwidth). Some servers don't support it.
            try:
                resp = session.head(url, allow_redirects=True, timeout=timeout_seconds)
                status = resp.status_code
                # If server rejects HEAD, fall back to GET
                if status in (405, 501):
                    raise requests.RequestException("HEAD not allowed/supported")
            except requests.RequestException:
                resp = session.get(
                    url, allow_redirects=True, timeout=timeout_seconds, stream=True
                )
                status = resp.status_code

            print(f"({status}) {url}")

        except requests.RequestException:
            print(f"(ERROR) {url}")


if __name__ == "__main__":
    main()