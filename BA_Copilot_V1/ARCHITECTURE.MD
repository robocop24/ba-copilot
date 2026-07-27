# BA Copilot V1 — Architecture Reference

## Overview

BA Copilot V1 is a **multi-agent AI pipeline** that automates Business Analyst deliverables from a raw requirement document. It runs 7 specialized agents sequentially through a `WorkflowOrchestrator`, accumulating outputs in a shared `WorkflowState`, and producing a structured JSON BA report. A Streamlit UI (`app.py`) is also provided for interactive artifact exploration.

---

## High‑Level Architecture

```
                 ┌──────────────────────┐
                 │ Requirement Document │
                 │ (.txt / .pdf / .docx)│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Document Processor  │  → plain text
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Workflow Orchestrator│  ← runs agents sequentially
                 └──────────┬───────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                     Agent Pipeline                           │
├──────────────────────────────────────────────────────────────┤
│  1. RequirementAnalyzer      → actors, modules, requirements │
│         ↓                                                    │
│  2. UserStoryAgent           → user stories                  │
│         ↓                                                    │
│  3. AcceptanceCriteriaAgent  → Given-When-Then criteria      │
│         ↓                                                    │
│  4. GapAnalysisAgent         → gaps, clarification questions │
│         ↓                                                    │
│  5. EffortEstimationAgent    → complexity, story points, days│
│         ↓                                                    │
│  6. ReviewAgent              → quality score, issues         │
│         ↓                                                    │
│  7. RefinementAgent          → improvements, final score     │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   WorkflowState      │  ← mutable data bag
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  outputs/            │
                 │  ba_report.json      │
                 └──────────────────────┘
```

---

## Core Components

### 1. Document Processor (`document/document_processor.py`)

Ingests requirement documents and outputs plain text.

| Format | Library | Method |
|--------|---------|--------|
| `.txt` | `pathlib` | `Path.read_text(encoding="utf-8")` |
| `.pdf` | `PyPDF2` | `PdfReader` → iterate pages → extract text |
| `.docx` | `python-docx` | `Document` → join paragraph texts |

Unsupported formats raise `ValueError`.

---

### 2. Workflow Orchestrator (`workflow/orchestrator.py`)

The central coordinator. Instantiates all 7 agents in `__init__` and runs the sequential pipeline:

```python
def run(self, requirement: str) -> WorkflowState:
    state = WorkflowState()
    state.analysis          = self.analyzer.analyze(requirement)
    state.stories           = self.user_story_agent.generate(state.analysis)
    state.acceptance_criteria = self.acceptance_criteria_agent.generate(state.stories)
    state.story_gaps        = self.gap_analysis_agent.generate(state.stories)
    state.effort_estimation = self.effort_agent.generate(composite)
    state.review            = self.review_agent.generate(composite)
    state.refinement        = self.refinement_agent.generate(state.review)
    return state
```

- **Linear, non‑branching** — no conditional logic or error handling.
- Each agent receives the accumulated output of previous agents.

---

### 3. Workflow State (`workflow/state.py`)

A mutable plain‑class container (no Pydantic, no typing):

```python
class WorkflowState:
    analysis: dict | None
    stories: dict | None
    acceptance_criteria: dict | None
    story_gaps: dict | None
    effort_estimation: dict | None
    review: dict | None
    refinement: dict | None
```

`to_dict()` serializes all attributes for JSON output. No validation — purely a data bag.

---

### 4. Base Agent (`agents/base_agent.py`)

Common parent for all agents:

```python
class BaseAgent:
    def __init__(self, prompt_file: str):
        self.prompt_template = Path("prompts/prompt_file").read_text()
        self.llm = ProviderFactory.get_provider()
```

- Loads a prompt `.txt` file at construction time.
- Obtains an LLM provider from the `ProviderFactory`.
- Child classes call `self.llm.generate(prompt)` and `json.loads()` the response.

---

### 5. LLM Provider System (`core/`)

#### `core/llm.py` — `LLMProvider` (abstract base)
```python
class LLMProvider:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
```
Pure contract — no implementation.

#### `core/mock_provider.py` — `MockLLMProvider`
Returns **hard‑coded JSON** based on keyword matching in the prompt:

