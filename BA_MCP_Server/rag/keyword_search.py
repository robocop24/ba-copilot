class KeywordSearch:
    

    def score(self, query:str, chunk:str):
        
        query_words = set(query.lower().split())
    
        chunk_words = set(chunk.lower().split())
    
        return len(query_words.intersection(chunk_words))