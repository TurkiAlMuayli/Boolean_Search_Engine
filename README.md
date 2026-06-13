## Boolean Search Engine

A simple but functional Boolean search engine implemented from scratch in Python.
It builds an inverted index over a news corpus and supports AND (&) and OR (space)
query operators with real-time result retrieval.

### Features
- Inverted index construction from raw text documents
- Boolean query parsing: AND (&) and OR (space-separated) operators
- Case-insensitive search with punctuation stripping
- Loads and indexes real news articles from a JSON corpus
- Benchmarks index build time, query latency (in microseconds), and vocabulary size

### How queries work
Queries use a two-level syntax:
- Space = OR  →  terms/groups joined by spaces are unioned
- & = AND      →  terms joined by & are intersected within a group

Example:
  "President Donald&Trump"  →  docs containing "President" OR (docs containing "Donald" AND "Trump")

### Files
- Boolean_Search_Engine.py  — main engine: indexing, querying, and experiment runner
- news.json                 — news corpus (JSONL format, one article per line)

### Usage
Place a news.json file (JSONL with headline and short_description fields) in the same
directory, then run:

    python Boolean_Search_Engine.py

The script will load the corpus, build the index, and run a set of sample queries
with result counts and timing.

### Dataset
Compatible with the Kaggle News Category Dataset (HuffPost articles), which provides
headline and short_description fields in JSONL format.
