from contextvars import ContextVar

current_trace_id = ContextVar("trace_id", default=None)