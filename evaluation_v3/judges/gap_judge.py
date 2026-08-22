from BA_Copilot_V3.llm.provider_factory import ProviderFactory
from BA_Copilot_V3.utils.invoke_with_validation import invoke_with_validation
from evaluation_v3.models.judge_score import GapAnalysisRubric
from evaluation_v3.prompt_loader import load_prompt


class GapAnalysisJudge:
    
    def evaluate(self, gap_analysis: str):
        
        llm = ProviderFactory.get_llm()
        
        prompt_template = load_prompt("gap_judge_prompt.txt")
        prompt = prompt_template.format(gap_analysis=gap_analysis)
        
        result = invoke_with_validation(llm, prompt, GapAnalysisRubric)
        
        total = (result.clarity + result.completeness
                 + result.consistency + result.specificity)
        
        return {
            "score": result,
            "total": total,
            "max_score": 20,
        }
