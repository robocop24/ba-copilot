from pydantic import BaseModel, Field

class RefinementOutput(BaseModel):

    revised_stories: list[str] = Field(description="Refined user stories after incorporating feedback")
    refinements: list[str] = Field(description="Specific changes made to address weaknesses/recommendations")
    changes_summary: str = Field(description="Brief summary of all changes made")