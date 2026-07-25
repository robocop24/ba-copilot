from models.analysis import AnalysisOutput
from pydantic import ValidationError

def analyzer_node(state):

    try:
        analysis = AnalysisOutput(
                actors=["Customer"],
                modules=["Authentication"],
                requirements=["User Login"]
            )
        return {
                "analysis": analysis
            }
    except ValidationError as e:
        print(e)