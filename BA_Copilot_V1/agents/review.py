from agents.base_agent import BaseAgent
import json

class ReviewAgent(BaseAgent):

    def __init__(self):
        super().__init__(prompt_file="prompts/review.txt")

    def generate(self, workflow_output: dict):

        prompt = self.prompt_template.replace("{workflow_output}", json.dumps(workflow_output, indent=2))

        response = self.llm.generate(prompt)

        return json.loads(response)