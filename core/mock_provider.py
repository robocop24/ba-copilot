from core.llm import LLMProvider

class MockLLMProvider(LLMProvider):

    def generate(self, prompt: str) -> str:

        if "agent_type:user_stories" in prompt.lower():

            return """
            {
                "user_stories": [
                    {
                        "story": "As a customer, I want to register so that I can access the portal."
                    },
                    {
                        "story": "As a customer, I want to login so that I can access my account."
                    }
                ]
            }
            """
       
        if "gap_analysis" in prompt.lower():
            return """{
                "gaps": [
            "Password policy is not defined.",
            "Session timeout is not specified.",
            "Email verification requirements are unclear."
        ],
        "clarification_questions": [
            "Should email verification be mandatory?",
            "What password complexity rules should apply?",
            "Should MFA be supported?"
        ]
    }
    """
   
        if "agent_type:acceptance_criteria" in prompt.lower():
            return """
    {
        "acceptance_criteria": [
            {
                "story": "User Registration",
                "criteria": [
                    "Given the user is on the registration page",
                    "When valid details are submitted",
                    "Then the account should be created successfully"
                ]
            },
            {
                "story": "User Login",
                "criteria": [
                    "Given the user has a valid account",
                    "When valid credentials are entered",
                    "Then the user should be logged in"
                ]
            }
        ]
    }
    """
       
        if "effort_estimation-02" in prompt.lower():
            return """
    {
        "complexity": "Medium",
        "story_points": 13,
        "estimated_days": 8,
        "assumptions": [
            "Single user role",
            "Standard authentication",
            "No third-party integrations"
        ],
        "risks": [
            "Authentication requirements may change",
            "Additional user roles may increase scope"
        ]
    }
    """
       
        if "review-01" in prompt.lower():
            return """
    {
        "quality_score": 8,
        "strengths": [
            "Requirements are clearly identified",
            "User stories follow standard format",
            "Acceptance criteria are available"
        ],
        "issues": [
            "Non-functional requirements are missing",
            "Security requirements are not defined"
        ],
        "recommendations": [
            "Add performance requirements",
            "Add security requirements",
            "Consider accessibility requirements"
        ]
    }
    """
       
        if "refinement" in prompt.lower():
            return """{
  "improvements": [
    "Define password policy",
    "Define MFA requirements",
    "Add performance requirements",
    "Add accessibility considerations"
  ],
  "final_quality_score": 9
}"""

        return """
        {
            "actors": ["Customer"],
            "modules": [
                "Registration",
                "Authentication",
                "Order Management",
                "Invoice Management"
            ],
            "functional_requirements": [
                "User Registration",
                "User Login",
                "View Orders",
                "Download Invoices"
            ]
        }
        """