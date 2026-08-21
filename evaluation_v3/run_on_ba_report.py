import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "BA_Copilot_V3"))

from evaluation_v3.ba_report_loader import (
    extract_acceptance_criteria,
    extract_gaps,
    extract_stories,
    load_latest_report,
)
from evaluation_v3.judges.ac_judge import AcceptanceCriteriaJudge
from evaluation_v3.judges.gap_judge import GapAnalysisJudge
from evaluation_v3.judges.story_judge import StoryJudge

# Set to a number (e.g. 3) to cap how many of each artifact are judged.
# None = judge everything (costs one LLM call per item).
LIMIT = None


def _average(scores) -> float:
    return round(sum(scores) / len(scores), 2) if scores else 0.0


def _judge(judge, items, label) -> list[int]:
    scores = []
    for i, item in enumerate(items, 1):
        result = judge.evaluate(item)
        scores.append(result["total"])
        print(f"{label} {i}: {result['total']}/{result['max_score']}")
    return scores


def main():
    report = load_latest_report(BASE_DIR / "BA_Copilot_V3" / "output")

    stories = extract_stories(report)
    acs = extract_acceptance_criteria(report)
    gaps = extract_gaps(report)

    if LIMIT is not None:
        stories = stories[:LIMIT]
        acs = acs[:LIMIT]
        gaps = gaps[:LIMIT]

    print(f"\nFound: {len(stories)} stories, {len(acs)} criteria, {len(gaps)} gaps")
    print("Judging with LLM...\n")

    story_scores = _judge(StoryJudge(), stories, "Story")
    ac_scores = _judge(AcceptanceCriteriaJudge(), acs, "AC")
    gap_scores = _judge(GapAnalysisJudge(), gaps, "Gap")

    summary = {
        "story_avg_score": _average(story_scores),
        "ac_avg_score": _average(ac_scores),
        "gap_avg_score": _average(gap_scores),
    }

    print("\n=== Summary ===\n")
    print(json.dumps(summary, indent=2))

    # Save where evaluation_v4 regression testing expects the "current" scores.
    out = BASE_DIR / "evaluation_v4" / "results" / "current_v1.json"
    out.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
