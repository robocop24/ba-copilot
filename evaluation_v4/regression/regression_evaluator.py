

"""Regression testing for BA Copilot evaluation scores.

Compares a "current" score dict against a "baseline" score dict and flags
metrics that regressed beyond a tolerance threshold.
"""

import json
from pathlib import Path


def load_json(path) -> dict:
    """Load a JSON file into a dict."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, data) -> None:
    """Write a dict to a JSON file (pretty-printed)."""
    Path(path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


class RegressionEvaluator:
    
    def __init__(self, threshold=0.0):
        """threshold: a metric must drop by MORE than this to count as regressed."""
        self.threshold = threshold
    
    def _status(self, delta):
        if delta is None:
            return "missing"
        if delta > self.threshold:
            return "Improved"
        if delta < -self.threshold:
            return "Regressed"
        return "Unchanged"
    
    def compare(self, baseline, current):
        
        # Union of keys, so a metric missing from either side is surfaced
        # instead of crashing with a KeyError.
        metrics = sorted(set(baseline) | set(current))
        
        report = {
            "metrics": {},
            "summary": {
                "improved": 0,
                "regressed": 0,
                "unchanged": 0,
                "missing": 0,
                "status": "PASS",
            },
        }
        
        for metric in metrics:
            
            base = baseline.get(metric)
            curr = current.get(metric)
            
            if base is None or curr is None:
                delta = None
                status = "missing"
            else:
                delta = round(curr - base, 2)
                status = self._status(delta)
            
            if status == "Improved":
                report["summary"]["improved"] += 1
            elif status == "Regressed":
                report["summary"]["regressed"] += 1
            elif status == "missing":
                report["summary"]["missing"] += 1
            else:
                report["summary"]["unchanged"] += 1
            
            report["metrics"][metric] = {
                "baseline": base,
                "current": curr,
                "delta": delta,
                "status": status,
            }
        
        # Overall FAIL if anything regressed or is missing.
        if report["summary"]["regressed"] or report["summary"]["missing"]:
            report["summary"]["status"] = "FAIL"
        
        return report