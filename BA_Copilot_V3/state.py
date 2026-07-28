from typing import TypedDict

from models.analysis import AnalysisOutput
from models.plan import PlanOutput
from models.gaps import GapOutput
from models.story import StoryOutput
from models.review import ReviewOutput
from models.refinement import RefinementOutput

class BAState(TypedDict):
    requirement: str
    plan: PlanOutput
    analysis: AnalysisOutput
    stories: StoryOutput
    gaps: GapOutput
    review:ReviewOutput
    refinement: RefinementOutput
    approved: bool|None
    
    iteration: int
    max_iterations: int