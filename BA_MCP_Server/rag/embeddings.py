from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    
    def __init__(self):
        self.model  = SentenceTransformer("all-MiniLM-L6-v2")
        
    def embed_documents(self,chunks:list[str]):
        return self.model.encode(chunks)
    
    def embed_query(self, query:str):
        return self.model.encode(query)