from langchain.agents import create_agent
from llm.provider_factory import ProviderFactory
from models.analysis import AnalysisOutput
from tools.retriever import retrieve_similar_brd
from utils.invoke_with_validation import invoke_with_validation

def analyzer_agent(prompt: str) -> AnalysisOutput:
    llm = ProviderFactory.get_llm()
    agent = create_agent(model=llm, tools=[retrieve_similar_brd])
    
    #agent.get_graph().draw_mermaid_png(output_file_path="analyzer_agent_graph.png")

    return invoke_with_validation(
        invokable=agent,
        payload={
            "messages": [
                ("user", prompt)
            ]
        },
        model_class=AnalysisOutput,
    )