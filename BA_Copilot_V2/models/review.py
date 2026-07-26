from pydantic import BaseModel

class ReviewOutput(BaseModel):

    quality_score: int
    
    strenghts: list[str]
    
    issues: list[str]

    recommendations: list[str]