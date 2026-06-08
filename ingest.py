"""
Ingestion and chunking pipeline for the Unofficial Guide.

Loads documents from the documents/ folder (.txt files saved by fetch_sources.py),
cleans text, and produces semantic chunks with specified size and overlap.
"""

import re
from pathlib import Path
from typing import List, Dict
from datetime import datetime

DOCS_DIR = Path(__file__).parent / "documents"


def load_documents(docs_dir: Path = DOCS_DIR) -> List[Dict]:
    """
    Load documents from .txt files in the documents/ folder.

    Each document's identity comes from its filename, not from any URL. The
    file may start with a header written by fetch_sources.py:
        Title: <title>
        Source: <url>      <- kept for citation only, not used for identity
        <blank line>
        <body text...>

    Args:
        docs_dir: Folder containing the .txt source files

    Returns:
        List of dicts: {text, title, doc_id, source_url, date_loaded, source_type}
    """
    documents = []

    for path in sorted(docs_dir.glob("*.txt")):
        try:
            raw = path.read_text(encoding="utf-8")
            title, source_url, text = _parse_document(raw, path)

            if text and len(text.strip()) > 100:  # Only keep if substantial
                documents.append({
                    'text': text,
                    'title': title,
                    'doc_id': path.stem,
                    'source_url': source_url,
                    'date_loaded': datetime.now().isoformat(),
                    'source_type': 'reddit' if 'reddit' in path.stem else 'blog',
                })
                print(f"✓ Loaded: {path.name} ({len(text)} chars)")
            else:
                print(f"⚠ Skipped {path.name}: insufficient text")

        except Exception as e:
            print(f"✗ Failed to load {path.name}: {e}")

    return documents


def _parse_document(raw: str, path: Path) -> tuple:
    """Strip the header off a saved .txt file, returning (title, source_url, body).

    The Source: URL is kept for citation, but identity comes from the filename.
    """
    title = path.stem
    source_url = ''
    body = raw

    # Header lines precede the first blank line.
    header, _, rest = raw.partition("\n\n")
    if header.startswith("Title:") or header.startswith("Source:"):
        for line in header.splitlines():
            if line.startswith("Title:"):
                title = line[len("Title:"):].strip()
            elif line.startswith("Source:"):
                source_url = line[len("Source:"):].strip()
        body = rest

    return title, source_url, body


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text from document
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove Reddit-specific artifacts
    text = re.sub(r'r/\w+|u/\w+', '', text)
    text = re.sub(r'Edit:|EDIT:|Edit \d+:', '', text)
    
    # Remove excessive punctuation
    text = re.sub(r'([!?.])\1{2,}', r'\1', text)
    
    # Strip
    text = text.strip()
    
    return text


def chunk_document(text: str, doc_id: str, chunk_size: int = 300,
                  overlap: int = 50, metadata: Dict = None) -> List[Dict]:
    """
    Split document into chunks with overlap, respecting sentence boundaries.

    Args:
        text: Document text
        doc_id: Document identifier (the .txt filename stem), used as the
            chunk_id prefix
        chunk_size: Target chunk size in characters (default 300)
        overlap: Overlap between chunks in characters (default 50)
        metadata: Extra fields (e.g. title, source_type) merged into every chunk

    Returns:
        List of dicts: {text, chunk_id, **metadata}
    """
    metadata = metadata or {}

    # Clean text first
    text = clean_text(text)

    chunks = []
    chunk_id = 0
    start = 0

    def make_chunk(chunk_text: str) -> Dict:
        return {
            'text': chunk_text,
            'chunk_id': f"{doc_id}_{chunk_id}",
            **metadata,
        }

    while start < len(text):
        # Calculate end position
        end = start + chunk_size

        # Don't go past the end
        if end >= len(text):
            chunk_text = text[start:].strip()
            if len(chunk_text) >= 50:  # Only include if minimum length
                chunks.append(make_chunk(chunk_text))
            break

        # Look for sentence boundary near end to avoid splitting mid-sentence
        # Search backwards for '.', '?', '!' followed by space
        boundary = end
        for i in range(end, max(end - 100, start), -1):
            if text[i] in '.?!' and i + 1 < len(text) and text[i + 1] == ' ':
                boundary = i + 1
                break

        chunk_text = text[start:boundary].strip()

        # Only add chunk if it meets minimum length
        if len(chunk_text) >= 50:
            chunks.append(make_chunk(chunk_text))
            chunk_id += 1

        # Move start forward, accounting for overlap
        start = boundary - overlap
        if start <= 0 or start >= len(text):
            break

    return chunks


def ingest_and_chunk(docs_dir: Path = DOCS_DIR, chunk_size: int = 300,
                     overlap: int = 50) -> List[Dict]:
    """
    End-to-end ingestion and chunking pipeline.

    Loads every .txt file in docs_dir and chunks it.

    Args:
        docs_dir: Folder containing the .txt source files
        chunk_size: Chunk size in characters
        overlap: Overlap in characters

    Returns:
        List of chunks: {text, chunk_id, title, source_url, source_type}
    """
    print(f"\n📄 Loading documents from {docs_dir}...\n")
    documents = load_documents(docs_dir)

    print(f"\n✂️  Chunking {len(documents)} documents...\n")
    all_chunks = []

    for doc in documents:
        chunks = chunk_document(
            doc['text'], doc['doc_id'], chunk_size, overlap,
            metadata={
                'title': doc['title'],
                'source_url': doc['source_url'],  # citation only
                'source_type': doc['source_type'],
            },
        )
        all_chunks.extend(chunks)
        print(f"  {doc['title']}: {len(chunks)} chunks")

    print(f"\n✓ Total chunks: {len(all_chunks)}\n")

    return all_chunks


# Example usage
if __name__ == '__main__':
    # Run pipeline over the saved .txt files in documents/
    chunks = ingest_and_chunk(chunk_size=300, overlap=50)

    # Display sample chunks
    print("\n🔍 Sample chunks:\n")
    for i, chunk in enumerate(chunks[:3]):
        print(f"Chunk {i+1} (ID: {chunk['chunk_id']}):")
        print(f"  Source: {chunk['title']} ({chunk['source_type']})")
        print(f"  Length: {len(chunk['text'])} chars")
        print(f"  Text: {chunk['text'][:100]}...")
        print()

