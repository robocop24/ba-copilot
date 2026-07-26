from models.gaps import GapAnalysisOutput
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt
from pydantic import ValidationError

def gap_analysis_node(state):
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(GapAnalysisOutput)
    
    prompt_template = load_prompt("gap_analysis.txt")
    prompt = prompt_template.format(analysis=state["analysis"])
    
    try:
        gaps = structured_llm.invoke(prompt)
        return {"gaps":gaps}
    except ValidationError as e:
            print(f"Validation error in analyzer: {e}")
            raise