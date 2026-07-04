from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parents[2] 
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

collection = client.get_or_create_collection(name="documents")

def store_embeddings(embedded_documents : list[dict]):
    """
    Input:
    [
        {
            "id": "...",
            "embedding": [...],
            "text": "...",
            "metadata": {...}
        }
    ]
    """
    collection.upsert(
        ids = [chunk["id"] for chunk in embedded_documents],
        embeddings = [chunk["embedding"] for chunk in embedded_documents],
        documents = [chunk["text"] for chunk in embedded_documents],
        metadatas = [chunk["metadata"] for chunk in embedded_documents]
    )
    

def search(
    query_embedding : list[float],
    n_results=5
):
    """
    query_embedding:
        List[float]

    returns:
        Similar chunks
    """

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

def count_documents():
    return collection.count()

def clear_database():
    ids = collection.get()["ids"]

    if ids:
        collection.delete(ids=ids)
        
def get_all_documents():
    return collection.get()