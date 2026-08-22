from pydantic import BaseModel


class GuardrailResult(BaseModel):
    
    passed: bool
    failures: list[str]
    recommendation: str