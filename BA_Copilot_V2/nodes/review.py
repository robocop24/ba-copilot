from models.review import ReviewOutput
from pydantic import ValidationError

def review_node(state):

    try:
        review = ReviewOutput(
                              quality_score=10,
                              recommendations=[
                                  "Add MFA", "Define password policy"
                              ]
                )
                      
        return {"review":review}
    except ValidationError as e:
            print(e)