import sys
from pathlib import Path

# Make rag/ importable from tools/
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.rag_engine import RAGEngine

from observability.logger import log_event
from observability.metrics_registry import metrics, save_metrics
from observability.trace import generate_trace_id, set_trace_id

# Build once at module load — FAISS index + embeddings live in memory
_engine = RAGEngine()


def retrieve_similar_brd(requirement: str, trace_id: str = "") -> str:
    """Retrieve relevant BRD knowledge via two-stage RAG (FAISS + hybrid re-rank)."""
    
    set_trace_id(trace_id or generate_trace_id())
    
    log_event("mcp", f"retrieve_similar_brd called requirement='{requirement[:60]}'")
    metrics.increment("rag_queries")
    save_metrics("mcp_metrics.json")
    
    result = _engine.retrieve(requirement, top_k=3)
    log_event("mcp", "retrieve_similar_brd completed")
    return result

