class WorkflowState:

    def __init__(self):

        self.analysis = None
        self.stories = None
        self.acceptance_criteria = None
        self.story_gaps = None
        self.effort_estimation = None
        self.review = None
        self.refinement = None


    def to_dict(self):
        
        return {
            "analysis": self.analysis,
            "stories": self.stories,
            "acceptance_criteria": self.acceptance_criteria,
            "story_gaps": self.story_gaps,
            "effort_estimation": self.effort_estimation,
            "review": self.review,
            "refinement": self.refinement
        }