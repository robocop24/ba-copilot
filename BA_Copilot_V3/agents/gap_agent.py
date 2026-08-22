from llm.provider_factory import ProviderFactory
from models.gaps import GapOutput
from utils.append_guardrail_feedback import append_guardrail_feedback
from utils.invoke_with_validation import invoke_with_validation
from utils.judge_artifacts import judge_artifacts

from evaluation_v3.judges.gap_judge import GapAnalysisJudge
from guardrails.completeness_gate import CompletenessGate
from guardrails.quality_gate import QualityGate
from observability.logger import log_event


def gap_agent(prompt: str, max_attempts: int = 2) -> GapOutput:

    llm = ProviderFactory.get_llm()
    last_output = None

    for attempt in range(max_attempts):
        output = invoke_with_validation(
            invokable=llm,
            payload=prompt,
            model_class=GapOutput
        )

        completeness = CompletenessGate().validate_gaps(output)
        if not completeness.passed:
            last_output = output
            log_event(
                "COMPLETENESS_GATE",
                f"failed on attempt {attempt + 1}: {completeness.failures}",
                level="warn",
            )
            prompt = append_guardrail_feedback(prompt, completeness.failures)
            continue

        judged = judge_artifacts(GapAnalysisJudge(), output.gaps, label="gap")
        gate = QualityGate().validate({"gap_avg_score": judged["avg"]})

        if gate.passed:
            log_event("GAP_GATE", f"passed on attempt {attempt + 1}", avg=judged["avg"])
            return output

        last_output = output
        log_event(
            "GAP_GATE",
            f"failed on attempt {attempt + 1}: {gate.failures}",
            avg=judged["avg"],
            level="warn",
        )
        prompt = append_guardrail_feedback(
            prompt,
            gate.failures,
            "; ".join(judged["feedback"]),
        )

    log_event("GAP_GATE", f"fail-open after {max_attempts} attempts", level="warn")
    return last_output
