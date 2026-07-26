from models.analysis import AnalysisOutput
from pydantic import ValidationError
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt
from state import BAState

def analyzer_node(state: BAState) -> dict:
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(AnalysisOutput)
    
    prompt_template = load_prompt("analyzer.txt")
    prompt = prompt_template.format(
        requirement=state["requirement"],
        context=state["context"]
    )

    try:
        analysis = structured_llm.invoke(prompt)
        
        return {
                "analysis": analysis
            }
    except ValidationError as e:
        print(f"Validation error in analyzer: {e}")
        raise