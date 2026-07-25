from agents.base_agent import BaseAgent
import json

class EffortEstimationAgent(BaseAgent):

    def __init__(self):
        super().__init__(prompt_file="prompts/effort_estimation.txt")

    def generate(self, workflow_input: dict):

        prompt = self.prompt_template.replace("{workflow_input}", json.dumps(workflow_input, indent=2))

        response = self.llm.generate(prompt)

        return json.loads(response)