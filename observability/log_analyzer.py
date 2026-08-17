import json
from collections import defaultdict
from pathlib import Path


class LogAnalyzer:
    
    def __init__(self, log_file=None):
        self.log_file = (log_file or 
                         Path(__file__).parent/"logs"/"ba_copilot.log")
        self.logs = []
        self.load_log()  # auto-load so analysis methods work without a separate call
        
    def load_log(self):
        
        self.logs = []
        
        if not Path(self.log_file).exists():
            return []
            
        with open(self.log_file, "r", encoding="utf-8") as file:
            
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    self.logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
                
        return self.logs
    
    def component_latency_stats(self):
        
        duration_map = defaultdict(list)
        
        for log in self.logs:
            
            component = log.get("component")
            
            duration_ms = log.get("duration_ms")
            
            if(component and duration_ms is not None):
                
                duration_map[component].append(duration_ms)
                
        stats = {}
        for (component, durations) in duration_map.items():
            
            stats[component] = {
                "count": len(durations),
                "avg_ms": round(sum(durations) / len(durations), 2),
                "min_ms": round(min(durations), 2),
                "max_ms": round(max(durations), 2),
            }
            
        return stats
    
    
    def component_log_counts(self):
        """Count log lines per component (activity heatmap), not actual calls."""
        counts = defaultdict(int)
        for log in self.logs:
            
            component = log.get("component")
            
            if component:
                counts[component] += 1
        
        return dict(counts)
     
     
    def workflow_count(self):
        
        workflow_traces = set()
        
        for log in self.logs:
            trace_id = log.get("trace_id")
            if trace_id and trace_id != "-":
                workflow_traces.add(trace_id)
        
        return len(workflow_traces)
    
    
    def slowest_component(self, exclude=("workflow",)):
        """Return (component, stats) with the highest avg_ms, excluding
        the 'workflow' total, which would otherwise always win."""
        stats = self.component_latency_stats()
        
        if not stats:
            return None
        
        candidates = {c: s for c, s in stats.items() if c not in exclude}
        if not candidates:
            return None
        
        return max(candidates.items(), key=lambda item: item[1]["avg_ms"])
    
    # ── Counter helpers (all derived from the log) ─────────────────────
    def _count(self, component=None, level=None, message_prefix=None):
        """Count log records matching optional filters."""
        total = 0
        for log in self.logs:
            if component is not None and log.get("component") != component:
                continue
            if level is not None and log.get("level") != level:
                continue
            if message_prefix is not None and not log.get("message", "").startswith(message_prefix):
                continue
            total += 1
        return total
    
    def error_count(self):
        return self._count(level="error")
    
    def llm_call_count(self):
        return self._count(component="llm")
    
    def mcp_call_count(self):
        return self._count(component="mcp", message_prefix="calling tool")
    
    def cache_hit_count(self):
        return self._count(component="cache", message_prefix="hit")
    
    def cache_miss_count(self):
        return self._count(component="cache", message_prefix="miss")
    
    def rag_query_count(self):
        return self._count(component="rag", message_prefix="retrieve()")