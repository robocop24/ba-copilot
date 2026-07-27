from langchain_ollama import ChatOllama
from llm.base_provider import BaseProvider
from llm.settings import (MODEL_NAME)

class OllamaProvider(BaseProvider):
    
    @staticmethod
    def get_llm():
        
        return ChatOllama(model=MODEL_NAME,temperature=0)