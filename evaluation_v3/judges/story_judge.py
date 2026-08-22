from BA_Copilot_V3.llm.provider_factory import ProviderFactory
from BA_Copilot_V3.utils.invoke_with_validation import invoke_with_validation
from evaluation_v3.models.judge_score import StoryRubric
from evaluation_v3.prompt_loader import load_prompt


class StoryJudge:
    
    def evaluate(self, story: str):
        
        llm = ProviderFactory.get_llm()
        
        prompt_template = load_prompt("story_judge_prompt.txt")
        prompt = prompt_template.format(story=story)
        
        score = invoke_with_validation(llm, prompt, StoryRubric)
        
        total = (score.clarity + score.completeness
                 + score.consistency + score.testability)
        
        return {
            "score": score,
            "total": total,
            "max_score": 20,
        }