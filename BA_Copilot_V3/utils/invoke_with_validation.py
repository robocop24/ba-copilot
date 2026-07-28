from pydantic import ValidationError
from utils.json_parser import parse_llm_json
from utils.append_validation_feedback import append_validation_feedback


def _extract_text(response) -> str:
    """Extract text content from either an AIMessage (LLM) or agent result dict."""
    if hasattr(response, "content"):
        return response.content or ""
    if isinstance(response, dict):
        messages = response.get("messages", [])
        if messages:
            return messages[-1].content or ""
    return str(response)


def invoke_with_validation(
    invokable,
    payload,
    model_class,
    max_attempts=2
):

    last_error = None

    for _ in range(max_attempts):
        try:

            response = invokable.invoke(payload)

            text = _extract_text(response)
            json_dict = parse_llm_json(text)

            return model_class.model_validate(json_dict)

        except (ValidationError, ValueError) as e:

            last_error = e

            payload = append_validation_feedback(payload, e)

    raise last_error