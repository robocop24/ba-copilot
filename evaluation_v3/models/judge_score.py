from pydantic import BaseModel, Field


class StoryJudgeScore(BaseModel):
    clarity: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    consistency: int = Field(ge=1, le=5)
    testability: int = Field(ge=1, le=5)
    feedback: str


class AcceptanceCriteriaJudgeScore(BaseModel):
    clarity: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    consistency: int = Field(ge=1, le=5)
    testability: int = Field(ge=1, le=5)
    feedback: str


class GapAnalysisJudgeScore(BaseModel):
    clarity: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    consistency: int = Field(ge=1, le=5)
    specificity: int = Field(ge=1, le=5)
    feedback: str