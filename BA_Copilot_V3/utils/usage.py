def _extract_usage(response) -> dict:
    """Return token usage from an AIMessage (stateless) or agent result dict (ReAct)."""
    if hasattr(response, "usage_metadata"):
        u = response.usage_metadata or {}
        return {
            "prompt_tokens": u.get("input_tokens"),
            "completion_tokens": u.get("output_tokens"),
            "total_tokens": u.get("total_tokens"),
        }

    if isinstance(response, dict):
        messages = response.get("messages", [])
        prompt = completion = total = 0
        for msg in messages:
            u = getattr(msg, "usage_metadata", None) or {}
            prompt += u.get("input_tokens") or 0
            completion += u.get("output_tokens") or 0
            total += u.get("total_tokens") or 0
        if messages:
            return {"prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": total}
    return {}