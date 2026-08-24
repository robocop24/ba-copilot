"""Score a list of generated artifacts with an evaluation_v3 judge.

This is the online twin of the offline batch path in
`evaluation_v3/run_on_ba_report.py`. It judges each item, keeps the per-item
feedback (so a regeneration retry can use it), and returns the average score
that the quality gate consumes.
"""

from observability.logger import log_event


def judge_artifacts(judge, items: list[str], label: str = "artifact", max_items: int | None = 5) -> dict:
    """Judge a (possibly sampled) set of items and return averages + feedback.

    Args:
        judge: an evaluation_v3 judge instance with
            `evaluate(item) -> {"total": int, "max_score": int, "score": BaseModel}`,
            where `score` has a `feedback` field.
        items: list of artifact strings to score.
        label: human-readable artifact name used in logs.
        max_items: cap on how many items are judged (evenly sampled) to keep
            LLM cost bounded. Pass None to judge every item.

    Returns:
        {
            "avg": float,            # average total score across judged items
            "max_score": int,        # judge's max score (e.g. 20)
            "per_item": [int],       # total score per judged item
            "feedback": [str],       # judge feedback per judged item
            "total_items": int,      # number of items available
            "sampled_items": int,    # number of items actually judged
        }
    """
    sample = items
    if max_items is not None and len(items) > max_items:
        step = len(items) / max_items
        indexes = sorted({min(int(i * step), len(items) - 1) for i in range(max_items)})
        sample = [items[i] for i in indexes]

    scores = []
    feedback = []
    max_score = 0

    for index, item in enumerate(sample, 1):
        result = judge.evaluate(item)

        total = result["total"]
        max_score = result.get("max_score", max_score)

        scores.append(total)

        score = result.get("score")
        if score is not None and hasattr(score, "feedback"):
            feedback.append(score.feedback)

        log_event(
            "judge",
            f"{label} {index}/{len(sample)} scored {total}/{max_score}",
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
        "total_items": len(items),
        "sampled_items": len(sample),
    }
