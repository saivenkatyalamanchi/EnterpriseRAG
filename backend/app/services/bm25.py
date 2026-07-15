import re
from rank_bm25 import BM25Okapi
from backend.app.services.vectordb import get_all_documents


# Module-level state for the BM25 index
_bm25_index = None
_corpus_ids = []
_corpus_texts = []
_corpus_metadatas = []


def _tokenize(text: str) -> list[str]:
    """
    Simple whitespace + lowercased tokenizer.
    Strips punctuation for better keyword matching.
    """
    return re.findall(r"\w+", text.lower())


def build_bm25_index():
    """
    Build (or rebuild) the BM25 index from all
    documents currently stored in ChromaDB.

    Call this after every upload so the index
    stays in sync with the vector store.
    """
    global _bm25_index, _corpus_ids, _corpus_texts, _corpus_metadatas

    all_docs = get_all_documents()

    _corpus_ids = all_docs["ids"]
    _corpus_texts = all_docs["documents"]
    _corpus_metadatas = all_docs["metadatas"]

    if not _corpus_texts:
        _bm25_index = None
        return

    tokenized_corpus = [
        _tokenize(text) for text in _corpus_texts
    ]

    _bm25_index = BM25Okapi(tokenized_corpus)


def bm25_search(
    query: str,
    n_results: int = 5
) -> list[dict]:
    """
    Search the BM25 index for the most relevant chunks.

    Args:
        query: User question
        n_results: Number of chunks to retrieve

    Returns:
        [
            {
                "id": "...",
                "text": "...",
                "metadata": {...},
                "score": ...
            }
        ]
    """
    if _bm25_index is None:
        # Index not built yet — try building it now
        build_bm25_index()

    if _bm25_index is None:
        # Still None means no documents exist
        return []

    tokenized_query = _tokenize(query)
    scores = _bm25_index.get_scores(tokenized_query)

    # Get top-N indices sorted by score (descending)
    top_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:n_results]

    results = []
    for idx in top_indices:
        results.append({
            "id": _corpus_ids[idx],
            "text": _corpus_texts[idx],
            "metadata": _corpus_metadatas[idx],
            "score": float(scores[idx])
        })

    return results
