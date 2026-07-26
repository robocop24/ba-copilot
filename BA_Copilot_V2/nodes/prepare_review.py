def prepare_review_node(state):
    
    review_context = f"""
    
    USER STORIES
    {state['stories'].model_dump_json}
    
    GAP ANALYSIS
    {state['gaps'].model_dump_json}
    
    """
    
    return {
        "review_context": review_context
    }