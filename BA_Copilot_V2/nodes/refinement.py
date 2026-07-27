from models.refinement import RefinementOutput
from llm.provider_factory import ProviderFactory
from utils.prompt_loader import load_prompt
from utils.json_parser import parse_llm_json


def refinement_node(state):
    llm = ProviderFactory.get_llm()
    prompt_template = load_prompt("refinement.txt")
    prompt = prompt_template.format(
        review_output=state["review"],
        stories=state["stories"]
    )

    fallback = {
        "revised_stories": [],
        "refinements": [],
        "changes_summary": "LLM parsing failed"
    }

    try:
        response = llm.invoke(prompt)
        data = parse_llm_json(response.content, default=fallback)
        refinement = RefinementOutput(**data)
        return {"refinement": refinement, "iteration": state.get("iteration", 0) + 1}
    except Exception as e:
        print(f"Error in refinement_node: {e}")
        refinement = RefinementOutput(**fallback)
        return {"refinement": refinement, "iteration": state.get("iteration", 0) + 1}