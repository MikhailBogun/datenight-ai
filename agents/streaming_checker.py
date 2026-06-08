"""Agent #4: Checks show availability on Netflix/HBO using Claude tool use."""
import json
from pathlib import Path

import anthropic

from agents.utils import extract_json

CATALOG_PATH = Path(__file__).parent.parent / "data" / "streaming_catalog.json"

with CATALOG_PATH.open() as f:
    CATALOG: dict[str, dict] = json.load(f)

ALLOWED_PLATFORMS = {"Netflix", "HBO"}

CHECK_TOOL = {
    "name": "check_shows_availability",
    "description": (
        "Check which TV shows are available on Netflix or HBO (subscribed platforms). "
        "Amazon Prime and other platforms are NOT available — exclude them. "
        "Returns availability and platform for each title."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "titles": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of TV show titles to check.",
            }
        },
        "required": ["titles"],
    },
}

SYSTEM_PROMPT = (
    "You are a streaming availability checker.\n"
    "You will receive a list of TV show candidates. Call the "
    "check_shows_availability tool ONCE with all titles at the same time.\n"
    "After receiving the results, return ONLY the shows that ARE available, "
    "preserving the reason and conversation_starter from the input.\n"
    "If zero shows are available, return {\"recommendations\": []}.\n"
    "Output Format: valid JSON only, no markdown, no preamble:\n"
    "{\n"
    '  "recommendations": [\n'
    '    {\n'
    '      "title": "Show Title",\n'
    '      "platform": "Netflix or HBO",\n'
    '      "reason": "why she would love it",\n'
    '      "conversation_starter": "question this show will spark"\n'
    "    }\n"
    "  ]\n"
    "}"
)


def _run_tool(titles: list[str]) -> list[dict]:
    results = []
    for title in titles:
        title_lower = title.lower()
        entry = next(
            (data | {"title": t} for t, data in CATALOG.items()
             if t.lower() == title_lower),
            None,
        )
        if entry and entry["platform"] in ALLOWED_PLATFORMS:
            results.append({
                "title": entry["title"],
                "platform": entry["platform"],
                "available": True,
            })
        else:
            platform_note = entry["platform"] if entry else "not in catalog"
            results.append({
                "title": title,
                "available": False,
                "reason": f"found on {platform_note} — not a subscribed platform",
            })
    return results


def check_streaming_availability(
    client: anthropic.Anthropic, candidates: dict
) -> dict:
    candidates_text = "\n".join(
        f"- {c['title']}: {c['reason']} | "
        f"Conversation starter: {c.get('conversation_starter', '')}"
        for c in candidates["candidates"]
    )

    messages = [
        {
            "role": "user",
            "content": (
                f"Check availability for these shows:\n{candidates_text}\n\n"
                "Call the tool once with all titles, then return only "
                "those available on Netflix or HBO."
            ),
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=[CHECK_TOOL],
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return extract_json(block.text)
            return {"recommendations": []}

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    results = _run_tool(block.input["titles"])
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(results),
                        }
                    )

            messages.append({"role": "user", "content": tool_results})
