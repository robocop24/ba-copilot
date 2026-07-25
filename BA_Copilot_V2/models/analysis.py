from pydantic import BaseModel

class AnalysisOutput(BaseModel):

    actors: list[str]

    modules: list[str]

    requirements: list[str]