import chromadb
import uuid
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path="./chromadb")

def list_collections():
    return [col.name for col in chroma_client.list_collections()]

def get_or_create_collection(name: str):
    return chroma_client.get_or_create_collection(name=name.replace(" ", "_"))

def add_documents_to_collection(collection_name: str, chunks: list[str]):
    collection = get_or_create_collection(collection_name)

    unique_ids = [str(uuid.uuid4()) for _ in chunks]
    collection.add(
        ids=unique_ids,
        documents=chunks
    )

def query_collection(collection_name: str, query_text: str, n_results: int = 2):
    collection = chroma_client.get_collection(name=collection_name)
    return collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents"]
    )["documents"]

def delete_collection(name: str):
    """Supprime une collection ChromaDB si elle existe."""
    try:
        chroma_client.delete_collection(name)
    except Exception as e:
        print(f"Erreur lors de la suppression de la collection {name}: {e}")
