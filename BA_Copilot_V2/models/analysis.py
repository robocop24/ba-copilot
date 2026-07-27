import ast

from pydantic import BaseModel, Field, field_validator


class AnalysisOutput(BaseModel):
    actors: list[str] = Field(description="Business actors involved in the process")
    modules: list[str] = Field(description="Application modules identified in the requirement")
    requirements: list[str] = Field(description="Functional requirements")

    @field_validator('actors', 'modules', 'requirements', mode='before')
    def parse_lists(cls, v):
        if isinstance(v, str):
            try:
                return ast.literal_eval(v)
            except (ValueError, SyntaxError) as e:
                print(f"Validation error: {e}")
                return []          # ← Return empty list, not dict
        return v