#!/usr/bin/env python3
"""Allow running metrics as a module: python -m scripts.metrics"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from rich.console import Console

from ._imports import discover_prompts, get_logger
from .collector import collect_metrics
from .dashboard import update_dashboard

logger = get_logger(__name__)
console = Console()


def _resolve_library_root(target: Path) -> Path:
    """Resolve library root from target path."""
    if target.name == "prompts" and target.is_dir():
        return target.parent
    if "prompts" in target.parts and target.is_dir():
        return target.parent.parent
    return target


def main() -> None:
    """Collect and display metrics for prompt library."""
    from config import init

    init()

    parser = argparse.ArgumentParser(description="Collect metrics for prompt library")
    parser.add_argument("target", nargs="?", default=".", help="Path to prompt directory or library root")
    parser.add_argument("--all", action="store_true", help="Collect metrics for all prompts in library")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--dashboard", action="store_true", help="Update dashboard files")
    args = parser.parse_args()

    library_root = Path(__file__).parent.parent.parent

    if args.all:
        prompts = discover_prompts(library_root)
    else:
        target = Path(args.target).resolve()
        is_prompt_dir = target.name != "prompts" and "prompts" in target.parts and target.is_dir()
        if is_prompt_dir:
            prompts = [target]
            library_root = _resolve_library_root(target)
        elif target.name == "prompts" and target.is_dir():
            library_root = target.parent
            prompts = discover_prompts(library_root)
        else:
            library_root = target if (target / "prompts").is_dir() else library_root
            prompts = discover_prompts(library_root)

    if not prompts:
        console.print("[WARN] No prompts found.", style="yellow")
        sys.exit(0)

    metrics_list = [collect_metrics(p) for p in prompts]

    if args.dashboard:
        for m in metrics_list:
            prompt_dir = library_root / "prompts" / m.name
            update_dashboard(m, prompt_dir)
        console.print(f"[OK] Updated dashboards for {len(metrics_list)} prompt(s)", style="green")

    if args.json:
        output = {
            "collected_at": date.today().isoformat(),
            "prompts": [m.to_dict() for m in metrics_list],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    console.rule(f"[bold]Metrics — {len(metrics_list)} prompt(s)[/bold]")

    for m in metrics_list:
        console.print(f"\n[bold blue]METRICS[/bold blue] {m.name} ({m.version}, {m.status})")
        console.print(f"   Usage: {m.usage_count} | Tests: {m.test_pass_rate}% ({m.test_passed}/{m.test_total})")
        quality = m.quality_avg if m.quality_count > 0 else "—"
        console.print(f"   Latency P50: {m.latency_p50}s | Quality: {quality}")
        console.print(f"   Changes this month: {m.changes_this_month}")

    console.print("")


if __name__ == "__main__":
    main()
