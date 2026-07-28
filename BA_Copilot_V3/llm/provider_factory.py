from llm.settings import MODEL_PROVIDER
from llm.deepseek_provider import DeepSeekProvider

class ProviderFactory:

    @staticmethod
    def get_llm():
        if MODEL_PROVIDER == "deepseek":
            return DeepSeekProvider.get_llm()
        raise ValueError("Unsupported provider")