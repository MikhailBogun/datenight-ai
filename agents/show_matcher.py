"""Agent #3: Picks top-3 show candidates based on psychographic profile."""
import json
from pathlib import Path

import anthropic

from agents.utils import extract_json

CATALOG_PATH = Path(__file__).parent.parent / "data" / "streaming_catalog.json"

with CATALOG_PATH.open() as f:
    _CATALOG: dict[str, list[str]] = json.load(f)

ALL_AVAILABLE = [
    title for titles in _CATALOG.values() for title in titles
]

SYSTEM_PROMPT = (
    "You are a TV show recommendation expert for romantic date nights.\n"
    "Given a psychographic profile of a person, suggest the top 3 TV shows "
    "that would impress her — something she would genuinely enjoy and that "
    "creates good conversation.\n"
    "IMPORTANT: You MUST only pick shows from the provided available catalog.\n"
    "Output Format: ONLY a valid JSON object, no markdown, no preamble:\n"
    "{\n"
    '  "candidates": [\n'
    '    {"title": "Exact Show Title", "reason": "one sentence why she\'d love it"},\n'
    '    {"title": "Exact Show Title", "reason": "one sentence why she\'d love it"},\n'
    '    {"title": "Exact Show Title", "reason": "one sentence why she\'d love it"}\n'
    "  ]\n"
    "}"
)


def match_shows(client: anthropic.Anthropic, profile: dict) -> dict:
    catalog_list = "\n".join(f"- {entry}" for entry in ALL_AVAILABLE)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Psychographic profile:\n"
                    f"Interests: {', '.join(profile['primary_interests'])}\n"
                    f"Vibe: {profile['aesthetic_vibe']}\n"
                    f"Preferred genres: {', '.join(profile['recommended_genres'])}\n\n"
                    f"Available catalog (pick ONLY from these):\n{catalog_list}"
                ),
            }
        ],
    )
    return extract_json(response.content[0].text)
