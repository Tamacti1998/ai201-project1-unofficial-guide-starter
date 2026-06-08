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

    Each file starts with a header written by fetch_sources.py:
        Title: <title>
        Source: <url>
        <blank line>
        <body text...>

    Args:
        docs_dir: Folder containing the .txt source files

    Returns:
        List of dicts: {text, source_url, title, date_fetched, source_type}
    """
    documents = []

    for path in sorted(docs_dir.glob("*.txt")):
        try:
            raw = path.read_text(encoding="utf-8")
            title, source_url, text = _parse_document(raw, path)

            if text and len(text.strip()) > 100:  # Only keep if substantial
                documents.append({
                    'text': text,
                    'source_url': source_url,
                    'title': title,
                    'date_fetched': datetime.now().isoformat(),
                    'source_type': 'reddit' if 'reddit.com' in source_url else 'blog'
                })
                print(f"✓ Loaded: {path.name} ({len(text)} chars)")
            else:
                print(f"⚠ Skipped {path.name}: insufficient text")

        except Exception as e:
            print(f"✗ Failed to load {path.name}: {e}")

    return documents


def _parse_document(raw: str, path: Path) -> tuple:
    """Split a saved .txt file into (title, source_url, body)."""
    title = path.stem
    source_url = path.stem
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


def chunk_document(text: str, source_url: str, chunk_size: int = 300,
                  overlap: int = 50, metadata: Dict = None) -> List[Dict]:
    """
    Split document into chunks with overlap, respecting sentence boundaries.

    Args:
        text: Document text
        source_url: Source URL for metadata
        chunk_size: Target chunk size in characters (default 300)
        overlap: Overlap between chunks in characters (default 50)
        metadata: Extra fields (e.g. title, source_type) merged into every chunk

    Returns:
        List of dicts: {text, source_url, chunk_id, **metadata}
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
            'source_url': source_url,
            'chunk_id': f"{_url_to_id(source_url)}_{chunk_id}",
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


def _url_to_id(url: str) -> str:
    """Convert URL to a short, collision-free ID prefix."""
    # Strip protocol and any trailing slash so URLs that differ only by a
    # trailing '/' don't collapse to the same id.
    url = url.replace('https://', '').replace('http://', '').rstrip('/')
    parts = [p for p in url.split('/') if p]
    domain = parts[0].replace('.com', '').replace('www.', '') if parts else 'doc'
    # Last path segment is the most distinctive part (e.g. the thread slug/id).
    thread_id = parts[-1][:12] if len(parts) > 1 else ''
    return f"{domain}_{thread_id}".lower()


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
        List of chunks: {text, source_url, chunk_id, title, source_type}
    """
    print(f"\n📄 Loading documents from {docs_dir}...\n")
    documents = load_documents(docs_dir)

    print(f"\n✂️  Chunking {len(documents)} documents...\n")
    all_chunks = []

    for doc in documents:
        chunks = chunk_document(
            doc['text'], doc['source_url'], chunk_size, overlap,
            metadata={'title': doc['title'], 'source_type': doc['source_type']},
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

