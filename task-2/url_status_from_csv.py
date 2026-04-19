import csv
import sys
from urllib.parse import urlparse
import requests


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""

    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url

    return url


def iter_urls_from_csv(csv_path: str, column_name: str = "urls"):
    with open(csv_path, "r", encoding="utf-8", newline="") as f:  # fixed encoding
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
        print("Usage: python url_status_from_csv.py 'file.csv'")
        sys.exit(1)

    csv_path = sys.argv[1]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "url-status-checker/1.0 (by Ejibode Ibraheem - https://github.com/Linsmed/DEVOPS-PROJECT)"
        }  # improved user-agent with identity
    )

    timeout_seconds = 15

    for url in iter_urls_from_csv(csv_path):
        try:
            try:
                resp = session.head(url, allow_redirects=True, timeout=timeout_seconds)
                status = resp.status_code

                # If server rejects HEAD, fall back to GET
                if status in (405, 501):
                    raise requests.RequestException("HEAD not supported")

            except requests.RequestException:
                resp = session.get(
                    url, allow_redirects=True, timeout=timeout_seconds, stream=True
                )
                status = resp.status_code

            print(f"({status}) {url}")

        except requests.RequestException as e:
            error_type = type(e).__name__
            print(f"(ERROR: {error_type}) {url}")


if __name__ == "__main__":
    main()