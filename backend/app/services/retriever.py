from backend.app.services.embeddings import model
from backend.app.services.vectordb import search
from backend.app.services.bm25 import bm25_search


def retrieve(
    query: str,
    n_results: int = 5
):
    """
    Retrieve the most relevant chunks for a query
    using semantic (embedding) search only.

    Args:
        query: User question
        n_results: Number of chunks to retrieve

    Returns:
        [
            {
                "id": "...",
                "text": "...",
                "metadata": {...},
                "distance": ...
            }
        ]
    """

    # Generate query embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Search vector database
    results = search(
        query_embedding=query_embedding,
        n_results=n_results
    )

    retrieved_chunks = []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for chunk_id, text, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances
    ):
        retrieved_chunks.append(
            {
                "id": chunk_id,
                "text": text,
                "metadata": metadata,
                "distance": distance
            }
        )

    return retrieved_chunks


def hybrid_retrieve(
    query: str,
    n_results: int = 5,
    k: int = 60
):
    """
    Hybrid retrieval combining semantic search and BM25,
    merged using Reciprocal Rank Fusion (RRF).

    RRF score = Σ 1 / (k + rank)

    Args:
        query: User question
        n_results: Number of final chunks to return
        k: RRF constant (default 60, standard value)

    Returns:
        [
            {
                "id": "...",
                "text": "...",
                "metadata": {...},
                "score": ...,
                "sources": ["semantic", "bm25"] or ["semantic"] or ["bm25"]
            }
        ]
    """

    # --- 1. Semantic search ---
    semantic_results = retrieve(
        query,
        n_results=n_results
    )

    # --- 2. BM25 search ---
    bm25_results = bm25_search(
        query,
        n_results=n_results
    )

    # --- 3. Reciprocal Rank Fusion ---
    # Track RRF scores and chunk data by ID
    rrf_scores: dict[str, float] = {}
    chunk_data: dict[str, dict] = {}
    chunk_sources: dict[str, list[str]] = {}

    # Score semantic results by rank
    for rank, chunk in enumerate(semantic_results, start=1):
        chunk_id = chunk["id"]
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1 / (k + rank)
        chunk_data[chunk_id] = {
            "id": chunk_id,
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        }
        chunk_sources[chunk_id] = ["semantic"]

    # Score BM25 results by rank
    for rank, chunk in enumerate(bm25_results, start=1):
        chunk_id = chunk["id"]
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1 / (k + rank)
        if chunk_id not in chunk_data:
            chunk_data[chunk_id] = {
                "id": chunk_id,
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            }
            chunk_sources[chunk_id] = ["bm25"]
        else:
            chunk_sources[chunk_id].append("bm25")

    # --- 4. Sort by fused score and return top-N ---
    sorted_ids = sorted(
        rrf_scores,
        key=lambda cid: rrf_scores[cid],
        reverse=True
    )[:n_results]

    fused_results = []
    for chunk_id in sorted_ids:
        result = chunk_data[chunk_id]
        result["score"] = rrf_scores[chunk_id]
        result["sources"] = chunk_sources[chunk_id]
        fused_results.append(result)

    return fused_results