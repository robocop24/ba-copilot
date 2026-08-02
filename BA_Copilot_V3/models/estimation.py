from pydantic import BaseModel, Field


class StoryEstimate(BaseModel):

    story: str = Field(validation_alias="user_story")
    story_points: int


class EstimationOutput(BaseModel):
    estimates: list[StoryEstimate]