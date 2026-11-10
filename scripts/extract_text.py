"""Extract per-page text from data/raw/*.pdf into data/pages.jsonl."""

import csv
import json
import sys
from pathlib import Path

from pypdf import PdfReader

SOURCES = Path("data/sources.csv")
RAW_DIR = Path("data/raw")
OUT = Path("data/pages.jsonl")
MIN_CHARS = 50  # pages with less text than this are flagged (possibly images/scans)


def main() -> int:
    with SOURCES.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("report_id")]

    total_pages = 0
    with OUT.open("w", encoding="utf-8") as out:
        for row in rows:
            report_id = row["report_id"]
            pdf_path = RAW_DIR / f"{report_id}.pdf"
            if not pdf_path.exists():
                print(f"MISSING {report_id}", file=sys.stderr)
                continue

            reader = PdfReader(str(pdf_path))
            sparse = []
            for i, page in enumerate(reader.pages, start=1):
                text = (page.extract_text() or "").strip()
                if len(text) < MIN_CHARS:
                    sparse.append(i)
                record = {
                    "report_id": report_id,
                    "report_month": row["report_month"],
                    "title": row["title"],
                    "url": row["url"],
                    "page": i,
                    "text": text,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
            total_pages += len(reader.pages)

            note = f" | low-text pages: {sparse}" if sparse else ""
            print(f"{report_id}: {len(reader.pages)} pages{note}")

    print(f"\nWrote {total_pages} pages to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
