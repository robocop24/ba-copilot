class AcceptanceCriteriaRubricEvaluator:
    
    def evaluate(self, criteria: str):
        
        criteria_lower = criteria.lower()
        
        scores = {}
        
        scores["clarity"] = (5 if len(criteria.split()) >= 10 else 3)
        
        completeness_score = 0
        if "given" in criteria_lower: completeness_score += 2
        if "when" in criteria_lower: completeness_score += 2
        if "then" in criteria_lower: completeness_score += 1
        scores["completeness"] = completeness_score
        
        scores["consistency"] = 5 if ("given" in criteria_lower 
                                      and "when" in criteria_lower) else 2
        
        scores["testability"] = 5 if ("then" in criteria_lower) else 2
        
        total_score = sum(scores.values())
        
        max_score = 20
        
        quality = ("Excellent" if total_score >= 17 else "Good" 
            if total_score >= 13 else "Need improvement")
        
        return {
            "criteria": criteria,
            "scores": scores,
            "total_score": total_score,
            "max_score": max_score,
            "quality": quality
        }
        
    def evaluate_all(self, criteria_list: list[str]):
        
        return [self.evaluate(criteria) for criteria in criteria_list]
