import json
from datetime import datetime, timezone
from pathlib import Path

from .trace import get_trace_id

LOG_FILE = Path(__file__).resolve().parent / "logs" / "ba_copilot.log"

LOG_FILE.parent.mkdir(exist_ok=True)

def log_event(component, message, duration_ms=None, level="info"):
    
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_line = {
        "time": ts,
        "trace_id": get_trace_id() or "-",
        "level": level,
        "component": component,
        "message": message,
    }
    
    if duration_ms is not None:          # only include it when someone measured it
        log_line["duration_ms"] = duration_ms
    
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_line) + "\n")
    