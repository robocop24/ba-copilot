class StoryRubricEvaluator:
    
    def evaluate(self, story: str):
        
        story_lower = story.lower()
        
        scores = {}
        
        scores["clarity"] = (5 if len(story.split()) >= 12 else 3)
        
        completeness_score = 0
        if "as a" in story_lower: completeness_score +=2
        if "i want" in story_lower: completeness_score +=2
        if "so that" in story_lower: completeness_score +=1
        scores["completeness"] =completeness_score
        
        scores["consistency"] = 5 if ("as a" in story_lower 
                                      and "i want" in story_lower) else 2
        
        scores["testability"] = 5 if ("so that" in story_lower) else 2
        
        total_score = sum(scores.values())
        
        max_score = 20
        
        quality = ("Excellent" if total_score >= 17 else "Good" 
            if total_score >= 13 else "Need improvement")
        
        return {
            "story": story,
            "scores": scores,
            "total_score": total_score,
            "max_score": max_score,
            "quality": quality
        }
        
    def evaluate_all(self, stories: list[str]):
        
        return [self.evaluate(story) for story in stories]