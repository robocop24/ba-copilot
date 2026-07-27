from models.review import ReviewOutput
from pydantic import ValidationError
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt
from utils.json_parser import parse_llm_json

def review_node(state):
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(ReviewOutput)
    prompt_template = load_prompt("review.txt")
    prompt = prompt_template.format(review_context=state["review_context"],)
    
    try:
        response = llm.invoke(prompt)
        data = parse_llm_json(response.content)
        review = ReviewOutput(**data)
        return {"review": review}
            
    except ValidationError as e:
            print(e)