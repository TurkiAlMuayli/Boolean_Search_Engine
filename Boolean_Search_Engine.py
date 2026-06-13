import json
import re
import time


def create_index(corpus):
    index = {}
    for doc_id, document in enumerate(corpus):
        tokens = set(re.findall(r'[a-z]+', document.lower()))  # lowercase & strip punctuation
        for token in tokens:
            if token not in index:
                index[token] = set()
            index[token].add(doc_id)
    return index


def boolean_search(query, index):
    if not query or not query.strip():
        return []

    result = set()

    for group in query.strip().split(' '):  # space = OR, split into OR-groups
        if not group:
            continue

        group_result = None
        for term in group.split('&'):       # & = AND, split into AND-terms
            term = term.lower()
            if not term:
                continue
            term_docs = index.get(term, set())
            if group_result is None:
                group_result = set(term_docs)   # first term, initialise
            else:
                group_result &= term_docs       # intersect (AND)

        if group_result:
            result |= group_result              # union across OR-groups

    return sorted(result)


def load_news_corpus(filepath):
    corpus = []
    metadata = []
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                article = json.loads(line)
                text = (article.get('headline', '') + ' ' +
                        article.get('short_description', ''))  # combine fields as document text
                corpus.append(text)
                metadata.append(article)
            except json.JSONDecodeError:
                continue
    return corpus, metadata


def run_experiments(news_filepath):
    print("Loading news corpus ...")
    t0 = time.time()
    corpus, metadata = load_news_corpus(news_filepath)
    t1 = time.time()
    print(f"  {len(corpus):,} articles loaded in {(t1 - t0) * 10**6:,.0f} us\n")

    print("Building inverted index ...")
    t0 = time.time()
    index = create_index(corpus)
    t1 = time.time()
    print(f"  Index built in {(t1 - t0) * 10**6:,.0f} us")
    print(f"  Vocabulary size: {len(index):,} unique terms\n")

    queries = [
        "Cristiano Ronaldo",
        "Anime",
        "President Donald&Trump",
        "DC&Comics",
        "Fifa World&Cup",
    ]

    sep = "=" * 62
    print(sep)

    for query in queries:
        t0 = time.time()
        results = boolean_search(query, index)
        t1 = time.time()
        elapsed_us = (t1 - t0) * 10**6     # convert to microseconds

        print(f"  '{query}'")
        print(f"    Results : {len(results):,}")
        print(f"    Time    : {elapsed_us:.2f} us")
        for doc_id in results[:3]:
            print(f"    -> [{doc_id}] {metadata[doc_id]['headline'][:70]}")
        print()

    print(sep)


if __name__ == "__main__":
    NEWS_PATH = "news.json"
    run_experiments(NEWS_PATH)
