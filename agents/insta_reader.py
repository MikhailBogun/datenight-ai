"""Agent #1: Returns mock Instagram profile dump by username."""
from data.mock_profiles import AVAILABLE_USERNAMES, get_profile


def read_profile(username: str) -> str:
    username = username.lower()
    if not username.startswith("@"):
        username = f"@{username}"

    profile = get_profile(username)
    if profile is None:
        available = ", ".join(AVAILABLE_USERNAMES)
        raise ValueError(
            f"Profile '{username}' not found in mock data. "
            f"Available: {available}"
        )
    return profile
