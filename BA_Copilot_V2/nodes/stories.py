from models.stories import StoriesOutput
from pydantic import ValidationError

def stories_node(state):

    try:
        stories = StoriesOutput(
            user_stories=["As a customer, I want to login so that I can access my account."]
            )
        return {
                "stories": stories
            }
    
    except ValidationError as e:
            print(e)