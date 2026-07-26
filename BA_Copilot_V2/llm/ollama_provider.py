from langchain_ollama import ChatOllama
from llm.base_provider import BaseProvider

class OllamaProvider(BaseProvider):
    
    def __init__(self, model_name):
        self.model_name = model_name
        
    def get_llm(self):
        
        return ChatOllama(model=self.model_name,temperature=0)