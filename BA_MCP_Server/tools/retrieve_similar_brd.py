import sys
from pathlib import Path

# Make rag/ importable from tools/
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.rag_engine import RAGEngine

# Build once at module load — FAISS index + embeddings live in memory
_engine = RAGEngine()


def retrieve_similar_brd(requirement: str) -> str:
    """Retrieve relevant BRD knowledge via two-stage RAG (FAISS + hybrid re-rank)."""
    return _engine.retrieve(requirement, top_k=3)

