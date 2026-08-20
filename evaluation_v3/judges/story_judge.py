from BA_Copilot_V3.llm.provider_factory import ProviderFactory
from BA_Copilot_V3.utils.invoke_with_validation import invoke_with_validation
from evaluation_v3.models.judge_score import StoryJudgeScore
from evaluation_v3.prompt_loader import load_prompt


class StoryJudge:
    
    def evaluate(self, story: str):
        
        llm = ProviderFactory.get_llm()
        
        prompt_template = load_prompt("story_judge_prompt.txt")
        prompt = prompt_template.format(story=story)
        
        result = invoke_with_validation(llm, prompt, StoryJudgeScore)
        
        total = (result.clarity + result.completeness
                 + result.consistency + result.testability)
        
        return {
            "score": result,
            "total": total,
            "max_score": 20,
        }