# datenight-ai

CLI tool that takes an Instagram username, analyzes her profile with Claude AI, and returns TV shows available on **Netflix or HBO** that match her taste.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Anthropic API key

## Setup

```bash
# 1. Install dependencies
uv sync

# 2. Add your API key
cp .env.example .env
# open .env and set ANTHROPIC_API_KEY=sk-ant-...

# Or export directly (no .env file needed)
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Usage

```bash
uv run python main.py get-show @art_girl
uv run python main.py get-show @tech_babe
uv run python main.py get-show @sport_girl
uv run python main.py get-show @fashion_muse
uv run python main.py get-show @kdrama_girl

# list all available profiles
uv run python main.py list-profiles
```

## Mock profiles

Instagram scraping is mocked. Each username maps to a pre-built profile dump (bio, posts, hashtags).

| Username | Type | Edge case |
|---|---|---|
| `@art_girl` | painter, museum-goer, dark academia | — |
| `@tech_babe` | software dev, sci-fi, cyberpunk | — |
| `@sport_girl` | marathon runner, yoga, plant-based | — |
| `@fashion_muse` | vintage fashion, Paris, sustainable style | — |
| `@kdrama_girl` | K-drama & anime only, explicitly rejects western TV | Catalog has zero K-dramas or anime — system finds closest western equivalents and justifies them in her own terms |

## How it works

```
@username → InstaReader → InterestProfiler → ShowMatcher → StreamingChecker → output
              (mock)        (Sonnet)           (Sonnet)      (Haiku + tool use)
```

Four agents in sequence. The last one uses Claude **tool use** (function calling) to verify each show against a local Netflix/HBO catalog before returning results.
