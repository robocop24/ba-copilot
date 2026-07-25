from pydantic import BaseModel

class ReviewOutput(BaseModel):

    quality_score: int

    recommendations: list[str]