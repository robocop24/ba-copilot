import threading
from collections import defaultdict


class Metrics:
    
    def __init__(self):
        self.counters = defaultdict(int)
        self._lock = threading.Lock()
        
    def increment(self, metric_name:str):
        with self._lock:
            self.counters[metric_name] += 1
        
    def get(self, metric_name:str):
        with self._lock:
            return  self.counters.get(metric_name, 0)
        
        
    def snapshot(self):
        with self._lock:
            return dict(self.counters)
            
        