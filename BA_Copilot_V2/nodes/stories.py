from models.stories import StoriesOutput
from models.analysis import AnalysisOutput
from pydantic import ValidationError
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt
from state import BAState

def stories_node(state: BAState) -> dict:
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(StoriesOutput)
    prompt_template = load_prompt("user_story.txt")
    prompt = prompt_template.format(analysis=state["analysis"])

    try:
        stories = structured_llm.invoke(prompt)
        return {
                "stories": stories
            }
    
    except ValidationError as e:
            print(e)