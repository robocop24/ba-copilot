from collections import defaultdict


class LatencyTracker:
    
    def __init__(self):
        self.latencies = defaultdict(list)