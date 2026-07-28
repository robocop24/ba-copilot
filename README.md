# BA Copilot — Agentic AI Business Analyst Assistant

**BA Copilot** is a multi-agent AI system that automates the full Business Analyst workflow. It ingests raw requirement documents (`.txt`, `.pdf`, `.docx`) and produces structured BA deliverables — analysis, user stories, gap analysis, quality review, and iterative refinements.

> Three implementations are provided:
> - **V1** — Stable, custom orchestration + Streamlit UI
> - **V2** — LangGraph-based with human-in-the-loop approval and SQLite checkpointing
> - **V3** ⭐ — **Current.** Production LangGraph workflow with planner routing, tool-calling agents, auto-retry validation, and iterative refinement loop

---

## 🧠 What It Produces

| Artifact | Description |
|---|---|
| **Analysis** | Actors, modules, and functional requirements extracted from raw input |
| **User Stories** | Standardized "As a … I want … so that …" format |
| **Acceptance Criteria** | Given‑When‑Then scenarios for each story |
| **Gap Analysis** | Missing information, ambiguities, edge cases, and clarification questions |
| **Effort Estimation** | Complexity, story points, estimated days, assumptions, and risks |
| **Quality Review** | 1–10 score with strengths, weaknesses, and recommendations |
| **Refinement** | Revised stories and a summary of changes based on review feedback |
| **Human Approval** | V2 pauses the graph for manual approve/refine decision (with iteration cap) |

---

## 🎯 Quick Start

### V3 ⭐ — LangGraph Production Workflow (Recommended)

```bash
cd BA_Copilot_V3
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows
pip install -r requirements.txt
cp .env.example .env                # then add your DEEPSEEK_API_KEY
python main.py                      # full automated workflow
```

### V1 — Stable (Custom Orchestration + Streamlit UI)

```bash
cd BA_Copilot_V1
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows
pip install -r requirements.txt
python main.py                      # CLI – writes outputs/ba_report.json
streamlit run app.py                # Browser UI
```

### V2 — LangGraph (Human‑in‑the‑Loop + Checkpoints)

```bash
cd BA_Copilot_V2
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows
pip install -r requirements.txt
cp .env.example .env                # then add your DEEPSEEK_API_KEY
python main.py                      # interactive approval prompt
```

---

## 📦 Version Comparison

| Feature | V1 | V2 | V3 ⭐ |
|---|---|---|---|
| **Framework** | Custom sequential pipeline | LangGraph `StateGraph` | LangGraph `StateGraph` |
| **LLM Backend** | Mock provider (deterministic) | DeepSeek via OpenAI API | DeepSeek via OpenAI API |
| **Planner** | ❌ None | ❌ Fixed linear flow | ✅ Dynamic router (analyzer / gap / done) |
| **Agent Pattern** | One-shot LLM calls | One-shot LLM calls | Shared `invoke_with_validation` + auto-retry |
| **Tool-calling Agent** | ❌ | ❌ | ✅ ReAct agent with `retrieve_similar_brd` |
| **Parallelism** | ❌ Sequential only | ✅ Stories + Gap in parallel | ✅ Stories + Gap in parallel |
| **Refinement Loop** | ❌ Manual | ✅ Human-in-the-loop | ✅ Automatic approval router + iteration cap |
| **State** | Plain `WorkflowState` class | Typed `BAState` (TypedDict) | Typed `BAState` (TypedDict) with all outputs |
| **Persistence** | JSON file | SQLite checkpointing | SQLite checkpointing |
| **UI** | Streamlit (`app.py`) | CLI only | CLI only |
| **Status** | ✅ Stable | 🚧 Active Development | ⭐ **Current** |

---

## 🏗️ Architecture at a Glance

### V3 ⭐ — Planner-Routed LangGraph with Tool-Calling Agent

```mermaid
graph TD
    START --> planner

    planner -->|analyze_requirements| analyzer
    planner -->|gap_analysis| gap_analysis
    planner -->|done| END

    analyzer --> story
    analyzer --> gap_analysis

    story --> review
    gap_analysis --> review

    review --> approval

    approval -->|refinement| refinement
    approval -->|end| END
```

The **planner** dynamically routes based on the requirement. The **analyzer** is a ReAct agent with a BRD knowledge retrieval tool. **Story** and **gap_analysis** run in parallel, then converge at **review**. The **approval router** enables automatic iterative refinement with an iteration cap.

### V1 — Linear Agent Pipeline

```
Requirement.txt  →  DocumentProcessor  →  Orchestrator
  ┌──────────────────────────────────────────────────────┐
  │ Analyzer → Stories → AcceptanceCriteria → GapAnalysis │
  │ → EffortEstimation → Review → Refinement              │
  └──────────────────────────────────────────────────────┘
                                                    →  ba_report.json
```

### V2 — LangGraph Graph with Fan‑Out / Fan‑In

```
START → retriever → analyze_requirements
                         ╱            ╲
                  build_stories    gap_analysis
                         ╲            ╱
                      prepare_review
                            │
                       review_output
                            │
                         approval ←── human interrupt
                          ╱    ╲
                       END    refinement_output ──→ prepare_review (loop)
```

---

## 📂 Project Structure

