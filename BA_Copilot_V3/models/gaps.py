from pydantic import (BaseModel, Field)

class GapOutput(BaseModel):
    
    gaps_found: bool = Field(description="True if any gaps were identified in the analysis")
    gaps: list[str] = Field(description="List of gap descriptions (missing requirements, edge cases, integration points)")
    
    