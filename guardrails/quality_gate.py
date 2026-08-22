from guardrails.models.guardrail_result import GuardrailResult


class QualityGate:
    
    STORY_THRESHOLD = 15
    AC_THRESHOLD = 15
    GAP_THRESHOLD = 15

    # Only metrics present in the evaluation dict are checked, so the same
    # gate works for a full report (all three keys) or a single artifact
    # (e.g. just "story_avg_score") during the inline workflow.
    _RULES = {
        "story_avg_score": (STORY_THRESHOLD, "Story score below threshold"),
        "ac_avg_score": (AC_THRESHOLD, "Acceptance criteria score below threshold"),
        "gap_avg_score": (GAP_THRESHOLD, "Gap analysis score below threshold"),
    }

    def validate(self, evaluation:dict):
        failures = []

        for metric, (threshold, message) in self._RULES.items():
            if metric in evaluation and evaluation[metric] < threshold:
                failures.append(message)

        passed = len(failures) == 0

        return GuardrailResult(
            passed=passed,
            failures=failures,
            recommendation="CONTINUE" if passed else "REGENERATE",
        )