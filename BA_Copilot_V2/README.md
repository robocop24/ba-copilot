# BA Copilot V2 — LangGraph Implementation

## Overview

**BA Copilot V2** is the development version using **LangGraph**, a framework for building resilient, resumable AI workflows with human-in-the-loop approval gates.

### Why LangGraph?

- **Typed State** — `BAState` ensures data consistency across all nodes
- **Checkpoint Persistence** — SQLite stores workflow state for resumable execution
- **Human Interrupts** — approval node pauses workflow for human review
- **Thread-based Execution** — supports multiple parallel workflows with independent state
- **Event Streaming** — observe workflow progress in real-time

### Deliverables

The system converts requirements into:

- **Functional Requirements** — extracted from raw requirements
- **User Stories** — As-a/I-want/So-that format
- **Acceptance Criteria** — Given-When-Then scenarios
- **Gap Analysis** — missing information, ambiguities, risks
- **Effort Estimation** — complexity, story points, estimated effort
- **Quality Review** — evaluates artifacts for improvements
- **Refinement Recommendations** — uses review feedback to enhance output
- **Human Approval** — workflow pauses for review and approval

---

## Key Features

## Key Features

### 1. **Typed State Management**

All data flows through a strongly-typed `BAState`:

```python
class BAState(TypedDict):
    requirement: str              # Input requirement
    context: str                  # Retrieved context
    analysis: AnalysisOutput      # Actors, modules, requirements
    stories: StoriesOutput        # User stories
    review: ReviewOutput          # Quality score, recommendations
    refinement: RefinementOutput  # Improvements, final score
    approved: bool | None         # Human approval decision
```

### 2. **Graph-based Workflow**

`graph.py` defines a `StateGraph` with nodes and conditional routing:

```python
builder = StateGraph(BAState)
builder.add_node('retriever', retriever_node)
builder.add_node('analyze_requirements', analyzer_node)
builder.add_node('build_stories', stories_node)
builder.add_node('review_output', review_node)
builder.add_node('approval', approval_node)        # ← Human interrupt point
builder.add_node('refinement_output', refinement_node)

builder.add_edge(START, 'retriever')
builder.add_edge('review_output', 'approval')      # → Approval gate
builder.add_conditional_edges('approval', approval_router)  # Route on approval

graph = builder.compile(checkpointer=checkpointer)
```

### 3. **Checkpoint Persistence**

