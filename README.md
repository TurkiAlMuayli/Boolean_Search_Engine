# Boolean Search Engine

A simple but functional Boolean search engine implemented from scratch in Python.
It builds an inverted index over a news corpus and supports AND (`&`) and OR (space)
query operators with real-time result retrieval.

## Features

- Inverted index construction from raw text documents
- Boolean query parsing: AND (`&`) and OR (space-separated) operators
- Case-insensitive search with punctuation stripping
- Loads and indexes real news articles from a JSON corpus
- Benchmarks index build time, query latency (in microseconds), and vocabulary size

## How queries work

Queries use a two-level syntax:

- **Space = OR** → terms/groups joined by spaces are unioned
- **`&` = AND** → terms joined by `&` are intersected within a group

Example:
`"President Donald&Trump"` → docs containing `"President"` OR (docs containing `"Donald"` AND `"Trump"`)

## Files

- `Boolean_Search_Engine.py` — main engine: indexing, querying, and experiment runner
- `news.json` — news corpus (JSONL format, one article per line)

## Usage

Place a `news.json` file (JSONL with `headline` and `short_description` fields) in the
same directory, then run:

```
python Boolean_Search_Engine.py
```

The script will load the corpus, build the index, and run a set of sample queries
with result counts and timing.

## Dataset

Compatible with the Kaggle News Category Dataset (HuffPost articles), which provides
`headline` and `short_description` fields in JSONL format.

## Performance

Benchmarked on the full corpus: **209,527 documents**, producing an inverted index
of **86,248 unique terms**.

| Query | Expansion | Results | Search Time (µs) |
|---|---|---|---|
| `Cristiano Ronaldo` | Cristiano OR Ronaldo | 20 | ~24–29 |
| `Anime` | Anime | 10 | ~6–14 |
| `President Donald&Trump` | President OR (Donald AND Trump) | 11,406 | ~3,500–14,700 |
| `DC&Comics` | DC AND Comics | 10 | ~47–216 |
| `Fifa World&Cup` | Fifa OR (World AND Cup) | 254 | ~409–588 |

Narrow AND queries and single-term lookups resolve in low double-digit microseconds
thanks to O(1) set lookups in the index. Broad OR queries (e.g. `"president"`) take
longer because the result set itself is large — the cost scales with the size of the
matched postings list, not the size of the corpus.

*(Timings were measured with Python's `time.time()` and vary slightly between runs
due to system load; values above show the observed range across multiple runs.)*

## Requirements

No external dependencies — standard library only (`json`, `re`, `time`).

## Design Choices

**Sets for building, lists for returning** — `set()` is used during index
construction for O(1) duplicate handling; `sorted()` on output ensures consistent,
reproducible ordering.

**Regex tokenization** — `re.findall(r'[a-z]+', doc.lower())` extracts only
lowercase alphabetic tokens; punctuation, numbers, and symbols are stripped
automatically.

**Fields indexed** — `headline + ' ' + short_description` are concatenated before
tokenizing. Category, authors, link, and date are deliberately excluded.

**`None` as AND sentinel** — `group_result = None` before the first term detects
the first token without an empty-set initialization that would otherwise always
yield zero results.

**Query parsing preserves `&`** — parse order is: split by space (OR) → split by
`&` (AND) → lowercase. Splitting happens before case conversion, so `&` is never
affected by `.lower()`.
