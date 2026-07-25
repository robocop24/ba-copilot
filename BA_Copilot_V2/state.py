from typing import TypedDict
from models.analysis import (AnalysisOutput)
from models.stories import (StoriesOutput)
from models.review import (ReviewOutput)
from models.refinement import (RefinementOutput)

class BAState(TypedDict):

    requirement: str

    context: str

    analysis: AnalysisOutput

    stories: StoriesOutput

    review: ReviewOutput

    refinement: RefinementOutput
    
    approved: bool|None