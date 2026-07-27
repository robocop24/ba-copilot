from typing import TypedDict
from models.analysis import (AnalysisOutput)
from models.stories import (StoriesOutput)
from models.review import (ReviewOutput)
from models.refinement import (RefinementOutput)
from models.gaps import (GapAnalysisOutput)

class BAState(TypedDict, total=False):

    requirement: str

    context: str

    analysis: AnalysisOutput

    stories: StoriesOutput
    
    gaps: GapAnalysisOutput
    
    review_context: str

    review: ReviewOutput

    refinement: RefinementOutput
    
    approved: bool
    
    iteration: int          
    
    max_iterations: int 