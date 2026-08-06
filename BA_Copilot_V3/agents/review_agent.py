from llm.provider_factory import ProviderFactory
from models.review import ReviewOutput
from utils.invoke_with_validation import invoke_with_validation

def review_agent(prompt: str) -> ReviewOutput:
    
    llm = ProviderFactory.get_llm()
    
    return invoke_with_validation(
        invokable=llm,
        payload=prompt,
        model_class=ReviewOutput
    )