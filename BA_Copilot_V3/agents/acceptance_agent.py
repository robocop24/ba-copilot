from llm.provider_factory import ProviderFactory
from models.acceptance import AcceptanceOutput
from utils.invoke_with_validation import invoke_with_validation


def acceptance_agent(prompt:str)->AcceptanceOutput:
        
    llm = ProviderFactory.get_llm()
    
    return invoke_with_validation(
        invokable=llm,
        payload=prompt,
        model_class=AcceptanceOutput
    )