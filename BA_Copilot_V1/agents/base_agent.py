from pathlib import Path
from core.provider_factory import ProviderFactory

class BaseAgent:
    def __init__(self, prompt_file: str):

        prompt_path = Path(prompt_file)
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

        self.llm = ProviderFactory.get_provider()