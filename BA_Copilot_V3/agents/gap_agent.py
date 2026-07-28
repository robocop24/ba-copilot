from models.gaps import GapOutput
from llm.provider_factory import ProviderFactory
from utils.invoke_with_validation import invoke_with_validation

def gap_agent(prompt:str)->GapOutput:
    
    llm = ProviderFactory.get_llm()
    
    return invoke_with_validation(
        invokable=llm,
        payload=prompt,
        model_class=GapOutput
    )
    
    