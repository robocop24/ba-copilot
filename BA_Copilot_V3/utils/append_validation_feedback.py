def append_validation_feedback(payload, error: str):
    """Append validation error feedback to the payload for retry.

    For string payloads (LLM), appends to the prompt string.
    For dict payloads (agent), appends a user message to the messages list.
    """
    feedback = f"\n\nPREVIOUS RESPONSE INVALID\n{error}\n\nRespond with valid JSON only."

    if isinstance(payload, str):
        return payload + feedback

    if isinstance(payload, dict):
        messages = payload.get("messages", [])
        return {**payload, "messages": [*messages, ("user", feedback)]}

    return payload
