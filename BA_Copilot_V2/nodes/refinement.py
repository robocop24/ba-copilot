from models.refinement import (RefinementOutput)
from pydantic import ValidationError

def refinement_node(state):

    try:
        refinement = RefinementOutput(
                improvements=[
                    "Add MFA requirement",
                    "Define password policy"
                ],
                final_quality_score=9
            )
        
        return { "refinement": refinement}
    
    except ValidationError as e:
            print(e)