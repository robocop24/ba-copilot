from models.refinement import (RefinementOutput)
from pydantic import ValidationError
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt

def refinement_node(state):
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(RefinementOutput)
    prompt_template = load_prompt("review.txt")
    prompt = prompt_template.format(review_output=state["review"],)
        
    try:
        refinement = structured_llm.invoke(prompt)
        return {"refinement": refinement}
                
    except ValidationError as e:
        print(e)