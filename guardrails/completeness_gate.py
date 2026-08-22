"""Deterministic structural checks — cheap and run BEFORE the LLM judge.

Complementary to `QualityGate` (which scores subjective quality with an LLM
judge). This gate only asks "is anything missing / structurally broken?", so
an empty or malformed artifact fails fast without paying for an LLM call.
"""

import re

from guardrails.models.guardrail_result import GuardrailResult

# "As a <role>..." or "As an <role>..." at the start (leading whitespace ok).
_STORY_HEADER = re.compile(r"^\s*As\s+an?\s+\S", re.IGNORECASE)


class CompletenessGate:
    """Structural checks for story, acceptance-criteria, and gap outputs."""

    def validate_story(self, story_output) -> GuardrailResult:
        failures = []

        stories = getattr(story_output, "user_stories", None)

        if not stories:
            return GuardrailResult(
                passed=False,
                failures=["No user stories generated"],
                recommendation="REGENERATE",
            )

        for index, story in enumerate(stories, 1):
            text = story.strip() if isinstance(story, str) else ""

            if not text:
                failures.append(f"Story {index} is empty")
                continue

            if not _STORY_HEADER.match(text):
                failures.append(f"Story {index} does not start with 'As a(n)'")
            if "I want" not in text:
                failures.append(f"Story {index} is missing 'I want'")
            if "so that" not in text.lower():
                failures.append(f"Story {index} is missing 'so that'")

        return self._result(failures)

    def validate_acceptance(self, acceptance_output, expected_stories: int | None = None) -> GuardrailResult:
        failures = []

        criteria = getattr(acceptance_output, "criteria", None)

        if not criteria:
            return GuardrailResult(
                passed=False,
                failures=["No acceptance criteria generated"],
                recommendation="REGENERATE",
            )

        seen_indexes = set()

        for index, entry in enumerate(criteria, 1):
            story_index = getattr(entry, "story_index", None)
            summary = getattr(entry, "story_summary", "") or ""
            acs = getattr(entry, "acceptance_criteria", None) or []

            if story_index is None:
                failures.append(f"Criteria {index} is missing story_index")
            elif story_index in seen_indexes:
                failures.append(f"Criteria {index} duplicates story_index {story_index}")
            else:
                seen_indexes.add(story_index)

            if not summary.strip():
                failures.append(f"Criteria {index} has an empty story_summary")

            non_empty = [a for a in acs if isinstance(a, str) and a.strip()]
            if len(non_empty) < 3:
                failures.append(f"Criteria {index} has fewer than 3 acceptance criteria")
            elif len(non_empty) > 5:
                failures.append(f"Criteria {index} has more than 5 acceptance criteria")

        if expected_stories is not None:
            expected_indexes = set(range(expected_stories))
            missing = sorted(expected_indexes - seen_indexes)
            extra = sorted(seen_indexes - expected_indexes)
            for story_idx in missing:
                failures.append(f"Missing acceptance criteria for story_index {story_idx}")
            for story_idx in extra:
                failures.append(f"Unexpected story_index {story_idx} in acceptance criteria")

        return self._result(failures)

    def validate_gaps(self, gap_output) -> GuardrailResult:
        failures = []

        gaps_found = getattr(gap_output, "gaps_found", None)
        gaps = getattr(gap_output, "gaps", None) or []

        if gaps_found is True and not gaps:
            failures.append("gaps_found is True but no gaps are listed")
        if gaps_found is False and gaps:
            failures.append("gaps_found is False but gaps are listed")

        for index, gap in enumerate(gaps, 1):
            if not (isinstance(gap, str) and gap.strip()):
                failures.append(f"Gap {index} is empty")

        return self._result(failures)

    @staticmethod
    def _result(failures: list[str]) -> GuardrailResult:
        passed = len(failures) == 0
        return GuardrailResult(
            passed=passed,
            failures=failures,
            recommendation="CONTINUE" if passed else "REGENERATE",
        )
