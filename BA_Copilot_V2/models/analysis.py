from pydantic import (BaseModel, Field, ValidationError, field_validator)

class AnalysisOutput(BaseModel):

    actors: list[str] = Field(description="Business actors involved in the process")

    modules: list[str] = Field(description="Application modules identified in the requirement")

    requirements: list[str] = Field(description="Functional requirements")
    
    @field_validator('actors', 'modules', 'requirements', mode='before')
    def parse_lists(cls, v):
        if isinstance(v, str):
            # Try to parse string representation of list
            import ast
            try:
                return ast.literal_eval(v)
            except ValidationError as e:
                print(f"Validation error: {e}")
                return {
                    "analysis": AnalysisOutput(
                        actors=[],
                        modules=[],
                        requirements=[]
                    )
                    }
        return v