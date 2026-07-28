from pydantic import BaseModel, Field

class PlanOutput(BaseModel):
    
    next_step: str = Field(description="Next agent to execute")
    reason: str = Field(description="")