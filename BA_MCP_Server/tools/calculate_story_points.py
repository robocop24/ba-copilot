def calulate_story_points(complexity:str)->int:
    """Calculate story points based on complexity"""
    
    try:
        complexity_mapping = {
                "low":2,
                "medium":5,
                "high":8,
                "very_high":13
            }
            
        complexity = complexity.lower().strip()
            
        return complexity_mapping[complexity]
    
    except KeyError:
        raise ValueError(
            f"Invalid complexity '{complexity}'. "
            "Use: low, medium, high, very_high"
        )