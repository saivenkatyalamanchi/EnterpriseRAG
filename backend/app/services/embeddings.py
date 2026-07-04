from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def create_embeddings(chunks):
    """
    Input:
    [
        {
            "chunk_id": 0,
            "text": "...",
            "metadata": {...}
        }
    ]
    """

    texts = [
        chunk["chunk"]
        for chunk in chunks
    ]

    vectors = model.encode(
        texts,
        normalize_embeddings=True
    )

    results = []

    for chunk, vector in zip(chunks, vectors):
        results.append(
            {
                "id":
                    f"{chunk['metadata']['source']}"
                    f"_{chunk['metadata']['chunk_index']}",

                "embedding":
                    vector.tolist(),

                "text":
                    chunk["chunk"],

                "metadata":
                    chunk["metadata"]
            }
        )

    return results