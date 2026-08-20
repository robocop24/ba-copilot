class GapAnalysisRubricEvaluator:
    
    def evaluate(self, gap_analysis: str):
        
        gap_lower = gap_analysis.lower()
        
        scores = {}
        
        scores["clarity"] = (5 if len(gap_analysis.split()) >= 12 else 3)
        
        completeness_score = 0
        if "assumption" in gap_lower: completeness_score += 1
        if "dependency" in gap_lower: completeness_score += 1
        if "risk" in gap_lower: completeness_score += 1
        if "clarification" in gap_lower: completeness_score += 1
        if completeness_score == 4: completeness_score += 1  # bonus: all sections present
        scores["completeness"] = completeness_score
        
        scores["consistency"] = 5 if ("assumption" in gap_lower 
                                      and "dependency" in gap_lower) else 2
        
        scores["specificity"] = 5 if ("risk" in gap_lower 
                                      or "clarification" in gap_lower) else 2
        
        total_score = sum(scores.values())
        
        max_score = 20
        
        quality = ("Excellent" if total_score >= 17 else "Good" 
            if total_score >= 13 else "Need improvement")
        
        return {
            "gap_analysis": gap_analysis,
            "scores": scores,
            "total_score": total_score,
            "max_score": max_score,
            "quality": quality
        }
        
    def evaluate_all(self, analyses_list: list[str]):
        
        return [self.evaluate(item) for item in analyses_list]
