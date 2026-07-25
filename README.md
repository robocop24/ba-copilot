# BA Copilot - Agentic AI Business Analyst Assistant

A multi-agent AI system that automates Business Analyst activities, converting requirements into structured BA deliverables.

## 📋 Project Overview

BA Copilot generates:

- **Functional Requirements** — extracted from raw requirements
- **User Stories** — in standardized As-a/I-want/So-that format
- **Acceptance Criteria** — Given-When-Then scenarios
- **Gap Analysis** — identifies missing information, ambiguities, risks
- **Effort Estimation** — complexity, story points, effort breakdown
- **Quality Review** — evaluates generated artifacts for improvement
- **Refinement Recommendations** — uses review feedback to enhance deliverables
- **Human Approval Workflow** — LangGraph V2 supports human-in-the-loop interrupts

---

## 🎯 Quick Start

### For End-Users: Run V1 (Stable)

```bash
cd BA_Copilot_V1
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

### For Development: Run V2 (LangGraph + Checkpoints)

```bash
cd BA_Copilot_V2
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

---

## 📦 Version Comparison

| Feature | V1 | V2 |
|---------|----|----|
| **Framework** | Custom Orchestration | LangGraph |
| **State Management** | In-memory | TypedDict + Checkpointing |
| **Persistence** | JSON output only | SQLite checkpoints |
| **Human Approval** | Planned | ✅ Implemented with interrupts |
| **Resumable Workflows** | No | ✅ Yes (with thread IDs) |
| **Status** | Stable | Development |

---

## 🏗️ Architecture

### V1 — Custom Orchestration
- Sequential workflow orchestrated in `workflow/orchestrator.py`
- Direct agent-to-agent flow
- Outputs stored as JSON

### V2 — LangGraph Framework
- **Graph-based workflow** with typed state (`BAState`)
- **Checkpoint persistence** for resumable executions
- **Router-based conditionals** for approval workflow
- **Human-in-the-loop** approval node with `interrupt()` support
- **Thread-based execution** for stateful conversations

---

## 📂 Project Structure

```
BA_Copilot/
├── BA_Copilot_V1/              # Stable custom orchestration
│   ├── agents/                 # Analyzer, Reviewer, Refinement agents
│   ├── workflow/               # Orchestration logic
│   ├── core/                   # LLM provider abstraction
│   ├── requirements.txt        # V1 dependencies
│   └── README.md
│
├── BA_Copilot_V2/              # LangGraph development version
│   ├── nodes/                  # Graph nodes (retriever, analyzer, etc.)
│   ├── routers/                # Conditional edge routers
│   ├── models/                 # Pydantic output types
│   ├── tools/                  # Node-specific utilities
│   ├── state.py                # BAState TypedDict definition
│   ├── graph.py                # StateGraph with checkpoints
│   ├── main.py                 # Entry point with streaming + approval
│   ├── requirements.txt        # V2 dependencies (LangGraph, etc.)
│   └── README.md
│
├── .vscode/                    # VS Code workspace settings
├── .gitignore                  # Excludes .venv folders
└── README.md                   # This file
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
