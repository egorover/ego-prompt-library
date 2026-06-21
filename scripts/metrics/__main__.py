#!/usr/bin/env python3
"""Allow running metrics as a module: python -m scripts.metrics"""

from pathlib import Path

from rich.console import Console

from ..logger import get_logger
from .collector import collect_metrics
from ..shared import discover_prompts

logger = get_logger(__name__)
console = Console()


def main() -> None:
    """Collect and display metrics for all prompts."""
    library_root = Path(__file__).parent.parent.parent
    prompts = discover_prompts(library_root)

    if not prompts:
        console.print("[WARN] No prompts found.", style="yellow")
        return

    metrics_list = [collect_metrics(p) for p in prompts]

    console.rule(f"[bold]Metrics — {len(metrics_list)} prompt(s)[/bold]")

    for m in metrics_list:
        console.print(f"\n[bold blue]METRICS[/bold blue] {m.name} ({m.version}, {m.status})")
        console.print(f"   Usage: {m.usage_count} | Tests: {m.test_pass_rate}% ({m.test_passed}/{m.test_total})")
        console.print(f"   Latency P50: {m.latency_p50}s | Quality: {m.quality_avg if m.quality_count > 0 else '—'}")
        console.print(f"   Changes this month: {m.changes_this_month}")

    console.print("")


if __name__ == "__main__":
    main()
