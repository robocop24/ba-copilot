"""Run the REAL story pipeline end-to-end and report eval + guardrail results.

This is not a unit test — it calls the actual LLM (DeepSeek) for both
generation and judging. Requirements:
    - DEEPSEEK_API_KEY present in BA_Copilot_V3/.env

It exercises:
    1. story_agent (generate -> judge -> quality gate -> retry loop)
    2. an explicit re-judge + gate of the final output, so you can see the
       per-story scores and the final verdict.

Usage:
    python tests/run_story_pipeline.py

NOTE: the explicit re-judge in step 2 makes one extra LLM call per story.
Comment out `show_scores(...)` if you only want the gated output.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "BA_Copilot_V3"))

from agents.story_agent import story_agent
from models.analysis import AnalysisOutput
from utils.prompt_loader import load_prompt

from BA_Copilot_V3.utils.judge_artifacts import judge_artifacts
from evaluation_v3.judges.story_judge import StoryJudge
from guardrails.quality_gate import QualityGate


def build_prompt() -> str:
    """Assemble the same prompt the story node would, using mock input data."""
    analysis = AnalysisOutput(
        actors=["Customer", "Support Agent"],
        modules=["Authentication", "Notification"],
        requirements=[
            "Customer can reset password via a secure email link",
            "Customer receives a confirmation email after reset",
        ],
    )

    story_standard = (
        "As a <role>, I want <goal>, so that <benefit>."
    )

    template = load_prompt("story.txt")
    return template.format(
        analysis=analysis.model_dump_json(indent=2),
        story_standard=story_standard,
    )


def show_scores(stories: list[str]) -> None:
    """Re-judge the final stories and print the gate verdict.

    This duplicates the judge call that story_agent already performed
    internally, purely so the numbers are visible on stdout.
    """
    print("\n=== Eval + Guardrail report ===\n")

    judged = judge_artifacts(StoryJudge(), stories, label="story")

    for i, (total, feedback) in enumerate(zip(judged["per_item"], judged["feedback"]), 1):
        print(f"Story {i}: {total}/{judged['max_score']}")
        print(f"  feedback: {feedback}")

    print(f"\nAverage: {judged['avg']}/{judged['max_score']}")

    verdict = QualityGate().validate({"story_avg_score": judged["avg"]})
    print(f"Gate passed: {verdict.passed}")
    print(f"Recommendation: {verdict.recommendation}")
    if verdict.failures:
        print("Failures:")
        for failure in verdict.failures:
            print(f"  - {failure}")


def main() -> None:
    prompt = build_prompt()

    print("=== Running story_agent (generate -> judge -> gate -> retry) ===\n")
    output = story_agent(prompt=prompt)

    print("=== Stories (final, already gated) ===\n")
    for i, story in enumerate(output.user_stories, 1):
        print(f"{i}. {story}")

    show_scores(output.user_stories)

    print("\nDone. Gate events logged to observability/logs/ba_copilot.log")


if __name__ == "__main__":
    main()
