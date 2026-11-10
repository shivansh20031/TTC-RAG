"""Keyword search over data/chunks.jsonl. Usage: python scripts/search.py "your question"."""

import json
import re
import sys
from pathlib import Path

from rank_bm25 import BM25Okapi

CHUNKS = Path("data/chunks.jsonl")
TOP_K = 5


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python scripts/search.py "your question"', file=sys.stderr)
        return 1

    query = " ".join(sys.argv[1:])
    with CHUNKS.open(encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]

    bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)

    shown = 0
    for i in ranked:
        if scores[i] <= 0 or shown == TOP_K:
            break
        c = chunks[i]
        snippet = " ".join(c["text"].split()[:40])
        print(f"[{c['report_id']}, p. {c['page']}] score {scores[i]:.2f}")
        print(f"  {snippet}...\n")
        shown += 1

    if shown == 0:
        print("No matching chunks found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
