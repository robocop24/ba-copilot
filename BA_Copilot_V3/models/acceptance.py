from pydantic import BaseModel, Field


class StoryCriteria(BaseModel):
    """Acceptance criteria for a single user story."""

    story_index: int = Field(description="0-based index matching the input stories list")
    story_summary: str = Field(description="Short summary of the story for traceability")
    acceptance_criteria: list[str] = Field(
        description="3-5 Given/When/Then criteria for this story"
    )


class AcceptanceOutput(BaseModel):
    """Container for all acceptance criteria."""

    criteria: list[StoryCriteria] = Field(
        description="Acceptance criteria for each user story"
    )