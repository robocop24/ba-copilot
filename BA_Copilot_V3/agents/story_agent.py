from llm.provider_factory import ProviderFactory
from models.story import StoryOutput
from utils.invoke_with_validation import invoke_with_validation

def story_agent(prompt):
    
    llm = ProviderFactory.get_llm()
    
    return invoke_with_validation(
        invokable=llm,
        payload=prompt,
        model_class=StoryOutput
    )