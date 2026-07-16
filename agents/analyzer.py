from pathlib import Path
import json
from agents.base_agent import BaseAgent

class RequirementAnalyzer(BaseAgent):
    def __init__(self):
        super().__init__(prompt_file="prompts/analyzer.txt")

    def analyze(self, requirement: str):

        prompt = self.prompt_template.replace("{requirement}", requirement)

        response = self.llm.generate(prompt)

        return json.loads(response)