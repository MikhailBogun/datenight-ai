"""Agent #3: Picks top-3 show candidates based on psychographic profile."""
import json
from pathlib import Path

import anthropic

from agents.utils import extract_json

CATALOG_PATH = Path(__file__).parent.parent / "data" / "streaming_catalog.json"

with CATALOG_PATH.open() as f:
    _CATALOG: dict[str, dict] = json.load(f)

SYSTEM_PROMPT = (
    "You are a TV show recommendation expert for romantic date nights.\n"
    "Given a psychographic profile, pick the top 3 shows from the provided "
    "catalog that would genuinely impress her and spark great conversation on "
    "a first date. Prioritize shows that match her personality and date vibe, "
    "not just genre.\n"
    "Output Format: ONLY a valid JSON object, no markdown, no preamble:\n"
    "{\n"
    '  "candidates": [\n'
    '    {\n'
    '      "title": "Exact Show Title",\n'
    '      "reason": "one sentence why she would love it",\n'
    '      "conversation_starter": "one interesting question this show will spark"\n'
    "    }\n"
    "  ]\n"
    "}"
)

_PRE_FILTER_SIZE = 50
_FALLBACK_MIN = 20


def _filter_by_genres(genres: list[str]) -> list[str]:
    """Return top-N titles most relevant to the given genres."""
    genres_lower = {g.lower() for g in genres}
    scored = [
        (title, len(genres_lower & set(data["genres"])))
        for title, data in _CATALOG.items()
        if len(genres_lower & set(data["genres"])) > 0
    ]
    scored.sort(key=lambda x: -x[1])
    result = [t for t, _ in scored[:_PRE_FILTER_SIZE]]
    if len(result) < _FALLBACK_MIN:
        extras = [t for t in _CATALOG if t not in result]
        result.extend(extras[: _FALLBACK_MIN - len(result)])
    return result


def match_shows(client: anthropic.Anthropic, profile: dict) -> dict:
    filtered_titles = _filter_by_genres(profile.get("recommended_genres", []))
    catalog_list = "\n".join(f"- {t}" for t in filtered_titles)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Profile:\n"
                    f"Interests: {', '.join(profile['primary_interests'])}\n"
                    f"Vibe: {profile['aesthetic_vibe']}\n"
                    f"Date vibe: {profile.get('date_vibe', '')}\n"
                    f"Genres: {', '.join(profile['recommended_genres'])}\n\n"
                    f"Available shows (pick ONLY from this list):\n{catalog_list}"
                ),
            }
        ],
    )
    return extract_json(response.content[0].text)
