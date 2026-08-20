from evaluation_v1.rules.story_rules import MIN_WORD_COUNT, REQUIRED_PATTERN


class StoryEvaluator:
    
    def evaluate(self, story: str):
        
        story_lower = story.lower()
        
        patterns_found = [kw for kw in REQUIRED_PATTERN if kw in story_lower]
        has_min_length = len(story.split()) >= MIN_WORD_COUNT
        
        score = len(patterns_found) + int(has_min_length)
        max_score = len(REQUIRED_PATTERN) + 1
        
        return {
            "story": story,
            "patterns_found": patterns_found,
            "patterns_missing": [kw for kw in REQUIRED_PATTERN if kw not in story_lower],
            "has_min_length": has_min_length,
            "score": score,
            "max_score": max_score,
            "status": (
                "PASS" if score == max_score else "FAIL"
            )
        }
        
    def evaluate_all(self, stories: list[str]):
        
        return [self.evaluate(story) for story in stories]