"""Agent #2: Psychographic profiler — extracts interests from Instagram text."""
import anthropic

from agents.utils import extract_json

SYSTEM_PROMPT = (
    "You are an expert psychographic analyst code-named 'Profiler'.\n"
    "Task: Analyze an Instagram profile (bio, captions, hashtags) to understand "
    "who this person is and what kind of TV show experience would resonate with "
    "her on a first date — something that creates genuine connection and good "
    "conversation, not just genre matching.\n"
    "Output Format: ONLY a valid JSON object, no markdown, no preamble:\n"
    "{\n"
    '  "primary_interests": ["interest1", "interest2", "interest3"],\n'
    '  "aesthetic_vibe": "2-3 sentence description of her personality and style",\n'
    '  "recommended_genres": ["genre1", "genre2"],\n'
    '  "date_vibe": "one sentence on what kind of story would move or impress her"\n'
    "}"
)


def build_interest_profile(client: anthropic.Anthropic, profile_text: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this Instagram profile:\n\n{profile_text}",
            }
        ],
    )
    return extract_json(response.content[0].text)
