import json
import re


def extract_json(text: str) -> dict:
    """Extract JSON from Claude responses that may include markdown code blocks."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)
