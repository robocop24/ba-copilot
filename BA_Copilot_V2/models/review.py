from pydantic import BaseModel, Field

class ReviewOutput(BaseModel):

    score: int = Field(description="Quality score from 1 to 10")
    strengths: list[str] = Field(description="Strengths of the BA artifacts")
    weaknesses: list[str] = Field(description="Weaknesses or gaps")
    recommendations: list[str] = Field(description="Improvement suggestions")
    approved: bool = Field(description="Whether the artifacts are approved")