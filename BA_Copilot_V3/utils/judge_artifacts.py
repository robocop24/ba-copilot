"""Score a list of generated artifacts with an evaluation_v3 judge.

This is the online twin of the offline batch path in
`evaluation_v3/run_on_ba_report.py`. It judges each item, keeps the per-item
feedback (so a regeneration retry can use it), and returns the average score
that the quality gate consumes.
"""

from observability.logger import log_event


def judge_artifacts(judge, items: list[str], label: str = "artifact") -> dict:
    """Judge every item and return averages plus feedback.

    Args:
        judge: an evaluation_v3 judge instance with
            `evaluate(item) -> {"total": int, "max_score": int, "score": BaseModel}`,
            where `score` has a `feedback` field.
        items: list of artifact strings to score.
        label: human-readable artifact name used in logs.

    Returns:
        {
            "avg": float,          # average total score across items
            "max_score": int,      # judge's max score (e.g. 20)
            "per_item": [int],     # total score per item
            "feedback": [str],     # judge feedback per item
        }
    """
    scores = []
    feedback = []
    max_score = 0

    for index, item in enumerate(items, 1):
        result = judge.evaluate(item)

        total = result["total"]
        max_score = result.get("max_score", max_score)

        scores.append(total)

        score = result.get("score")
        if score is not None and hasattr(score, "feedback"):
            feedback.append(score.feedback)

        log_event(
            "judge",
            f"{label} {index} scored {total}/{max_score}",
            label=label,
            index=index,
            total=total,
            max_score=max_score,
        )

    avg = round(sum(scores) / len(scores), 2) if scores else 0.0

    return {
        "avg": avg,
        "max_score": max_score,
        "per_item": scores,
        "feedback": feedback,
    }
