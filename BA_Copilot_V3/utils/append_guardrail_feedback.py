"""Append quality-gate failures + judge feedback to a payload for regeneration.

Sibling of `append_validation_feedback`, but for the quality gate instead of a
Pydantic validation error. Same payload handling: string for plain LLMs, dict
(for agent results) appends a user message.
"""


def append_guardrail_feedback(payload, failures: list[str], feedback: str = "") -> str | dict:
    """Append gate failures and judge feedback to the prompt for a retry.

    Args:
        payload: str prompt (LLM) or {"messages": [...]} dict (agent).
        failures: list of gate failure messages, e.g. ["Story score below threshold"].
        feedback: optional joined judge feedback text.

    Returns:
        A new payload with the feedback appended. The original payload is not mutated.
    """
    lines = [
        "",
        "PREVIOUS RESPONSE FAILED VALIDATION",
        "Failures: " + ("; ".join(failures) if failures else "none"),
    ]
    if feedback:
        lines.append("Judge feedback: " + feedback)
    lines.append("Regenerate the output, addressing every issue above. Return valid output only.")

    text = "\n".join(lines)

    if isinstance(payload, str):
        return payload + text

    if isinstance(payload, dict):
        messages = payload.get("messages", [])
        return {**payload, "messages": [*messages, ("user", text)]}

    return payload
