"""
RAG Engine — encapsulates the full retrieval pipeline:
  chunk → enrich → embed → FAISS ANN → hybrid re-rank
"""
import json
from pathlib import Path

from .chunker import chunk_text
from .embeddings import EmbeddingModel
from .hybrid_search import HybridSearch
from .metadata_store import MetadataStore
from .retriever import Retriever
from .vector_store import VectorStore


class RAGEngine:
    """Loads knowledge base once, exposes a .retrieve(query) method."""

    def __init__(self, knowledge_base_dir: str | None = None):
        if knowledge_base_dir is None:
            knowledge_base_dir = Path(__file__).parent.parent / "knowledge_base"

        self.kb_dir = Path(knowledge_base_dir)
        self.metadata_store = MetadataStore()
        self.embedding_model = EmbeddingModel()
        self._cache_path = self.kb_dir / "cached_chunks.json"

        # ── 1. Load or build chunks ─────────────────────────
        self.all_chunks = self._load_or_build_chunks()

    # ── Private helpers ─────────────────────────────────────
    def _load_or_build_chunks(self) -> list[dict]:
        """Return cached chunks if fresh, otherwise re-chunk from source files."""
        txt_files = list(self.kb_dir.glob("*.txt"))

        if self._cache_path.exists():
            cache_mtime = self._cache_path.stat().st_mtime
            newest_source = max(f.stat().st_mtime for f in txt_files)
            if cache_mtime >= newest_source:
                return json.loads(self._cache_path.read_text(encoding="utf-8"))

        # Build from scratch
        chunks = self._build_chunks(txt_files)
        self._cache_path.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
        return chunks

    def _build_chunks(self, txt_files: list[Path]) -> list[dict]:
        """Chunk all txt files and attach metadata."""
        all_chunks: list[dict] = []
        for file_path in txt_files:
            metadata = self.metadata_store.extract_metadata(file_path.name)
            for chunk in chunk_text(file_path, self.embedding_model.model):
                all_chunks.append({
                    "text": chunk,
                    "project": metadata["project"],
                    "module": metadata["module"],
                })
        return all_chunks

    def retrieve(self, query: str, top_k: int = 3, candidate_k: int = 10) -> str:
        """Run the full two-stage pipeline and return formatted results."""

        # ── Query enrichment (metadata filter) ──────────────
        enrich = self.metadata_store.extract_query_metadata(query) or {}

        # ── Stage 1: metadata filter → FAISS ANN ────────────
        filtered = self.metadata_store.filter_chunks(self.all_chunks, **enrich)
        if not filtered:
            return (
                f"No relevant BRD knowledge found for '{query}'.\n"
                f"Available modules: authentication, billing, checkout, claims"
            )

        filtered_texts = [c["text"] for c in filtered]
        filtered_embeddings = self.embedding_model.embed_documents(filtered_texts)

        # Build a temporary FAISS index on the filtered subset
        temp_store = VectorStore(filtered_texts, filtered_embeddings)
        temp_retriever = Retriever(temp_store)

        query_emb = self.embedding_model.embed_query(query)
        candidates = temp_retriever.retrieve(query_emb, top_k=min(candidate_k, len(filtered_texts)))

        # ── Stage 2: hybrid re-rank ─────────────────────────
        candidate_texts = [item["chunk"] for item in candidates]
        candidate_embeddings = self.embedding_model.embed_documents(candidate_texts)

        hybrid = HybridSearch(candidate_texts, candidate_embeddings)
        results = hybrid.search(query, query_emb, top_k=min(top_k, len(candidate_texts)))

        # ── Format output ───────────────────────────────────
        lines = [f"Top {len(results)} relevant BRD snippets for: '{query}'\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"--- Result {i} (hybrid: {r['hybrid_score']:.3f}) ---")
            lines.append(r["chunk"])
            lines.append("")
        return "\n".join(lines)
