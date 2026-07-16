from agents.base_agent import BaseAgent
import json

class GapAnalysisAgent(BaseAgent):

    def __init__(self):
        super().__init__(prompt_file="prompts/gap_analysis.txt")

    def generate(self, analysis):

        prompt = self.prompt_template.replace("{analysis}", json.dumps(analysis, indent=2))

        response = self.llm.generate(prompt)

        return json.loads(response)