from llm.provider_factory import ProviderFactory
from models.refinement import RefinementOutput
from utils.invoke_with_validation import invoke_with_validation

def refinement_agent(prompt):
    
    llm = ProviderFactory.get_llm()
    
    return invoke_with_validation(
        invokable=llm,
        payload=prompt,
        model_class=RefinementOutput
    )