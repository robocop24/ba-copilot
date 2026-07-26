from pydantic import (BaseModel, Field)

class GapAnalysisOutput(BaseModel):
    
    gaps: list[str] = Field(description="Identified requirement gaps")
    
    questions: list[str] = Field(description="Clarification question")