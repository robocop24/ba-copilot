from agents.gap_agent import gap_agent
from utils.prompt_loader import load_prompt


def gap_node(state):

    prompt_template = load_prompt("gap.txt")
    prompt = prompt_template.format(
        requirement=state["requirement"],
        analysis=state["analysis"].model_dump_json(indent=2),
    )

    gaps = gap_agent(prompt=prompt)

    return {
        "gaps": gaps
    }