from core.mock_provider import MockLLMProvider

class ProviderFactory:

    @staticmethod
    def get_provider():
        # Here you can implement logic to choose which LLM provider to return
        # For example, you could read from a config file or environment variable
        # For now, we'll just return a default provider
        return MockLLMProvider()