from pydantic import BaseModel, Field


class RefinementOutput(BaseModel):

    improvements: list[str] = Field(
        description="Concrete improvements made across all artifacts (stories, ACs, estimates, gaps) based on review feedback"
    )
    final_summary: str = Field(description="Final executive summary of the refined BA analysis")