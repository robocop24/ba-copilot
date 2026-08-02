from langchain.agents import create_agent
from llm.provider_factory import ProviderFactory
from models.estimation import EstimationOutput
from tools.retriever import calulate_story_points
from utils.invoke_with_validation import invoke_with_validation


def estimation_agent(prompt:str)->EstimationOutput:
    
    llm = ProviderFactory().get_llm()
    
    agent = create_agent(model=llm, tools=[calulate_story_points])
    
    return invoke_with_validation(
        invokable=agent,
        payload={
            "messages": [
                ("user", prompt)
            ]
        },
        model_class=EstimationOutput
    )