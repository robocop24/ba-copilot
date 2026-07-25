from pydantic import BaseModel

class StoriesOutput(BaseModel):

    user_stories: list[str]