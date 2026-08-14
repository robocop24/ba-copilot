from datetime import datetime, timezone
from pathlib import Path

from .trace import get_trace_id

LOG_FILE = Path(__file__).resolve().parent / "logs" / "ba_copilot.log"

LOG_FILE.parent.mkdir(exist_ok=True)

def log_event(component, message):
    
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{ts} | {get_trace_id() or '-'} | {component} | {message}"
    
    # print(log_line)
    
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_line + "\n")
    