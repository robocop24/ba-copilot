from llm.settings import (MODEL_PROVIDER,MODEL_NAME)
from llm.ollama_provider import OllamaProvider

class ProviderFactory:
    
    @staticmethod
    def get_llm():
        
        if MODEL_PROVIDER == "ollama":
            return OllamaProvider(MODEL_NAME).get_llm()
        
        raise ValueError("Unsupported provider")