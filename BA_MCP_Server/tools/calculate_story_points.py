from observability.logger import log_event
from observability.trace import generate_trace_id, set_trace_id


def calculate_story_points(complexity: str, trace_id: str = "") -> int:
    """Calculate story points based on complexity."""
    
    set_trace_id(trace_id or generate_trace_id())
    log_event("mcp", f"calculate_story_points called complexity='{complexity}'")

    try:
        complexity_mapping = {
            "low": 2,
            "medium": 5,
            "high": 8,
            "very_high": 13,
        }
        complexity = complexity.lower().strip()
        result = complexity_mapping[complexity]
        log_event("mcp", f"calculate_story_points completed points={result}")
        return result
    
    except KeyError:
        
        log_event("mcp", f"calculate_story_points failed: invalid complexity '{complexity}'")
        raise ValueError(f"Invalid complexity '{complexity}'. Use: low, medium, high, very_high")