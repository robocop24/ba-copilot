from typing import TypedDict

from models.analysis import AnalysisOutput
from models.estimation import EstimationOutput
from models.gaps import GapOutput
from models.plan import PlanOutput
from models.refinement import RefinementOutput
from models.review import ReviewOutput
from models.story import StoryOutput


class BAState(TypedDict):
    requirement: str
    plan: PlanOutput
    analysis: AnalysisOutput
    stories: StoryOutput
    estimation: EstimationOutput
    gaps: GapOutput
    review:ReviewOutput
    refinement: RefinementOutput
    approved: bool|None
    
    iteration: int
    max_iterations: int