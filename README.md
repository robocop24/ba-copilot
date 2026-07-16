# BA Copilot - Agentic AI Business Analyst Assistant

## Overview

BA Copilot is a multi-agent AI system that automates common Business Analyst activities from a requirement document.

The system converts business requirements into structured BA deliverables such as:

- Functional Requirements
- User Stories
- Acceptance Criteria
- Gap Analysis
- Effort Estimation
- Quality Review
- Refinement Recommendations

---

## Features

### Requirement Analyzer Agent
Extracts:

- Actors
- Modules
- Functional Requirements

### User Story Agent

Generates user stories in the format:

As a <user>,
I want <goal>,
So that <benefit>

### Acceptance Criteria Agent

Generates Given-When-Then style acceptance criteria.

### Gap Analysis Agent

Identifies:

- Missing Information
- Ambiguities
- Risks
- Clarification Questions

### Effort Estimation Agent

Provides:

- Complexity
- Story Points
- Estimated Effort
- Assumptions
- Risks

### Review Agent

Evaluates generated BA artifacts and identifies improvement opportunities.

### Refinement Agent

Uses review feedback to recommend report improvements.

---

## Architecture

Workflow:

Requirement
→ Analyzer Agent
→ User Story Agent
→ Acceptance Criteria Agent
→ Gap Analysis Agent
→ Effort Estimation Agent
→ Review Agent
→ Refinement Agent
→ BA Report

---

## Project Structure

```text
ba-agent/
│
├── agents/
│
├── core/
│
├── document/
│
├── prompts/
│
├── workflow/
│
├── outputs/
│
└── main.py
```

---

## Key Design Concepts

### Workflow Orchestrator

Coordinates agent execution.

### Workflow State

Maintains application state between agents.

### Base Agent

Reusable parent class for all agents.

### Provider Factory

Centralized provider selection.

### Document Processor

Supports requirement ingestion.

---

## Technologies

- Python
- JSON
- Agentic Workflow Design
- Prompt Engineering
- Workflow Orchestration
- State Management

---

## Future Enhancements

- Real LLM Integration
- OpenAI Agent SDK Integration
- LangGraph Version
- PDF Support
- DOCX Support
- Streamlit UI
- RAG Integration
- Vector Database Support

---

## Sample Output

The system generates a structured BA report containing:

- Analysis
- Stories
- Acceptance Criteria
- Gap Analysis
- Effort Estimation
- Review
- Refinement

---

## Author

Suhail Riyaz
Agentic AI Enthusiast