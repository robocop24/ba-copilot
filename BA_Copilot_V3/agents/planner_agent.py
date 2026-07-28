from llm.provider_factory import ProviderFactory
from models.plan import PlanOutput
from utils.invoke_with_validation import invoke_with_validation

def planner_agent(prompt: str) -> PlanOutput:

    llm = ProviderFactory.get_llm()

    return invoke_with_validation(
        invokable=llm,
        payload=prompt,
        model_class=PlanOutput,
    )