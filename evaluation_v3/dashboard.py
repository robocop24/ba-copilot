import sys
from pathlib import Path

# Add the project root (for `evaluation_v3`) and BA_Copilot_V3 (for its
# top-level `llm`, `utils`, `models` packages) to sys.path.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "BA_Copilot_V3"))

from evaluation_v3.judges.ac_judge import AcceptanceCriteriaJudge
from evaluation_v3.judges.gap_judge import GapAnalysisJudge
from evaluation_v3.judges.story_judge import StoryJudge

story = """
As a user, I want to login, so that I can access my account.
"""

acceptance_criteria = """
Given a registered user, when valid credentials are entered,
then access should be granted.
"""

gap_analysis = """
Assumption: Users already exist.
Dependency: Email service must be available.
Risk: OTP delivery may fail.
Clarification: Password policy is not defined.
"""


def _print_report(title: str, result: dict):
    print(f"\n=== {title} ===\n")
    print(f"Total Score: {result['total']}/{result['max_score']}")
    print(result["score"].model_dump_json(indent=2))


def main():

    _print_report("Story Judge Report", StoryJudge().evaluate(story))
    _print_report("Acceptance Criteria Judge Report",
                  AcceptanceCriteriaJudge().evaluate(acceptance_criteria))
    _print_report("Gap Analysis Judge Report",
                  GapAnalysisJudge().evaluate(gap_analysis))


if __name__ == "__main__":
    main()