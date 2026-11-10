"""Split data/pages.jsonl into overlapping word-window chunks in data/chunks.jsonl."""

import json
from pathlib import Path

PAGES = Path("data/pages.jsonl")
OUT = Path("data/chunks.jsonl")
MAX_WORDS = 250  # chunk size in words
OVERLAP = 40     # words shared between neighbouring chunks


def windows(words: list[str]) -> list[str]:
    """Return word windows of MAX_WORDS, each overlapping the previous by OVERLAP."""
    if len(words) <= MAX_WORDS:
        return [" ".join(words)] if words else []
    step = MAX_WORDS - OVERLAP
    return [" ".join(words[start:start + MAX_WORDS])
            for start in range(0, len(words), step)
            if words[start:start + MAX_WORDS]]


def main() -> None:
    count = 0
    with PAGES.open(encoding="utf-8") as src, OUT.open("w", encoding="utf-8") as out:
        for line in src:
            page = json.loads(line)
            for n, text in enumerate(windows(page["text"].split()), start=1):
                chunk = {
                    "chunk_id": f"{page['report_id']}-p{page['page']}-c{n}",
                    "report_id": page["report_id"],
                    "report_month": page["report_month"],
                    "title": page["title"],
                    "url": page["url"],
                    "page": page["page"],
                    "text": text,
                }
                out.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                count += 1
    print(f"Wrote {count} chunks to {OUT}")


if __name__ == "__main__":
    main()
