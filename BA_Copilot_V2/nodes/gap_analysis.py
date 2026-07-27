from models.gaps import GapAnalysisOutput
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt
from pydantic import ValidationError
from utils.json_parser import parse_llm_json

def gap_analysis_node(state):
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(GapAnalysisOutput)
    
    prompt_template = load_prompt("gap_analysis.txt")
    prompt = prompt_template.format(analysis=state["analysis"])
    
    try:
        response = llm.invoke(prompt)
        data = parse_llm_json(response.content)
        gaps = GapAnalysisOutput(**data)
        return {"gaps":gaps}
    except ValidationError as e:
            print(f"Validation error in analyzer: {e}")
            raise