```
ba-copilot/
├── README.md                       ← This file
│
├── BA_Copilot_V3/                  ⭐ Current — planner-routed LangGraph + tool-calling agents
│   ├── agents/                     │  6 agents (planner, analyzer, gap, story, review, refinement)
│   ├── nodes/                      │  7 graph nodes
│   ├── routers/                    │  planner_router + approval_router
│   ├── models/                     │  6 Pydantic output models
│   ├── prompts/                    │  6 prompt templates (.txt)
│   ├── llm/                        │  DeepSeek provider (OpenAI-compatible)
│   ├── tools/                      │  BRD knowledge retriever (ReAct agent tool)
│   ├── utils/                      │  invoke_with_validation, json_parser, prompt_loader
│   ├── document/                   │  Multi-format document processor
│   ├── graph/                      │  StateGraph definition + checkpointing
│   ├── input/                      │  Sample requirement files
│   ├── main.py                     │  Entry point
│   ├── state.py                    │  BAState TypedDict
│   ├── requirements.txt
│   └── README.md
│
├── BA_Copilot_V1/                  ← Stable: custom orchestration + Streamlit
│   ├── agents/                     │  7 specialty agents (analyzer, stories, etc.)
│   ├── core/                       │  LLM provider abstraction & mock provider
│   ├── document/                   │  Multi‑format document processor
│   ├── prompts/                    │  7 prompt templates (.txt)
│   ├── workflow/                   │  Orchestrator + WorkflowState
│   ├── samples/                    │  Sample input files
│   ├── outputs/                    │  Generated ba_report.json
│   ├── app.py                      │  Streamlit web UI
│   ├── main.py                     │  CLI entry point
│   ├── ARCHITECTURE.MD             │  Detailed architecture docs
│   └── README.md
│
├── BA_Copilot_V2/                  ← LangGraph: human‑in‑the‑loop + checkpoints
│   ├── nodes/                      │  8 graph nodes (retriever, analyzer, …)
│   ├── routers/                    │  Conditional routing (approval_router)
│   ├── models/                     │  Pydantic data models
│   ├── tools/                      │  Retriever stub (RAG‑ready)
│   ├── utils/                      │  JSON parser & prompt loader
│   ├── llm/                        │  Provider factory (DeepSeek + Ollama stub)
│   ├── document/                   │  Multi‑format document processor
│   ├── prompts/                    │  7 prompt templates (.txt)
│   ├── input/                      │  Input requirement files
│   ├── state.py                    │  BAState TypedDict
│   ├── graph.py                    │  StateGraph builder + SQLite checkpointer
│   ├── main.py                     │  Entry point (stream + interrupt + resume)
│   ├── .env.example                │  Environment template
│   └── README.md
│
└── .gitignore
```

---

## 🚀 Workflow

Both V1 and V2 follow the same logical flow:

```
Requirement
  ↓
Retriever (extracts context)
  ↓
Analyzer (identifies actors, modules, requirements)
  ↓
Story Generator (creates user stories)
  ↓
Reviewer (evaluates quality)
  ↓
[APPROVAL INTERRUPT] (V2 only)
  ↓
Refinement (improves based on review)
  ↓
BA Report Output
```

---

## 🔄 V2 Approval Workflow

V2 adds human-in-the-loop approval between review and refinement:

1. **Stream execution** — workflow runs via `graph.stream()` yielding events
2. **Detect interrupt** — approval node calls `interrupt()` and pauses
3. **Get state** — retrieve workflow state with `graph.get_state(config)`
4. **User input** — prompt for approval decision
5. **Resume** — continue with `graph.invoke(Command(resume=approved), config=config)`
6. **Persist** — SQLite checkpoint preserves state across sessions

---

## 🛠️ Development

### Adding New Nodes (V2)

Create a new node file in `nodes/`:

```python
from state import BAState

async def my_node(state: BAState) -> dict:
    """Process state and return updates."""
    # Your logic here
    return {"key": value}
```

Add to graph in `graph.py`:

```python
builder.add_node('my_node', my_node)
builder.add_edge('previous_node', 'my_node')
```

### Adding Conditional Routing (V2)

Create a router in `routers/`:

```python
def my_router(state: BAState) -> str:
    if condition:
        return "node_a"
    return "node_b"

# In graph.py:
builder.add_conditional_edges('source_node', my_router)
```

---

## 📝 Configuration

### Input Files

- **V1**: `samples/requirement.txt`
- **V2**: `samples/requirement.txt`

Modify `main.py` to use different input sources.

### LLM Provider (V2)

Update in `state.py` or environment:

```python
# Use OPENAI_API_KEY or other provider via core/provider_factory.py
```

---

## 🔐 Environment Isolation

**Important**: Each version uses its own virtual environment:

- `BA_Copilot_V1/.venv` — V1 dependencies only
- `BA_Copilot_V2/.venv` — V2 dependencies (LangGraph, etc.)

Never install V2 packages into V1's `.venv` or vice versa. Both folders are git-ignored for safety.

---

## 📖 Documentation

- [V1 README](./BA_Copilot_V1/README.md) — Setup and usage for stable version
- [V2 README](./BA_Copilot_V2/README.md) — LangGraph, checkpoints, and approval workflow

---

## 👤 Author

Suhail Riyaz  
Agentic AI Enthusiast

---

## 📄 License

[Add license information if applicable]