| Prompt keyword | Returns |
|----------------|---------|
| `agent_type:user_stories` | User stories JSON |
| `gap_analysis` | Gaps + clarification questions |
| `agent_type:acceptance_criteria` | Acceptance criteria JSON |
| `effort_estimation-02` | Effort estimation JSON |
| `review-01` | Review JSON |
| `refinement` | Refinement JSON |
| *(default)* | Analyzer JSON (actors, modules, requirements) |

**No real LLM is called.** Fully deterministic for testing/demo.

#### `core/provider_factory.py` — `ProviderFactory`
```python
class ProviderFactory:
    @staticmethod
    def get_provider():
        return MockLLMProvider()
```
Always returns the mock. Swap to a real provider by returning a different `LLMProvider` implementation.

---

## Agent Design (Details)

### Requirement Analyzer (`agents/analyzer.py`)
- **Prompt**: `prompts/analyzer.txt` — `{requirement}` placeholder
- **Method**: `analyze(requirement)`
- **Output**: `{"actors": [...], "modules": [...], "functional_requirements": [...]}`

### User Story Agent (`agents/user_story.py`)
- **Prompt**: `prompts/user_story.txt` — `{analysis}` placeholder
- **Method**: `generate(analysis)`
- **Output**: `{"user_stories": [{"story": "As a … I want … so that …"}, ...]}`

### Acceptance Criteria Agent (`agents/acceptance_criteria.py`)
- **Prompt**: `prompts/acceptance_criteria.txt` — `{stories}` placeholder
- **Method**: `generate(stories)`
- **Output**: `{"acceptance_criteria": [{"story": "...", "criteria": ["Given … When … Then …"]}, ...]}`

### Gap Analysis Agent (`agents/gap_analysis.py`)
- **Prompt**: `prompts/gap_analysis.txt` — `{analysis}` placeholder (though orchestrator passes `state.stories`)
- **Method**: `generate(analysis)`
- **Output**: `{"gaps": [...], "clarification_questions": [...]}`

### Effort Estimation Agent (`agents/effort_estimation.py`)
- **Prompt**: `prompts/effort_estimation.txt` — `{workflow_input}` placeholder
- **Method**: `generate(workflow_input)` — receives composite of analysis + stories + ACs
- **Output**: `{"complexity": "...", "story_points": N, "estimated_days": N, "assumptions": [...], "risks": [...]}`

### Review Agent (`agents/review.py`)
- **Prompt**: `prompts/review.txt` — `{workflow_output}` placeholder
- **Method**: `generate(workflow_output)` — receives composite of ALL previous outputs
- **Output**: `{"quality_score": N, "strengths": [...], "issues": [...], "recommendations": [...]}`

### Refinement Agent (`agents/refinement.py`)
- **Prompt**: `prompts/refinement.txt` — `{review_output}` placeholder
- **Method**: `generate(review_output)`
- **Output**: `{"improvements": [...], "final_quality_score": N}`

---

## Entry Points

### `main.py` — CLI
```python
def build_state(file_path="samples/requirement.txt"):
    text = DocumentProcessor().extract_text(file_path)
    orchestrator = WorkflowOchestrator()
    state = orchestrator.run(text)
    Path("outputs/ba_report.json").write_text(json.dumps(state.to_dict()))
    return state
```
Prints the JSON to stdout. Default input is `samples/requirement.txt`.

### `app.py` — Streamlit UI
Imports `build_state()` from `main.py`. Renders each artifact section in the browser:
- 🔍 Analysis
- 🧩 User Stories
- ✅ Acceptance Criteria
- ⚠️ Story Gaps
- ⏱ Effort Estimation
- 🧠 Review Summary
- 🔧 Refinement Suggestions
- 📥 Download button for `ba_report.json`

---

## V1 Status

| Feature | Status |
|---------|--------|
| Multi‑Agent Workflow | ✅ |
| Workflow Orchestration | ✅ |
| Workflow State Management | ✅ |
| Provider Factory Pattern | ✅ |
| Prompt Management | ✅ |
| JSON Report Generation | ✅ |
| Review & Refinement Loop | ✅ |
| Streamlit UI | ✅ |
| PDF/DOCX Support | ✅ |
| Real LLM Integration | Mock only (extensible) |
| Human‑in‑the‑Loop | ❌ (see V2) |
| Parallel Execution | ❌ (see V2) |
| State Persistence | ❌ (see V2) |

---

## Author

**Suhail Riyaz** — Agentic AI Enthusiast