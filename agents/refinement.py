from agents.base_agent import BaseAgent
import json

class RefinementAgent(BaseAgent):

    def __init__(self):
        super().__init__(prompt_file="prompts/refinement.txt")

    def generate(self, review_output: dict):

        prompt = self.prompt_template.replace("{review_output}", json.dumps(review_output, indent=2))

        response = self.llm.generate(prompt)

        return json.loads(response)