class Metrics:
    
    def __init__(self):
        
        
        self.metrics = {
            "mcp_calls":0,
            "cache_hits":0,
            "cache_misses":0,
            "rag_queries":0,
        }
        
    def increment(self, metric_name):
            
        self.metrics[metric_name] += 1
        
    def report(self):
        
        return self.metrics
            
        