from backend.app.services.embeddings import model
from backend.app.services.vectordb import search


def retrieve(
    query: str,
    n_results: int = 5
):
    """
    Retrieve the most relevant chunks for a query.

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