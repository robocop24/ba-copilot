from langchain.agents import create_agent
from llm.provider_factory import ProviderFactory
from models.estimation import EstimationOutput
from tools.retriever import calculate_story_points
from utils.invoke_structured import invoke_structured


def estimation_agent(prompt:str)->EstimationOutput:
    
    llm = ProviderFactory.get_llm()
    
    agent = create_agent(
        model=llm, 
        tools=[calculate_story_points],
        response_format=EstimationOutput
        )
    
    return invoke_structured(
        agent,
        payload={
            "messages": [
                ("user", prompt)
            ]
        }
    )