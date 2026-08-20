import sys
from pathlib import Path

# Add the project root to sys.path so absolute imports work when this file
# is run directly as a script (python evaluation/dashboard.py).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluation_v1.evaluators.ac_evaluator import AcceptanceCriteriaEvaluator
from evaluation_v1.evaluators.gap_evaluator import GapAnalysisEvaluator
from evaluation_v1.evaluators.story_evaluator import StoryEvaluator

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

def story_evaluator(evaluator:StoryEvaluator):
    
    results = evaluator.evaluate_all(stories=stories)
        
    total = len(results)
        
    passed = sum(1 for result in results if result["status"] == "PASS")
        
    failed = total - passed
        
    success_rate = (passed/total)*100
        
    print("\n=== Story Evaluation ===\n")
        
    print(f"Total Stories: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {success_rate:.2f}%")
        
    print("\n=== Details ===\n")
        
    for index, result in enumerate(results, start=1):
            
        print(f"Story {index}")
        print(f"Status {result["status"]}")
        print(f"Score {result["score"]}/{result["max_score"]}")
        print("-"*40)
        
def ac_evaluator(evaluator:AcceptanceCriteriaEvaluator):
    
    results = evaluator.evaluate_all(criteria_list=criteria_list)
        
    total = len(results)
        
    passed = sum(1 for result in results if result["status"] == "PASS")
        
    failed = total - passed
        
    success_rate = (passed/total)*100
        
    print("\n=== Acceptance Criteria Evaluation ===\n")
        
    print(f"Total Criteria: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {success_rate:.2f}%")
        
    print("\n=== Details ===\n")
        
    for index, result in enumerate(results, start=1):
            
        print(f"Criteria {index}")
        print(f"Status {result["status"]}")
        print(f"Score {result["score"]}/{result["max_score"]}")
        print("-"*40)
        
def gap_evaluator(evaluator:GapAnalysisEvaluator):
    
    results = evaluator.evaluate_all(gap_analyses)
        
    total = len(results)
        
    passed = sum(1 for result in results if result["status"] == "PASS")
        
    failed = total - passed
        
    success_rate = (passed/total)*100
        
    print("\n=== Gap Analysis Evaluation ===\n")
        
    print(f"Total Analysis: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {success_rate:.2f}%")
        
    print("\n=== Details ===\n")
        
    for index, result in enumerate(results, start=1):
            
        print(f"Analysis {index}")
        print(f"Status {result["status"]}")
        print(f"Score {result["score"]}/{result["max_score"]}")
        print("-"*40)


def main():
    
    story_evaluator(StoryEvaluator())
    ac_evaluator(AcceptanceCriteriaEvaluator())
    gap_evaluator(GapAnalysisEvaluator())
    
        
if __name__ == "__main__":
    main()