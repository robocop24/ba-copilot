from evaluation_v1.rules.gap_rules import MIN_WORD_COUNT, REQUIRED_PATTERN


class GapAnalysisEvaluator:
    
    def evaluate(self, gap_analysis: str):
        
        gap_lower = gap_analysis.lower()
        
        patterns_found = [kw for kw in REQUIRED_PATTERN if kw in gap_lower]
        has_min_length = len(gap_analysis.split()) >= MIN_WORD_COUNT
        
        score = len(patterns_found) + int(has_min_length)
        max_score = len(REQUIRED_PATTERN) + 1
        
        return {
            "gap_analysis": gap_analysis,
            "patterns_found": patterns_found,
            "patterns_missing": [kw for kw in REQUIRED_PATTERN if kw not in gap_lower],
            "has_min_length": has_min_length,
            "score": score,
            "max_score": max_score,
            "status": (
                "PASS" if score == max_score else "FAIL"
            )
        }
        
    def evaluate_all(self, analyses_list: list[str]):
        
        return [self.evaluate(item) for item in analyses_list]