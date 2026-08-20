from evaluation_v1.rules.ac_rules import MIN_WORD_COUNT, REQUIRED_PATTERN


class AcceptanceCriteriaEvaluator:
    
    def evaluate(self, criteria: str):
        
        criteria_lower = criteria.lower()
        
        patterns_found = [kw for kw in REQUIRED_PATTERN if kw in criteria_lower]
        has_min_length = len(criteria.split()) >= MIN_WORD_COUNT
        
        score = len(patterns_found) + int(has_min_length)
        max_score = len(REQUIRED_PATTERN) + 1
        
        return {
            "criteria": criteria,
            "patterns_found": patterns_found,
            "patterns_missing": [kw for kw in REQUIRED_PATTERN if kw not in criteria_lower],
            "has_min_length": has_min_length,
            "score": score,
            "max_score": max_score,
            "status": (
                "PASS" if score == max_score else "FAIL"
            )
        }
        
    def evaluate_all(self, criteria_list: list[str]):
        
        return [self.evaluate(criteria) for criteria in criteria_list]