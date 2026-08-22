import sys
from pathlib import Path

# Make the workspace root importable before any local imports.
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from evaluation_v4.regression.regression_evaluator import load_json
from guardrails.quality_gate import QualityGate


def main():
    current = load_json(ROOT_DIR / "evaluation_v4" / "results" / "current_v1.json")

    quality_gate = QualityGate()
    result = quality_gate.validate(current)

    print("\n=== Quality Gate ===\n")
    print(f"Passed: {result.passed}")
    print(f"Recommendation: {result.recommendation}")
    if result.failures:
        print("Failures:")
        for failure in result.failures:
            print(f"  - {failure}")
    else:
        print("No failures.")


if __name__ == "__main__":
    main()