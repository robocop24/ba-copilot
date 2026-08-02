
def review_requirement(requirement: str, analysis: str) -> str:
    """Prompt template: peer-review a requirement against BA standards."""
    return f"""
You are a Senior Business Analyst performing a peer review of the following material.

Requirement under review:
{requirement}

Submitted analysis / supporting notes:
{analysis}

Instructions:
1. Evaluate this requirement against the INVEST criteria (Independent, Negotiable,
   Valuable, Estimable, Small, Testable).
2. Flag any ambiguities, missing edge cases, or implicit assumptions.
3. Rate the requirement on a scale of 1-5 for: clarity, completeness, testability.
4. Provide concrete rewrite suggestions where the rating is ≤ 3.
5. Summarise your findings in a 3-bullet executive summary.
"""