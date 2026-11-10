"""Download the TTC CEO reports listed in data/sources.csv to data/raw/."""

import csv
import sys
import urllib.request
from pathlib import Path

SOURCES = Path("data/sources.csv")
RAW_DIR = Path("data/raw")
TIMEOUT = 60  # seconds per request


def download(url: str, dest: Path) -> None:
    """Fetch url into dest, writing to a temp file first so partial downloads never look complete."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = resp.read()

    if not data.startswith(b"%PDF"):
        raise ValueError("response is not a PDF (first bytes: %r)" % data[:20])

    tmp = dest.with_suffix(".pdf.part")
    tmp.write_bytes(data)
    tmp.rename(dest)


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with SOURCES.open(newline="", encoding="utf-8") as f:
        rows = [row for row in csv.DictReader(f) if row.get("report_id")]

    failures = []
    for row in rows:
        report_id = row["report_id"]
        dest = RAW_DIR / f"{report_id}.pdf"

        if dest.exists():
            print(f"skip   {report_id} (already downloaded)")
            continue

        try:
            download(row["url"], dest)
            size_kb = dest.stat().st_size // 1024
            print(f"ok     {report_id} ({size_kb} KB)")
        except Exception as exc:  # report and keep going
            print(f"FAIL   {report_id}: {exc}", file=sys.stderr)
            failures.append(report_id)

    print(f"\nDone. {len(rows) - len(failures)} of {len(rows)} reports available.")
    if failures:
        print("Failed: " + ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
