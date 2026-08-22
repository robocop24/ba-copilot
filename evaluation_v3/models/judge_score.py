from pydantic import BaseModel, Field


class RubricScore(BaseModel):
    clarity: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    consistency: int = Field(ge=1, le=5)
    feedback: str

class StoryRubric(RubricScore):
    testability: int = Field(ge=1, le=5)
    
class AcceptanceCriteriaRubric(RubricScore):
    testability: int = Field(ge=1, le=5)

class GapAnalysisRubric(RubricScore):
    specificity: int = Field(ge=1, le=5)