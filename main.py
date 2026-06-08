"""DateNight Show Matcher — orchestrator + CLI entry point."""
import os

import anthropic
import typer
from agents.insta_reader import read_profile
from agents.interest_profiler import build_interest_profile
from agents.show_matcher import match_shows
from agents.streaming_checker import check_streaming_availability
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()

app = typer.Typer(help="DateNight Show Matcher — AI-powered TV show recommender.")
console = Console()


def _get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print(
            "[red]Error:[/red] ANTHROPIC_API_KEY is not set.\n"
            "Add it to your [bold].env[/bold] file or export it:\n"
            "  [dim]export ANTHROPIC_API_KEY=sk-ant-...[/dim]"
        )
        raise typer.Exit(1)
    return anthropic.Anthropic(api_key=api_key)


def _abort(step: str, err: Exception) -> None:
    console.print(f"\n[red]✗ Step {step} failed:[/red] {err}")
    raise typer.Exit(1)


@app.command("get-show")
def get_show(username: str) -> None:
    """Find the perfect Netflix/HBO show for your date based on her Instagram."""
    client = _get_client()

    header = Panel(
        f"[bold magenta]DateNight Show Matcher[/bold magenta]\n"
        f"[dim]Scanning profile: {username}[/dim]",
        expand=False,
    )
    console.print(header)

    # Step 1: Read Instagram profile
    console.print("\n[cyan]●[/cyan] [bold]Step 1[/bold] Reading Instagram profile...")
    try:
        profile_text = read_profile(username)
    except ValueError as e:
        _abort("1 (InstaReader)", e)
    console.print("  [green]✓[/green] Profile loaded")

    # Step 2: Build psychographic profile
    console.print("[cyan]●[/cyan] [bold]Step 2[/bold] Analyzing interests & vibe...")
    try:
        profile = build_interest_profile(client, profile_text)
    except Exception as e:
        _abort("2 (InterestProfiler)", e)
    console.print(
        f"  [green]✓[/green] Interests: {', '.join(profile['primary_interests'])}"
    )
    console.print(
        f"  [green]✓[/green] Vibe: [italic]{profile['aesthetic_vibe']}[/italic]"
    )

    # Step 3: Match shows to profile
    console.print("[cyan]●[/cyan] [bold]Step 3[/bold] Matching shows to her taste...")
    try:
        candidates = match_shows(client, profile)
    except Exception as e:
        _abort("3 (ShowMatcher)", e)
    titles = [c["title"] for c in candidates["candidates"]]
    console.print(f"  [green]✓[/green] Candidates: {', '.join(titles)}")

    # Step 4: Filter to Netflix/HBO only
    console.print(
        "[cyan]●[/cyan] [bold]Step 4[/bold] Checking Netflix & HBO availability..."
    )
    try:
        result = check_streaming_availability(client, candidates)
    except Exception as e:
        _abort("4 (StreamingChecker)", e)

    if not result["recommendations"]:
        console.print(
            "\n[yellow]No candidates found on Netflix or HBO.[/yellow] "
            "Try a different profile."
        )
        raise typer.Exit(0)

    # Display results
    table = Table(
        title="\n[bold magenta]Tonight's Picks[/bold magenta]",
        show_lines=True,
        border_style="magenta",
    )
    table.add_column("Show", style="bold cyan", min_width=20)
    table.add_column("Platform", style="bold green", min_width=8)
    table.add_column("Why she'll love it", style="white", min_width=35)
    table.add_column("Start with", style="dim", min_width=30)

    for rec in result["recommendations"]:
        table.add_row(
            rec["title"],
            rec["platform"],
            rec["reason"],
            rec.get("conversation_starter", ""),
        )

    console.print(table)
    console.print(
        "\n[dim]Tip: start with the top pick — good luck tonight! 🎬[/dim]\n"
    )


@app.command("list-profiles")
def list_profiles() -> None:
    """Show all available mock Instagram profiles for testing."""
    from data.mock_profiles import AVAILABLE_USERNAMES

    console.print("\n[bold]Available mock profiles:[/bold]")
    for name in AVAILABLE_USERNAMES:
        console.print(f"  [cyan]{name}[/cyan]")
    console.print()


if __name__ == "__main__":
    app()
