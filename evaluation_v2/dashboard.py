import sys
from pathlib import Path

# Add the project root to sys.path so absolute imports work when this file
# is run directly as a script (python evaluation/dashboard.py).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation_v2.evaluators.ac_rubric_evaluator import (
    AcceptanceCriteriaRubricEvaluator,
)
from evaluation_v2.evaluators.gap_rubric_evaluator import GapAnalysisRubricEvaluator
from evaluation_v2.evaluators.story_rubric_evaluator import StoryRubricEvaluator

stories = [
    "As a User, I want to login, so that I can access my account.",
    "Create login page",
    "As a Customer, I want to reset my password, so that I can recover access to my account.",
]

criteria_list = [
    """
    Given a registered user, when a valid credentials are entered,
    Then access should be granted.
    """,
    """
    User enters password and logs in.
    """,
    """
    Given a user forget password, when reset link is clicked,
    Then the password reset page should open.
    """
]

gap_analyses = [
    """
    Assumption: Users already exist.
    Dependency: Email service must be available.
    Risk: OTP delivery may fail.
    Clarification:Password policy is not defined.
    """,
    """
        System should work correctly.
    """,
    """
        Assumption: Users have valid credentials.
        Dependency: Authentication API.
        Risk: High Login Traffic.
        Clarification:Session timeout duration not specified.
    """
]
     

def story_rubric_evaluator(evaluator:StoryRubricEvaluator):
    
    results = evaluator.evaluate_all(stories=stories)
        
    print("\n=== Story Rubric Evaluation ===\n")
                
    for index, result in enumerate(results, start=1):
            
        print(f"Story {index}")
        print(f"Quality {result["quality"]}")
        print(f"Total {result["total_score"]}/{result["max_score"]}")
        print("Scores:")
        for key, value in (result["scores"].items()):
            print(f"{key}:{value}/5")
        print("-"*40)
        

def ac_rubric_evaluator(evaluator: AcceptanceCriteriaRubricEvaluator):
    
    results = evaluator.evaluate_all(criteria_list=criteria_list)
        
    print("\n=== Acceptance Criteria Rubric Evaluation ===\n")
                
    for index, result in enumerate(results, start=1):
            
        print(f"Criteria {index}")
        print(f"Quality {result["quality"]}")
        print(f"Total {result["total_score"]}/{result["max_score"]}")
        print("Scores:")
        for key, value in (result["scores"].items()):
            print(f"{key}:{value}/5")
        print("-"*40)


def gap_rubric_evaluator(evaluator: GapAnalysisRubricEvaluator):
    
    results = evaluator.evaluate_all(gap_analyses)
        
    print("\n=== Gap Analysis Rubric Evaluation ===\n")
                
    for index, result in enumerate(results, start=1):
            
        print(f"Analysis {index}")
        print(f"Quality {result["quality"]}")
        print(f"Total {result["total_score"]}/{result["max_score"]}")
        print("Scores:")
        for key, value in (result["scores"].items()):
            print(f"{key}:{value}/5")
        print("-"*40)


def main():
    
    story_rubric_evaluator(StoryRubricEvaluator())
    ac_rubric_evaluator(AcceptanceCriteriaRubricEvaluator())
    gap_rubric_evaluator(GapAnalysisRubricEvaluator())
    
    
        
if __name__ == "__main__":
    main()