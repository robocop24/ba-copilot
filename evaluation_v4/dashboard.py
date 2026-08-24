import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation_v4.regression.regression_evaluator import (
    RegressionEvaluator,
    load_json,
    save_json,
)

BASE_DIR = Path(__file__).resolve().parent


def main():
    print("\n=== Regression Report ===\n")
    
    baseline = load_json(BASE_DIR / "results" / "baseline_v1.json")
    current = load_json(BASE_DIR / "results" / "current_v1.json")
    
    evaluator = RegressionEvaluator(threshold=0.5)
    report = evaluator.compare(baseline, current)
    
    summary = report["summary"]
    
    print(f"Overall status: {summary['status']}")
    print(f"Improved: {summary['improved']} | Regressed: {summary['regressed']} | "
          f"Unchanged: {summary['unchanged']} | Missing: {summary['missing']}\n")
    
    for metric, data in report["metrics"].items():
        
        print(f"{metric}")
        print(f"  baseline: {data['baseline']}")
        print(f"  current:  {data['current']}")
        print(f"  delta:    {data['delta']}")
        print(f"  status:   {data['status']}")
        print("-" * 40)

    pv = report.get("prompt_versions", {})
    entries = pv.get("entries", {})
    if entries:
        print("\nPrompt Versions")
        print("-" * 40)
        for key, data in entries.items():
            marker = "CHANGED" if data["changed"] else "same"
            print(f"{key}: {data['baseline']} -> {data['current']} ({marker})")
        print(f"\n{pv.get('changed', 0)} prompt(s) changed")
        print(f"baseline version: {baseline.get('version', '?')} | current version: {current.get('version', '?')}")
    
    save_json(BASE_DIR / "results" / "regression_report.json", report)
    print("Report saved to results/regression_report.json")


if __name__ == "__main__":
    main()