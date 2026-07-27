from models.analysis import AnalysisOutput
from pydantic import ValidationError
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt
from state import BAState
from utils.json_parser import parse_llm_json

def analyzer_node(state: BAState) -> dict:
    
    llm = ProviderFactory.get_llm()
    structured_llm = llm.with_structured_output(AnalysisOutput)
    
    prompt_template = load_prompt("analyzer.txt")
    prompt = prompt_template.format(
        requirement=state["requirement"],
        context=state["context"]
    )

    try:
        response = llm.invoke(prompt)
        data = parse_llm_json(response.content)
        analysis = AnalysisOutput(**data)
        return {
                "analysis": analysis
            }
    except ValidationError as e:
        print(f"Validation error in analyzer: {e}")
        raise