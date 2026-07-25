from agents.base_agent import BaseAgent
import json

class AcceptanceCriteriaAgent(BaseAgent):

    def __init__(self):
        super().__init__(prompt_file="prompts/acceptance_criteria.txt")

    def generate(self, stories: dict):

        prompt = self.prompt_template.replace("{stories}", json.dumps(stories, indent=2))

        response = self.llm.generate(prompt)

        return json.loads(response)