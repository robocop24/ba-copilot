import uuid

from .context import current_trace_id


def generate_trace_id() -> str:
    return uuid.uuid4().hex

def set_trace_id(trace_id: str) -> None:
    current_trace_id.set(trace_id)

def get_trace_id() -> str:
    return current_trace_id.get()