SQLite-backed checkpointing:

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect('ba_copilot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn)
graph = builder.compile(checkpointer=checkpointer)
```

**Benefits:**
- Save workflow state after each node
- Resume from the same point (with the same `thread_id`)
- Query history: `graph.get_state(config)`

### 4. **Human Approval Workflow**

Approval node uses `interrupt()` to pause:

```python
# In nodes/approval.py
from langgraph.types import interrupt

def approval_node(state: BAState):
    print("<<<< Approval node reached")
    approval = interrupt({
        "message": "Approval BA Report?"
    })
    return {"approved": approval}
```

Approval router decides path:

```python
# In routers/approval_router.py
def approval_router(state):
    approved = state["approved"]
    if approved:
        return "refinement_output"
    return END  # Stop if not approved
```

### 5. **Streaming + Resumable Execution**

`main.py` demonstrates full interrupt workflow:

```python
# Stream events to detect interrupts
for event in graph.stream({"requirement": "..."}, config=config):
    print(f"Event: {event}")

# Check if workflow was interrupted
state = graph.get_state(config)
if state.next:  # Paused at 'approval'
    user_input = input("Approve? (yes/no): ")
    approval = user_input == "yes"
    
    # Resume with user decision
    result = graph.invoke(Command(resume=approval), config=config)
```

### 6. **Thread-based Execution**

Each workflow run uses a unique `thread_id` for independent state:

```python
config = {
    "configurable": {
        "thread_id": "portal_project_v1"
    }
}

# This config persists across stream() and invoke() calls
graph.stream({...}, config=config)  # Run 1
graph.get_state(config)             # Query state
graph.invoke(Command(resume=True), config=config)  # Resume
```

---

## Agents & Nodes

Each workflow node is implemented in `nodes/` and processes the shared `BAState`:

| Node | Purpose | Input | Output |
|------|---------|-------|--------|
| **retriever** | Extracts context from requirement | `requirement` | `context` |
| **analyzer** | Identifies actors, modules, requirements | `context` | `analysis: AnalysisOutput` |
| **stories** | Generates user stories | `analysis` | `stories: StoriesOutput` |
| **review** | Evaluates quality, identifies improvements | `stories` | `review: ReviewOutput` |
| **approval** | **[INTERRUPT]** Prompts for human approval | `review` | `approved: bool` |
| **refinement** | Applies refinements based on review + approval | `review, approved` | `refinement: RefinementOutput` |

---

## Architecture

### Workflow Execution Flow

```
Input: Requirement
         ↓
    [retriever]
    Extract context from requirement
         ↓
    [analyzer]
    Identify actors, modules, requirements
         ↓
    [build_stories]
    Generate user stories
         ↓
    [review_output]
    Evaluate quality and identify improvements
         ↓
    [approval] ← **INTERRUPT: Await human approval**
         ↓
    [approval_router] → Conditional routing based on approval
         ├─ approved=True  → [refinement_output]
         └─ approved=False → END
         ↓
    [refinement_output]
    Apply improvements based on review
         ↓
    Output: BA Report (JSON)
```

### Graph Compilation & Checkpointing

```python
# graph.py
conn = sqlite3.connect('ba_copilot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn)

builder = StateGraph(BAState)
# ... add nodes and edges ...
graph = builder.compile(checkpointer=checkpointer)
```

**Checkpoint Persistence:**
- After each node execution, state is saved to SQLite
- Workflow can be resumed from `state.next` node
- Multiple parallel workflows isolated by `thread_id`

---

## Project Structure

```text
BA_Copilot_V2/
│
├── nodes/                    # Graph nodes
│   ├── retriever.py         # Extract context
│   ├── analyzer.py          # Analyze requirements
│   ├── stories.py           # Generate user stories
│   ├── review.py            # Quality review
│   ├── approval.py          # Human approval interrupt
│   └── refinement.py        # Apply refinements
│
├── routers/                 # Conditional edge routing
│   └── approval_router.py   # Route based on approval decision
│
├── models/                  # Pydantic output types
│   ├── analysis.py          # AnalysisOutput
│   ├── stories.py           # StoriesOutput
│   ├── review.py            # ReviewOutput
│   └── refinement.py        # RefinementOutput
│
├── tools/                   # Utilities (LLM calls, parsing)
│
├── state.py                 # BAState TypedDict definition
├── graph.py                 # StateGraph with checkpoints
├── main.py                  # Entry point (stream + approval)
├── requirements.txt         # V2 dependencies
├── ba_copilot.db           # SQLite checkpoint store
├── samples/
│   └── requirement.txt      # Sample input
└── README.md                # This file
```

---

## Setup

### Prerequisites

- **Python 3.11+** (required for modern LangGraph features)
- **Git** (for version control)

### Environment Isolation

**Important**: This is the V2 development environment. Keep it isolated from V1:

- **V1**: Use `../BA_Copilot_V1/.venv`
- **V2**: Use `./BA_Copilot_V2/.venv` (this folder)

### Installation

1. Create and activate a separate virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install V2-only dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Verify the graph can be imported:

```powershell
python -c "import graph; print('Graph loaded successfully')"
```

### Verify Checkpoint Database

The first run will create `ba_copilot.db` automatically. To reset:

```powershell
Remove-Item ba_copilot.db -ErrorAction SilentlyContinue
```

---

## Usage

### Run the Workflow with Approval

The main entry point `main.py` demonstrates the complete workflow including human approval:

```powershell
python main.py
```

**What happens:**

1. **Stream execution** — workflow runs and outputs events for each node
2. **Approval pause** — workflow pauses at the `approval` node with an `__interrupt__` event
3. **Checkpoint saved** — state is persisted to `ba_copilot.db`
4. **User prompt** — `Approve BA Report? (yes/no):` prompts for decision
5. **Resumable** — based on approval, workflow either:
   - **Approved** → continue to `refinement_output` node
   - **Rejected** → end workflow

**Expected output:**

```
Starting workflow...
Event: {'retriever': {...}}
Event: {'analyze_requirements': {...}}
Event: {'build_stories': {...}}
Event: {'review_output': {...}}
<<<< Approval node reached
Event: {'__interrupt__': (Interrupt(...))}

Current state after stream: StateSnapshot(...)
Interrupt detected. Nodes pending: ('approval',)
Approve BA Report? (yes/no): yes

User approval: True
<<<< Approval node reached
Resumed workflow result: {..., 'approved': True}

RESULT
==================================================
{'requirement': ..., 'approved': True, ...}
```

### Resume a Paused Workflow

To resume a previously paused workflow (using the same `thread_id`):

```python
from graph import graph
from langgraph.types import Command

config = {"configurable": {"thread_id": "portal_project"}}

# Check state
state = graph.get_state(config)
print(f"Next node: {state.next}")

# Resume with decision
result = graph.invoke(Command(resume=True), config=config)
```

### Query Workflow History

```python
from graph import graph

config = {"configurable": {"thread_id": "portal_project"}}

# Get current state
state = graph.get_state(config)
print(f"Values: {state.values}")
print(f"Next: {state.next}")
print(f"Metadata: {state.metadata}")
```

### Change Input Requirement

Edit `samples/requirement.txt` or modify `main.py`:

```python
# In main.py
result = graph.invoke({
    "requirement": "Your custom requirement here"
}, config=config)
```

---

## Development

### Adding a New Node

1. Create `nodes/my_node.py`:

```python
from state import BAState
from models.some_model import SomeOutput

async def my_node(state: BAState) -> dict:
    """Process state and return updates."""
    # Your logic
    return {"key": SomeOutput(...)}
```

2. Add to `graph.py`:

```python
from nodes.my_node import my_node

builder.add_node('my_node', my_node)
builder.add_edge('previous_node', 'my_node')
```

### Adding Conditional Routing

1. Create `routers/my_router.py`:

```python
from state import BAState

def my_router(state: BAState) -> str:
    if condition:
        return "node_a"
    return "node_b"
```

2. Add to `graph.py`:

```python
from routers.my_router import my_router

builder.add_conditional_edges('source_node', my_router)
```

### Running with Custom Thread ID

```python
config = {
    "configurable": {
        "thread_id": "my_custom_thread_id"
    }
}

for event in graph.stream(input_state, config=config):
    print(event)
```

---

## Database & Checkpoints

### SQLite Schema

The checkpoint database uses LangGraph's default schema:

```sql
-- Checkpoints table (auto-created by SqliteSaver)
CREATE TABLE checkpoints (
    thread_id TEXT,
    checkpoint_id TEXT,
    timestamp TEXT,
    data TEXT,
    PRIMARY KEY (thread_id, checkpoint_id)
);
```

### Clear Checkpoints

To reset all checkpoints:

```powershell
Remove-Item ba_copilot.db -ErrorAction SilentlyContinue
python main.py  # Will create a fresh database
```

To reset for a specific thread:

```python
# Checkpoint deletion currently requires direct DB manipulation
# or running with a new thread_id
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'langgraph'`

Ensure you activated the V2 virtual environment and installed dependencies:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Workflow Never Interrupts

Make sure `main.py` uses `graph.stream()` instead of `graph.invoke()`:

```python
# ✅ Correct: Uses stream for interrupts
for event in graph.stream({...}, config=config):
    pass

# ❌ Wrong: Bypasses interrupts
graph.invoke({...}, config=config)
```

### Database Locked

If you see "database is locked", ensure:
- Only one Python process is using `ba_copilot.db`
- The connection is not closed prematurely
- Try: `Remove-Item ba_copilot.db` and restart

---

---

## Comparison with V1

| Aspect | V1 | V2 |
|--------|----|----|
| Framework | Custom orchestration | LangGraph |
| State | In-memory dict | Typed `BAState` |
| Persistence | JSON files only | SQLite checkpoints |
| Approval | Placeholder | ✅ Implemented with interrupts |
| Resumable | No | ✅ Yes (with thread IDs) |
| Streaming | No | ✅ Yes (event-based) |
| Maturity | Production | Development |

---

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Parent README](../README.md) — Version comparison and overview
- [V1 README](../BA_Copilot_V1/README.md) — Stable version

---

## Author

Suhail Riyaz  
Agentic AI Enthusiast

---

## License

[Add license information if applicable]
