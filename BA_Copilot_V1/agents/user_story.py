import json
from pathlib import Path
from agents.base_agent import BaseAgent

class UserStoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(prompt_file="prompts/user_story.txt")

    def generate(self, analysis: dict):

        prompt = self.prompt_template.replace("{analysis}", json.dumps(analysis, indent=2))

        response = self.llm.generate(prompt)

        return json.loads(response)