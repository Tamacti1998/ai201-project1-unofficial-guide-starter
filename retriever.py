"""
Embedding + vector store + retrieval for the Unofficial Guide.

Architecture (see planning.md):
    Chunking (ingest.py)
      -> Embedding (sentence-transformers, all-MiniLM-L6-v2)
      -> Vector store (ChromaDB, cosine similarity, persisted to ./chroma_db)
      -> Retrieval (semantic search, top-k = 5)

Run this file directly to (re)build the index and try a sample query.
"""

from typing import List, Dict

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import ingest_and_chunk

# --- Config -----------------------------------------------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # 384-dim, per planning.md Retrieval Approach
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "unofficial_guide"
N_RESULTS = 5                          # top-k, per planning.md

# Cache the model so it is loaded once per process, not on every call.
_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL} ...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection(reset: bool = False):
    """Return the ChromaDB collection (cosine space), optionally wiped first."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass  # collection didn't exist yet
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed_and_store(chunks: List[Dict]) -> int:
    """
    Embed chunks with all-MiniLM-L6-v2 and store them in ChromaDB with metadata.

    Each chunk dict (from ingest.py) carries: text, chunk_id, title, source_url,
    source_type. The text is embedded; the rest is stored as metadata so
    retrieval can surface source attribution.

    Returns the number of chunks stored.
    """
    if not chunks:
        print("No chunks to embed.")
        return 0

    model = _get_model()
    collection = _get_collection(reset=True)  # fresh build each time

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks ...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=[e.tolist() for e in embeddings],
        documents=texts,
        metadatas=[
            {
                "title": c.get("title", ""),
                "source_url": c.get("source_url", ""),
                "source_type": c.get("source_type", ""),
            }
            for c in chunks
        ],
    )
    print(f"✓ Stored {collection.count()} chunks in ChromaDB ({CHROMA_PATH})")
    return collection.count()


def retrieve(query: str, k: int = N_RESULTS) -> List[Dict]:
    """
    Embed `query` and return the top-k most similar chunks by cosine similarity.

    Returns a list of dicts (most relevant first), each with:
      text, title, source_url, source_type, chunk_id, similarity
    where similarity = 1 - cosine_distance (1.0 = identical, 0.0 = unrelated).
    """
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for doc, meta, dist, cid in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
        results["ids"][0],
    ):
        hits.append({
            "text": doc,
            "title": meta.get("title", ""),
            "source_url": meta.get("source_url", ""),
            "source_type": meta.get("source_type", ""),
            "chunk_id": cid,
            "similarity": round(1 - dist, 4),
        })
    return hits


def build_index() -> int:
    """Run the full ingest -> chunk -> embed -> store pipeline."""
    chunks = ingest_and_chunk()
    return embed_and_store(chunks)


if __name__ == "__main__":
    build_index()

    sample = "Why do students find organic chemistry so hard?"
    print(f"\n🔍 Query: {sample}\n")
    for i, hit in enumerate(retrieve(sample), 1):
        print(f"{i}. [{hit['similarity']:.3f}] {hit['title']} ({hit['source_type']})")
        print(f"   {hit['text'][:140]}...\n")
