"""Measure retrieval. test_set.csv columns: question,report_id,page (page may be '2' or '2|8')."""

import csv
import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

CHUNKS = Path("data/chunks.jsonl")
TEST_SET = Path("data/test_set.csv")
K = 5
STOPWORDS = {"a", "an", "the", "is", "was", "were", "are", "of", "for", "in", "on", "to",
             "what", "which", "how", "did", "does", "do", "and", "by", "at", "with"}


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


def main() -> int:
    chunks = [json.loads(line) for line in CHUNKS.open(encoding="utf-8")]
    bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])
    tests = list(csv.DictReader(TEST_SET.open(newline="", encoding="utf-8")))

    hits = 0
    for t in tests:
        pages = {int(p) for p in t["page"].split("|")}
        scores = bm25.get_scores(tokenize(t["question"]))
        top = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)[:K]
        rank = next((r for r, i in enumerate(top, 1)
                     if chunks[i]["report_id"] == t["report_id"] and chunks[i]["page"] in pages), None)
        hits += rank is not None
        print(f"{'HIT  (rank ' + str(rank) + ')' if rank else 'MISS'} {t['question']}")

    print(f"\nRecall@{K}: {hits}/{len(tests)} = {hits / len(tests):.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

