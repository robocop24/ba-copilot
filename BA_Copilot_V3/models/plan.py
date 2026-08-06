from typing import Literal

from pydantic import BaseModel, Field


class PlanOutput(BaseModel):

    next_step: Literal["analyze_requirements", "done"] = Field(
        description="Next agent to execute"
    )
    reason: str = Field(description="Why this step was chosen")