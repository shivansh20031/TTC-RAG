# TTC Transit RAG

A question-answering tool for TTC monthly CEO reports. It returns the report passages that answer a question, with the report and page for each one. A test set measures how often the correct page appears in the top 5 results.

## Status

- **Working:** chunking, BM25 keyword retrieval, cited passages, and evaluation (Recall@5).
- **Not yet built:** written answers generated from the passages.

## How it works

1. **Chunking** (`scripts/chunk_pages.py`): splits each page into overlapping 250-word chunks (40-word overlap). Each chunk keeps its report ID, month, title, URL, and page number. Output: `data/chunks.jsonl`.
2. **Retrieval** (`scripts/evaluate.py`, `scripts/ask.py`): ranks chunks for a question with BM25 and returns the top 5.
3. **Evaluation** (`data/test_set.csv`): each row has a question, a `report_id`, and the correct page(s). A question is a hit if the correct report and page are in the top 5.

## Setup

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/shivansh20031/TTC-RAG.git
cd TTC-RAG
uv sync
```

Place the CEO report PDFs in `data/raw/`. The filenames and their `report_id` values are listed in `data/sources.csv`.

## Usage

```bash
uv run python scripts/chunk_pages.py
uv run python scripts/evaluate.py
uv run python scripts/ask.py "How many streetcars does the TTC have?"
```

Saved evaluation runs are in `notes/`.

## Results

| Run | Questions | Recall@5 | Notes |
|---|---|---|---|
| First run | 20 | 13/20 (65%) | Before page and wording fixes. See `notes/run_04_ceo_questions.txt`. |
| After fixes | 20 | 19/20 (95%) | Page numbers and wording corrected after the first run. See `notes/run_05_fixed_pages.txt`. This score was tuned against these questions, so it is not a measure of accuracy on new questions. |

## Known limitations

- **Retrieval only:** the tool returns passages, not answers.
- **Keyword matching:** BM25 needs the question's words to appear in the report.
- **Wrong month:** every monthly report repeats the same metrics, so a passage from the wrong month can rank highly.
- **Small test set:** 20 questions is too few to measure accuracy reliably.

## License

The CEO reports belong to the TTC.
