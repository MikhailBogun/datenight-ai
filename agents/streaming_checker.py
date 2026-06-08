"""Agent #4: Checks show availability on Netflix/HBO using Claude tool use."""
import json
from pathlib import Path

import anthropic

CATALOG_PATH = Path(__file__).parent.parent / "data" / "streaming_catalog.json"

with CATALOG_PATH.open() as f:
    CATALOG: dict[str, list[str]] = json.load(f)

CHECK_TOOL = {
    "name": "check_show_availability",
    "description": (
        "Check if a TV show is available on Netflix or HBO. "
        "Returns the platform name if available, or null if not found."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The exact title of the TV show to check.",
            }
        },
        "required": ["title"],
    },
}

SYSTEM_PROMPT = """You are a streaming availability checker.
You will receive a list of TV show candidates. For EACH show, you MUST call the \
check_show_availability tool to verify if it is on Netflix or HBO.
After checking all shows, return ONLY the ones that ARE available, with their platform.
Output Format: valid JSON only:
{
  "recommendations": [
    {"title": "Show Title", "platform": "Netflix or HBO", "reason": "why she'd love it"}
  ]
}
If no shows are available, return {"recommendations": []}.
No markdown, no preamble. JSON only."""


def _run_tool(title: str) -> dict:
    for platform, shows in CATALOG.items():
        for show in shows:
            if show.lower() == title.lower():
                return {"available": True, "platform": platform, "title": show}
    return {"available": False, "platform": None, "title": title}


def check_streaming_availability(
    client: anthropic.Anthropic, candidates: dict
) -> dict:
    candidates_text = "\n".join(
        f"- {c['title']}: {c['reason']}" for c in candidates["candidates"]
    )

    messages = [
        {
            "role": "user",
            "content": (
                f"Check availability for these shows:\n{candidates_text}\n\n"
                "Check each one and return only those available on Netflix or HBO."
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
                    from agents.utils import extract_json

                    return extract_json(block.text)
            return {"recommendations": []}

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = _run_tool(block.input["title"])
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        }
                    )

            messages.append({"role": "user", "content": tool_results})
