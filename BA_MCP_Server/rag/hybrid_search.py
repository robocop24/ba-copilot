from .keyword_search import KeywordSearch
from .semantic_search import SemanticSearch


class HybridSearch:
    
    def __init__(self, chunks, chunk_embeddings):
        
        self.chunks = chunks
        
        self.chunk_embeddings = chunk_embeddings
        
        self.keyword_search = KeywordSearch()
        
        
    def search(self, query, query_embedding, top_k=3):
        
        results = []
                
        for (chunk, embedding) in zip(self.chunks, self.chunk_embeddings):
            
            semantic_score = SemanticSearch.cosine_similarity(
                query_embedding, embedding)
              
            keyword_score = self.keyword_search.score(
                query=query, chunk=chunk)
            
            hybrid_score = (
                (0.8 * semantic_score) + (0.2 * keyword_score)
            )
            
            results.append(
                {
                    "chunk": chunk,
                    "semantic_score": float(semantic_score),
                    "keyword_score": keyword_score,
                    "hybrid_score": float(hybrid_score)
                }
            )
            
            
        results = sorted(
            results, key=lambda x: x["hybrid_score"], reverse=True)
                    
        return results[:top_k]