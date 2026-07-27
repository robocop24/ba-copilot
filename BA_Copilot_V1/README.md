# BA Copilot V1 — Stable (Custom Orchestration)

A multi-agent AI pipeline that converts a business requirement document into a structured BA report (JSON). V1 uses a straightforward, sequential orchestration model with a **mock LLM provider** for deterministic, offline‑friendly execution. A **Streamlit UI** is included for interactive exploration of the generated artifacts.

---

## 🧠 Agents & Outputs

V1 runs **7 specialized agents** in order, each reading from the accumulated state:

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 1 | **Requirement Analyzer** | Raw requirement text | `actors`, `modules`, `functional_requirements` |
| 2 | **User Story Agent** | Analysis dict | `user_stories` (As a / I want / So that) |
| 3 | **Acceptance Criteria Agent** | Stories dict | `acceptance_criteria` (Given‑When‑Then) |
| 4 | **Gap Analysis Agent** | Stories dict | `gaps`, `clarification_questions` |
| 5 | **Effort Estimation Agent** | Analysis + Stories + ACs | `complexity`, `story_points`, `estimated_days`, `assumptions`, `risks` |
| 6 | **Review Agent** | All previous outputs | `quality_score`, `strengths`, `issues`, `recommendations` |
| 7 | **Refinement Agent** | Review dict | `improvements`, `final_quality_score` |

---

## 🏗️ Architecture

```
Requirement (.txt/.pdf/.docx)
        │
        ▼
  DocumentProcessor         ← PyPDF2 / python-docx / plain text
        │
        ▼
  WorkflowOrchestrator      ← runs agents sequentially, accumulates state
        │
        ├──→ RequirementAnalyzer  (prompts/analyzer.txt)
        ├──→ UserStoryAgent       (prompts/user_story.txt)
        ├──→ AcceptanceCriteriaAgent  (prompts/acceptance_criteria.txt)
        ├──→ GapAnalysisAgent     (prompts/gap_analysis.txt)
        ├──→ EffortEstimationAgent (prompts/effort_estimation.txt)
        ├──→ ReviewAgent          (prompts/review.txt)
        └──→ RefinementAgent      (prompts/refinement.txt)
        │
        ▼
  WorkflowState             ← mutable data bag (7 attributes)
        │
        ▼
  outputs/ba_report.json    ← final serialized JSON
```

### Key Components

| Component | File | Role |
|-----------|------|------|
| **Base Agent** | `agents/base_agent.py` | Loads prompt, initializes LLM — parent of all agents |
| **Provider Factory** | `core/provider_factory.py` | Returns `MockLLMProvider` (swap to real LLM here) |
| **Mock Provider** | `core/mock_provider.py` | Returns hard‑coded JSON based on prompt keywords |
| **LLM Provider** | `core/llm.py` | Abstract base class (`generate(prompt) → str`) |
| **Orchestrator** | `workflow/orchestrator.py` | Instantiates agents, runs pipeline, returns state |
| **Workflow State** | `workflow/state.py` | Mutable container with 7 named attributes |
| **Document Processor** | `document/document_processor.py` | `.txt` / `.pdf` / `.docx` → plain text |

---

## 🚀 Setup & Run

**Prerequisites**: Python 3.11+, keep V1 isolated from V2 (use separate `.venv`).

```powershell
cd BA_Copilot_V1
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### CLI

```powershell
python main.py
```

Reads `samples/requirement.txt`, runs all agents, writes `outputs/ba_report.json`, and prints the JSON to stdout.

### Streamlit UI

```powershell
streamlit run app.py
```

Opens a browser dashboard showing each artifact section (Analysis, Stories, ACs, Gaps, Effort, Review, Refinement) with a download button for the full JSON report.

---

## 📁 Project Structure

```
BA_Copilot_V1/
├── agents/
│   ├── base_agent.py              # Shared agent base class
│   ├── analyzer.py                # RequirementAnalyzer
│   ├── user_story.py              # UserStoryAgent
│   ├── acceptance_criteria.py     # AcceptanceCriteriaAgent
│   ├── gap_analysis.py            # GapAnalysisAgent
│   ├── effort_estimation.py       # EffortEstimationAgent
│   ├── review.py                  # ReviewAgent
│   └── refinement.py              # RefinementAgent
├── core/
│   ├── llm.py                     # Abstract LLMProvider
│   ├── mock_provider.py           # Deterministic mock (keyword‑based)
│   └── provider_factory.py        # Factory returning MockLLMProvider
├── document/
│   └── document_processor.py      # .txt / .pdf / .docx extraction
├── prompts/
│   ├── analyzer.txt
│   ├── user_story.txt
│   ├── acceptance_criteria.txt
│   ├── gap_analysis.txt
│   ├── effort_estimation.txt
│   ├── review.txt
│   └── refinement.txt
├── workflow/
│   ├── orchestrator.py            # Pipeline coordinator
│   └── state.py                   # WorkflowState container
├── samples/
│   └── requirement.txt            # Default input
├── outputs/
│   └── ba_report.json             # Generated BA report
├── app.py                         # Streamlit UI
├── main.py                        # CLI entry point
├── ARCHITECTURE.MD                # Detailed architecture reference
├── requirements.txt               # streamlit, python-docx, PyPDF2
└── README.md
```

---

## ⚙️ Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | 1.59.2 | Web UI |
| `python-docx` | 1.2.0 | DOCX parsing |
| `PyPDF2` | 3.0.1 | PDF parsing |

> **No LLM SDK dependency.** The mock provider returns hard‑coded JSON deterministically. To use a real LLM, implement `LLMProvider.generate()` and update `ProviderFactory`.

---

## 🔧 Customization

- **Change input file**: Edit `main.py` → `build_state()` or pass a different path.
- **Swap to a real LLM**: Implement `core/llm.py` → `LLMProvider.generate()`, update `core/provider_factory.py` to return your provider.
- **Add a new agent**: Create a class in `agents/`, inherit from `BaseAgent`, add a prompt in `prompts/`, and wire it into `workflow/orchestrator.py`.

---

## 👤 Author

Suhail Riyaz — Agentic AI Enthusiast