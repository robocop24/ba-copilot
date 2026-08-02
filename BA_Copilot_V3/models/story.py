from pydantic import BaseModel, Field


class StoryOutput(BaseModel):
    
    user_stories: list[str] = Field(description="Generated user stories")