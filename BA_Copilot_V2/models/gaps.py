from pydantic import (BaseModel, ValidationError, field_validator, Field)

class GapAnalysisOutput(BaseModel):
    
    gaps_found: bool = Field(description="True if any gaps were identified in the analysis")
    gaps: list[str] = Field(description="List of gap descriptions (missing requirements, edge cases, integration points)")
    recommendations: list[str] = Field(description="Recommendations to address each gap")
    
    