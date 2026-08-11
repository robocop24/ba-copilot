from __future__ import annotations

import re
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity


def split_sentences(text: str) -> list[str]:
    """Naive sentence splitter. For production, use spaCy or nltk."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(
    file_path: str,
    model,
    similarity_threshold: float = 0.5,
    min_chunk_sentences: int = 2,
) -> list[str]:
    """
    Semantic chunking: split where meaning shifts.

    Args:
        file_path: Path to the document.
        model: SentenceTransformer instance (shared with caller).
        similarity_threshold: Cosine similarity below which a new chunk starts.
        min_chunk_sentences: Minimum sentences per chunk (merge small chunks).

    Returns:
        List of semantically coherent text chunks.
    """
    content = Path(file_path).read_text(encoding="utf-8")
    sentences = split_sentences(content)

    if len(sentences) <= min_chunk_sentences:
        return [content.strip()]

    # Compute embeddings for each sentence (uses caller's model)
    embeddings = model.encode(sentences)

    # Find breakpoints where similarity drops
    breakpoints = [0]  # always start at sentence 0
    for i in range(1, len(sentences)):
        sim = cosine_similarity(
            [embeddings[i - 1]], [embeddings[i]]
        )[0][0]
        if sim < similarity_threshold:
            breakpoints.append(i)

    breakpoints.append(len(sentences))  # end boundary

    # Build chunks from breakpoints
    chunks = []
    for start, end in zip(breakpoints, breakpoints[1:]):
        chunk = " ".join(sentences[start:end]).strip()
        if chunk:
            chunks.append(chunk)

    # Merge undersized chunks into neighbors
    chunks = _merge_small_chunks(chunks, sentences, min_chunk_sentences, breakpoints)

    return chunks


def _merge_small_chunks(
    chunks: list[str],
    sentences: list[str],
    min_sentences: int,
    breakpoints: list[int],
) -> list[str]:
    """Merge chunks that have too few sentences."""
    if len(chunks) <= 1:
        return chunks

    merged = []
    i = 0
    while i < len(chunks):
        current = chunks[i]
        sent_count = len(current.split(". "))  # rough sentence count

        if sent_count < min_sentences and i + 1 < len(chunks):
            # Merge with next chunk
            merged.append(current + " " + chunks[i + 1])
            i += 2
        elif sent_count < min_sentences and merged:
            # Merge with previous chunk
            merged[-1] = merged[-1] + " " + current
            i += 1
        else:
            merged.append(current)
            i += 1

    return merged