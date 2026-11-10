"""Print every report and page whose text contains a phrase. Usage: python scripts/find_page.py "phrase"."""

import json
import sys
from pathlib import Path

PAGES = Path("data/pages.jsonl")


def main() -> int:
    phrase = " ".join(sys.argv[1:]).lower()
    if not phrase:
        print('Usage: python scripts/find_page.py "phrase"', file=sys.stderr)
        return 1
    found = False
    for line in PAGES.open(encoding="utf-8"):
        page = json.loads(line)
        if phrase in " ".join(page["text"].split()).lower():
            print(f"{page['report_id']}, p. {page['page']}")
            found = True
    if not found:
        print("No pages contain that phrase.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

