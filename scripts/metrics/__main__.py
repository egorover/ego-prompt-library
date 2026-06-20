#!/usr/bin/env python3
"""Allow running metrics as a module: python -m scripts.metrics"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from metrics.collector import collect_metrics
from shared import discover_prompts


def main() -> None:
    """Collect and display metrics for all prompts."""
    library_root = scripts_dir.parent
    prompts = discover_prompts(library_root)

    if not prompts:
        print("[WARN] No prompts found.")
        return

    metrics_list = [collect_metrics(p) for p in prompts]

    print(f"\n{'=' * 60}")
    print(f"Metrics — {len(metrics_list)} prompt(s)")
    print(f"{'=' * 60}")

    for m in metrics_list:
        print(f"\n[METRICS] {m.name} ({m.version}, {m.status})")
        print(f"   Usage: {m.usage_count} | Tests: {m.test_pass_rate}% ({m.test_passed}/{m.test_total})")
        print(f"   Latency P50: {m.latency_p50}s | Quality: {m.quality_avg if m.quality_count > 0 else '—'}")
        print(f"   Changes this month: {m.changes_this_month}")

    print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    main()
