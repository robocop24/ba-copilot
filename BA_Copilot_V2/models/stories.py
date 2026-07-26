from pydantic import (BaseModel, ValidationError, field_validator, Field)

class StoriesOutput(BaseModel):

    user_stories: list[str] = Field(description="Generated user stories")
    
    @field_validator('user_stories', mode='before')
    def parse_lists(cls, v):
            if isinstance(v, str):
                # Try to parse string representation of list
                import ast
                try:
                    return ast.literal_eval(v)
                except ValidationError as e:
                    print(f"Validation error: {e}")
                    return {
                        "stories": StoriesOutput(
                            user_stories=[]
                        )
                        }
            return v