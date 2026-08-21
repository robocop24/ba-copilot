"""Load a BA Copilot report JSON and extract the three evaluable artifacts."""

import json
from pathlib import Path


def load_latest_report(output_dir) -> dict:
    """Return the most recently written ba_report_*.json in output_dir."""
    output_dir = Path(output_dir)
    files = sorted(
        output_dir.glob("ba_report_*.json"),
        key=lambda p: p.stat().st_mtime,
    )
    if not files:
        raise FileNotFoundError(f"No ba_report_*.json found in {output_dir}")
    return json.loads(files[-1].read_text(encoding="utf-8"))


def load_report(path) -> dict:
    """Return a specific report JSON as a dict."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def extract_stories(report: dict) -> list[str]:
    """User stories from the report."""
    return report.get("stories", {}).get("user_stories", [])


def extract_acceptance_criteria(report: dict) -> list[str]:
    """Return one acceptance-criteria block per story (criteria joined by newlines).

    The BA report nests criteria per story (5 each); joining them gives one
    judgeable block per story instead of judging every criterion separately.
    """
    blocks = []
    for entry in report.get("acceptance_criteria", {}).get("criteria", []):
        criteria = entry.get("acceptance_criteria", [])
        if criteria:
            blocks.append("\n".join(criteria))
    return blocks


def extract_gaps(report: dict) -> list[str]:
    """Gap descriptions from the report."""
    return report.get("gaps", {}).get("gaps", [])
