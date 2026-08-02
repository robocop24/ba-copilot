def acceptance_standard() -> str:
    """Guidelines for writing effective acceptance criteria."""
    return """
Acceptance Criteria Best Practices:
------------------------------------
1. Write from the end-user's perspective
2. Use concrete, testable language (avoid "fast", "intuitive")
3. One criterion per line — never combine multiple checks
4. Cover both happy-path and edge cases
5. Include non-functional criteria where relevant (performance, security)
6. Use the Given/When/Then format for clarity
"""