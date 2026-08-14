from pathlib import Path

# from BA_MCP_Server.rag.rag_engine import RAGEngine
from observability import generate_trace_id, log_event, set_trace_id

# set_trace_id(generate_trace_id())
# result = RAGEngine().retrieve("How should user login")
# print(result)
from .chunker import chunk_text
from .embeddings import EmbeddingModel
from .hybrid_search import HybridSearch
from .metadata_store import MetadataStore
from .retriever import Retriever
from .vector_store import VectorStore

KNOWLEDGE_BASE = Path(__file__).parent.parent / "knowledge_base"

files = list(KNOWLEDGE_BASE.glob("*.txt"))

embedding_model = EmbeddingModel()
#metadata enrichment start here with overlapping chunking
metadata_store = MetadataStore()

query = "How should user login"
set_trace_id(generate_trace_id())
log_event("rag", f"retrieve() called with query='{query}'")
enrich_query = metadata_store.extract_query_metadata(query)

all_chunks = []

for file in files:
    
    metadata = metadata_store.extract_metadata(file.name)
    
    chunks = chunk_text(file, embedding_model.model)
    
    for chunk in chunks:
        
        all_chunks.append(
                {
                    "text":chunk,
                    "project":metadata["project"],
                    "module":metadata["module"]
                }
            )
        
        
print(f"\nTotal chunks before filtering: {len(all_chunks)}")
print(f"enrich_query: {enrich_query}\n")

filtered_chunks = metadata_store.filter_chunks(all_chunks, **enrich_query)

print(f"Filtered chunks: {len(filtered_chunks)}\n")
# for chunk in filtered_chunks:        
#     print(f"[{chunk['project']}] [{chunk['module']}] {chunk['text'][:80]}...\n")
#metadata enrichment start here

chunks_text = [chunk["text"] for chunk in filtered_chunks]

#embedding starts here

chunks_embedding = embedding_model.embed_documents(chunks_text)
query_embedding = embedding_model.embed_query(query)
#embedding ends here

# vector serach by Faiss (HNSW) start here
vector_store = VectorStore(chunks_text, chunks_embedding)

retriver = Retriever(vector_store)

retrived_chunks = retriver.retrieve(query_embedding, top_k=10)
# vector serach by Faiss (HNSW) ends here

# hybrid search starts here
retrived_texts = [item["chunk"] for item in retrived_chunks]

retrived_chunks_embedding = embedding_model.embed_documents(retrived_texts)

hybrid_search = HybridSearch(retrived_texts, retrived_chunks_embedding)

results = hybrid_search.search(query, query_embedding, top_k=3)
# hybrid search ends here

print("\nResults:\n")

for result in results:
    
    print("*" * 50)
    
    print("Chunk: ", f"{result['chunk']}")
    
    print("Semantic Score: ", f"{result['semantic_score']:.4f}")
    
    print("Keyword Score: ", f"{result['keyword_score']}")
    
    print("Hybrid Score: ", f"{result['hybrid_score']:.4f}")