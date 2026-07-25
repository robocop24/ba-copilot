from pydantic import BaseModel

class RefinementOutput(BaseModel):

    improvements: list[str]

    final_quality_score: int