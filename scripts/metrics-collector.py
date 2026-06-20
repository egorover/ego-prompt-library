#!/usr/bin/env python3
"""
Metrics Collector — CLI entry point для сбора метрик промптов.

Использует модули: metrics.collector, metrics.parsers, metrics.dashboard.

Использование:
    python scripts/metrics-collector.py                     # собрать для всех промптов
    python scripts/metrics-collector.py prompts/python-architect  # конкретный
    python scripts/metrics-collector.py --json              # JSON-вывод
    python scripts/metrics-collector.py --dashboard         # обновить dashboard
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from shared import discover_prompts
from metrics import collect_metrics, update_dashboard


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect metrics for prompt library")
    parser.add_argument("target", nargs="?", default=".", help="Path to prompt directory or library root")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--dashboard", action="store_true", help="Update dashboard files")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    is_prompt_dir = "prompts" in str(target) and target.is_dir()
    library_root = target.parent.parent if is_prompt_dir else target

    prompts = [target] if is_prompt_dir else discover_prompts(library_root)

    if not prompts:
        print("[WARN] No prompts found.")
        sys.exit(0)

    metrics_list = [collect_metrics(p) for p in prompts]

    if args.dashboard:
        for m in metrics_list:
            prompt_dir = library_root / "prompts" / m.name
            update_dashboard(m, prompt_dir)
        print(f"[OK] Updated dashboards for {len(metrics_list)} prompt(s)")

    if args.json:
        output = {
            "collected_at": date.today().isoformat(),
            "prompts": [m.to_dict() for m in metrics_list],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    print(f"\n{'=' * 60}")
    print(f"Metrics Collection — {len(metrics_list)} prompt(s)")
    print(f"{'=' * 60}")

    for m in metrics_list:
        print(f"\n[METRICS] {m.name} ({m.version}, {m.status})")
        print(f"   Usage: {m.usage_count} | Tests: {m.test_pass_rate}% ({m.test_passed}/{m.test_total})")
        print(f"   Latency P50: {m.latency_p50}s | Quality: {m.quality_avg if m.quality_count > 0 else '—'}")
        print(f"   Changes this month: {m.changes_this_month}")

    print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    main()
