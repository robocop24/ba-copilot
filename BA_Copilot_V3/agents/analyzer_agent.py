from langchain.agents import create_agent
from llm.provider_factory import ProviderFactory
from models.analysis import AnalysisOutput
from tools.retriever import retrieve_similar_brd
from utils.invoke_structured import invoke_structured


def analyzer_agent(prompt: str) -> AnalysisOutput:
    llm = ProviderFactory.get_llm()
    agent = create_agent(
        model=llm, 
        tools=[retrieve_similar_brd],
        response_format=AnalysisOutput)
    
    #agent.get_graph().draw_mermaid_png(output_file_path="analyzer_agent_graph.png")

    return invoke_structured(
        invokable=agent,
        payload={
            "messages": [
                ("user", prompt)
            ]
        }    
    )