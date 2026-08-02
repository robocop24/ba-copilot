def analyze_requirement(requirement: str) -> str:
    """Prompt template: perform a structured analysis of a requirement."""
    return f"""
You are a Senior Business Analyst. Perform a structured analysis of the requirement below.

Requirement: {requirement}

Your analysis must include:
1. **Stakeholders** — Who is impacted? (primary, secondary, tertiary)
2. **Business Value** — What measurable outcome does this deliver?
3. **Functional Scope** — What must the system do? What is explicitly out of scope?
4. **Dependencies** — Upstream/downstream systems, teams, or data sources needed.
5. **Risks & Assumptions** — Key unknowns and mitigation strategies.
6. **Success Metrics** — How will we know this is done and working? (KPIs)

Be concise but thorough. Use bullet points.
"""