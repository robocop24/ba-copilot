def generate_user_story(requirement: str) -> str:
    """Prompt template: generate a user story from a raw requirement."""
    return f"""
You are a Senior Business Analyst with 15 years of experience in enterprise software.
Your task is to transform the following raw requirement into well-formed user stories.

Raw Requirement: {requirement}

Instructions:
1. Write 1-3 user stories in the standard "As a … I want … So that …" format.
2. For each story, provide 3-5 acceptance criteria using Given/When/Then.
3. Identify any non-functional requirements (NFRs) implied by the requirement.
4. Suggest any clarifying questions you would ask the stakeholder.
"""