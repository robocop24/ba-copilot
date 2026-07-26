from models.review import ReviewOutput
from pydantic import ValidationError
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt

def review_node(state):
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(ReviewOutput)
    prompt_template = load_prompt("review.txt")
    prompt = prompt_template.format(review_context=state["review_context"],)
    
    try:
        review = structured_llm.invoke(prompt)
        return {"review": review}
            
    except ValidationError as e:
            print(e)