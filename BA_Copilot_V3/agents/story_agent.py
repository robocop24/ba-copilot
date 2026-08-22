from llm.provider_factory import ProviderFactory
from models.story import StoryOutput
from utils.append_guardrail_feedback import append_guardrail_feedback
from utils.invoke_with_validation import invoke_with_validation
from utils.judge_artifacts import judge_artifacts

from evaluation_v3.judges.story_judge import StoryJudge
from guardrails.completeness_gate import CompletenessGate
from guardrails.quality_gate import QualityGate
from observability.logger import log_event


def story_agent(prompt: str, max_attempts: int = 2) -> StoryOutput:
    
    llm = ProviderFactory.get_llm()
    last_output = None

    for attempt in range(max_attempts):
        output = invoke_with_validation(
            invokable=llm,
            payload=prompt,
            model_class=StoryOutput
        )

        # 1) Structural completeness first — free, catches empty/malformed output
        #    without paying for an LLM judge.
        completeness = CompletenessGate().validate_story(output)
        if not completeness.passed:
            last_output = output
            log_event(
                "COMPLETENESS_GATE",
                f"failed on attempt {attempt + 1}: {completeness.failures}",
                level="warn",
            )
            prompt = append_guardrail_feedback(prompt, completeness.failures)
            continue

        # 2) LLM judge + quality gate — subjective quality vs threshold.
        judged = judge_artifacts(StoryJudge(), output.user_stories, label="story")
        gate = QualityGate().validate({"story_avg_score": judged["avg"]})

        if gate.passed:
            log_event("STORY_GATE", f"passed on attempt {attempt + 1}", avg=judged["avg"])
            return output

        last_output = output
        log_event(
            "STORY_GATE",
            f"failed on attempt {attempt + 1}: {gate.failures}",
            avg=judged["avg"],
            level="warn",
        )
        prompt = append_guardrail_feedback(
            prompt,
            gate.failures,
            "; ".join(judged["feedback"]),
        )

    log_event("STORY_GATE", f"fail-open after {max_attempts} attempts", level="warn")
    return last_output