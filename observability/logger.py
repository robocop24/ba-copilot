from datetime import datetime, timezone

from .trace import get_trace_id


def log_event(component, message):
    
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ts} | {get_trace_id()} | {component} | {message}")
    