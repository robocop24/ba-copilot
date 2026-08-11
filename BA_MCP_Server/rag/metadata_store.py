class MetadataStore:
    
    def filter_chunks(self, chunks, project=None, module=None):
        
        filtered_chunks = chunks
                
        if project:
            filtered_chunks = [
            chunk for chunk in filtered_chunks
            if chunk["project"] == project
            ]
                    
        if module:
            filtered_chunks = [
            chunk for chunk in filtered_chunks
            if chunk["module"] == module
            ]           
                    
        return filtered_chunks
    
    
    @staticmethod
    def extract_query_metadata(query:str):
        
        query = query.lower()
        
        metadata = {}
        
        if any(word in query
               for word in ["login", "signin", "password", "authentication"]
               ):
            
            metadata["module"] = "authentication"
            
        elif any(word in query
               for word in ["invoice", "billing", "payment"]
               ):
            
            metadata["module"] = "billing"
            
        return metadata
    
    @staticmethod
    def extract_metadata(file_name:str):
        
        file_name = file_name.replace(".txt", '')
        
        parts = file_name.split("_")
        
        return {
            "project":"_".join(parts[:-1]),
            "module": parts[-1]
        }