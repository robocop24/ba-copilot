class Retriever:
    
    def __init__(self, vector_store):
        
        self.vector_store = vector_store
        
    
    def retrieve(self, query_embedding, top_k=10):
        
        distances, indices = (
            self.vector_store.search(query_embedding, top_k)
        )
        
        results = []
        
        for idx, distance in zip(indices[0], distances[0]):
            
            results.append(
                {"chunk": self.vector_store.chunks[idx],
                "distance": float(distance)}
            )
            
        return results