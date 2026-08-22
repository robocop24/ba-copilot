from llm.provider_factory import ProviderFactory
from models.acceptance import AcceptanceOutput
from utils.append_guardrail_feedback import append_guardrail_feedback
from utils.invoke_with_validation import invoke_with_validation
from utils.judge_artifacts import judge_artifacts

from evaluation_v3.judges.ac_judge import AcceptanceCriteriaJudge
from guardrails.completeness_gate import CompletenessGate
from guardrails.quality_gate import QualityGate
from observability.logger import log_event


def acceptance_agent(prompt: str, max_attempts: int = 2, expected_stories: int | None = None) -> AcceptanceOutput:

    llm = ProviderFactory.get_llm()
    last_output = None

    for attempt in range(max_attempts):
        output = invoke_with_validation(
            invokable=llm,
            payload=prompt,
            model_class=AcceptanceOutput
        )

        completeness = CompletenessGate().validate_acceptance(output, expected_stories=expected_stories)
        if not completeness.passed:
            last_output = output
            log_event(
                "COMPLETENESS_GATE",
                f"failed on attempt {attempt + 1}: {completeness.failures}",
                level="warn",
            )
            prompt = append_guardrail_feedback(prompt, completeness.failures)
            continue

        # One judgeable block per story (criteria joined by newlines),
        # mirroring evaluation_v3.ba_report_loader.extract_acceptance_criteria.
        items = ["\n".join(entry.acceptance_criteria) for entry in output.criteria]

        judged = judge_artifacts(AcceptanceCriteriaJudge(), items, label="ac")
        gate = QualityGate().validate({"ac_avg_score": judged["avg"]})

        if gate.passed:
            log_event("AC_GATE", f"passed on attempt {attempt + 1}", avg=judged["avg"])
            return output

        last_output = output
        log_event(
            "AC_GATE",
            f"failed on attempt {attempt + 1}: {gate.failures}",
            avg=judged["avg"],
            level="warn",
        )
        prompt = append_guardrail_feedback(
            prompt,
            gate.failures,
            "; ".join(judged["feedback"]),
        )

    log_event("AC_GATE", f"fail-open after {max_attempts} attempts", level="warn")
    return last_output