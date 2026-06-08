"""Agent #2: Psychographic profiler — extracts interests from Instagram text."""
import anthropic

from agents.utils import extract_json

SYSTEM_PROMPT = (
    "Context: You are an expert psychographic analyst code-named 'Profiler'.\n"
    "Task: Analyze the provided text dump from an Instagram profile "
    "(bio, text captions, hashtags). Extract core interests, preferred "
    "lifestyle aesthetic, and general behavioral vibe.\n"
    "Output Format: You MUST output ONLY a valid JSON object:\n"
    "{\n"
    '  "primary_interests": ["interest1", "interest2", "interest3"],\n'
    '  "aesthetic_vibe": "short description of style/vibe",\n'
    '  "recommended_genres": ["genre1", "genre2"]\n'
    "}\n"
    "Strict Rule: Do not include any conversational filler, markdown "
    "formatting blocks (except 'json'), or preambles. Output pure JSON only."
)


def build_interest_profile(client: anthropic.Anthropic, profile_text: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this Instagram profile:\n\n{profile_text}",
            }
        ],
    )
    return extract_json(response.content[0].text)
