import json
import re

def parse_llm_json(response_text: str, default: dict | None = None) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    if default is None:
        default = {}

    text = response_text.strip()

    # Try to extract from ```json ... ``` block
    match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    # Also try to find the first { ... } if still failing
    if not text.startswith('{'):
        brace_match = re.search(r'\{.*\}', text, re.DOTALL)
        if brace_match:
            text = brace_match.group(0)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"⚠️ Failed to parse JSON. Raw: {response_text[:200]}...")
        return default