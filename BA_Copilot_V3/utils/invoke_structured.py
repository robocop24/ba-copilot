"""Structured-output invocation with lightweight exception retry.

Why this exists (vs. `invoke_with_validation`):
- `invoke_with_validation` is for agents that return FREE TEXT: it parses JSON,
  validates against a Pydantic model, and retries by feeding the validation
  error back to the LLM.
- Agents created with `create_agent(..., response_format=Model)` return an
  ALREADY-VALIDATED model under `result["structured_response"]` — there is no
  free text to parse, and no "wrong JSON shape" failure to correct.

So the only remaining failure modes are exceptions (API errors, parse errors,
tool errors). We retry those plainly, without any feedback loop.
"""

from observability.logger import log_event
from observability.metrics_registry import metrics


def invoke_structured(agent, payload, max_attempts=2):
    """Invoke a `create_agent(response_format=...)` agent and return its model.

    Args:
        agent: agent produced by `create_agent(..., response_format=Model)`.
        payload: dict payload, e.g. {"messages": [("user", prompt)]}.
        max_attempts: how many times to retry on exception.

    Returns:
        The validated Pydantic model (value of `result["structured_response"]`).

    NOTE for future revision: if `structured_response` is ever a plain dict
    instead of a model (depends on langchain version), wrap it:
    `Model.model_validate(result["structured_response"])`.
    """
    last_error = None
    for attempt in range(max_attempts):
        try:
            result = agent.invoke(payload)
            return result["structured_response"]  # already a validated model
        except Exception as e:  # intentional broad catch: retry ANY API/parse/tool error, then re-raise
            metrics.increment("errors")
            log_event("invoke_structured",
                      f"Error in structured call (attempt {attempt+1}): {e}",
                      level="error")
            last_error = e
    raise last_error