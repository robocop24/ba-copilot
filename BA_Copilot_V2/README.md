# BA Copilot V2 — LangGraph Agentic Workflow

An agentic Business Analyst assistant built on **LangGraph**. It ingests a requirement document, analyzes it, generates user stories and gap analysis **in parallel**, reviews the output, pauses for **human approval**, and loops back for **refinement** if rejected — all with **SQLite checkpointing** for resumable execution.

---

## 🚀 Features

| Feature | Detail |
|---------|--------|
| **Graph‑based workflow** | 8 nodes connected via LangGraph `StateGraph` |
| **Fan‑out / fan‑in** | Stories and gap analysis run in parallel after analysis |
| **Human‑in‑the‑loop** | `interrupt()` pauses for manual approve/refine decision |
| **Refinement loop** | Rejected outputs loop back through review → refinement (capped at `max_iterations`) |
| **SQLite checkpoints** | Persists state to `ba_copilot.db` per `thread_id` |
| **Provider‑agnostic LLM** | DeepSeek via OpenAI‑compatible API; Ollama stub included |
| **Structured output** | All LLM responses validated against Pydantic models |
| **Robust JSON parsing** | Handles markdown code blocks, bare JSON, and malformed responses |

---

## 🧱 Workflow Graph

```
START
  │
  ▼
retriever                 ← hardcoded context (RAG‑ready stub)
  │
  ▼
analyze_requirements      ← LLM: actors, modules, requirements
  ╱           ╲
 ╱             ╲
▼                ▼
build_stories       gap_analysis    ← PARALLEL (fan‑out)
 ╲             ╱
  ╲           ╱
   ▼         ▼
 prepare_review           ← assembles review context (fan‑in)
      │
      ▼
 review_output            ← LLM: 1–10 score, strengths, weaknesses
      │
      ▼
 approval                 ← interrupt() — HUMAN decides
    ╱      ╲
   ╱        ╲
  ▼          ▼
 END       refinement_output  ← LLM rewrites stories per feedback
            │
            └──→ prepare_review (loop)
```

---

## 📦 Nodes

| Node | File | Description |
|------|------|-------------|
| `retriever` | `nodes/retriever.py` | Loads requirement + returns hardcoded BRD context (stub for RAG) |
| `analyze_requirements` | `nodes/analyzer.py` | LLM extracts actors, modules, functional requirements |
| `build_stories` | `nodes/stories.py` | LLM generates "As a … I want … so that …" user stories |
| `gap_analysis` | `nodes/gap_analysis.py` | LLM identifies gaps, edge cases, recommendations |
| `prepare_review` | `nodes/prepare_review.py` | Non‑LLM: combines stories + gaps into review context |
| `review_output` | `nodes/review.py` | LLM scores and critiques the BA artifacts |
| `approval` | `nodes/approval.py` | `interrupt()` — pauses for human yes/no |
| `refinement_output` | `nodes/refinement.py` | LLM rewrites stories based on review feedback |

---

## 🧩 State (`BAState`)

Defined in `state.py` as a `TypedDict` (all fields optional via `total=False`):

| Field | Type | Set By |
|-------|------|--------|
| `requirement` | `str` | `main.py` (initial state) |
| `context` | `str` | `retriever` |
| `analysis` | `AnalysisOutput` | `analyze_requirements` |
| `stories` | `StoriesOutput` | `build_stories` |
| `gaps` | `GapAnalysisOutput` | `gap_analysis` |
| `review_context` | `str` | `prepare_review` |
| `review` | `ReviewOutput` | `review_output` |
| `refinement` | `RefinementOutput` | `refinement_output` |
| `approved` | `bool` | `approval` (via human interrupt) |
| `iteration` | `int` | `main.py` (init) + `refinement_output` (increments) |
| `max_iterations` | `int` | `main.py` (initial state, defaults to 3) |

---

## 🧠 Models (Pydantic)

| Model | File | Fields |
|-------|------|--------|
| `AnalysisOutput` | `models/analysis.py` | `actors`, `modules`, `requirements` |
| `StoriesOutput` | `models/stories.py` | `user_stories` (list of strings) |
| `GapAnalysisOutput` | `models/gaps.py` | `gaps_found`, `gaps`, `recommendations` |
| `ReviewOutput` | `models/review.py` | `score` (1–10), `strengths`, `weaknesses`, `recommendations`, `approved` |
| `RefinementOutput` | `models/refinement.py` | `revised_stories`, `refinements`, `changes_summary` |

All models include `@field_validator` to parse string‑ified lists from the LLM.

---

## 🔀 Router

**`routers/approval_router.py`** — decides the next step after approval:

- `approved == True` → `"end"`
- `iteration >= max_iterations` → `"end"` (with warning)
- Otherwise → `"refine"` (loops back to refinement)

---

## 🛠️ LLM Provider System

| File | Role |
|------|------|
| `llm/base_provider.py` | Abstract base (`get_llm()`) |
| `llm/deepseek_provider.py` | `ChatOpenAI` pointed at DeepSeek API (JSON mode, temp=0) |
| `llm/ollama_provider.py` | Stub for local Ollama models |
| `llm/provider_factory.py` | Currently returns `DeepSeekProvider`; easy to swap |
| `llm/settings.py` | Loads `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `MODEL_NAME` from `.env` |

---

## 🛠️ Setup

### 1. Navigate & create environment
```bash
cd BA_Copilot_V2
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

### 2. Configure API key
```bash
cp .env.example .env
```
Edit `.env`:
```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

### 3. Prepare input
Place your requirement document at `input/requirement.txt`. Supported formats: `.txt`, `.pdf`, `.docx`.

---

## ▶️ Usage

```bash
python main.py
```

The workflow will:
1. Load `input/requirement.txt`
2. Stream through the graph until the **approval** node
3. Pause and ask: **"Approve BA Report? (yes/no)"**
4. If **no** → refines stories and loops back to review (up to 3 iterations)
5. If **yes** → prints final state and generates `ba_copilot_graph.png`

---

## 📁 Project Structure

```
BA_Copilot_V2/
├── main.py                         # Entry point (stream + interrupt + resume)
├── state.py                        # BAState TypedDict
├── graph.py                        # StateGraph builder + SQLite checkpointer
│
├── nodes/                          # Graph nodes
│   ├── retriever.py                # Loads requirement + context
│   ├── analyzer.py                 # LLM: actors, modules, requirements
│   ├── stories.py                  # LLM: user stories
│   ├── gap_analysis.py             # LLM: gaps + recommendations
│   ├── prepare_review.py           # Assembles review context
│   ├── review.py                   # LLM: quality score + feedback
│   ├── approval.py                 # interrupt() for human decision
│   └── refinement.py               # LLM: rewrites stories + increments iteration
│
├── models/                         # Pydantic data models
│   ├── analysis.py                 # AnalysisOutput
│   ├── stories.py                  # StoriesOutput
│   ├── gaps.py                     # GapAnalysisOutput
│   ├── review.py                   # ReviewOutput
│   └── refinement.py               # RefinementOutput
│
├── prompts/                        # Prompt templates ({placeholder} format)
│   ├── analyzer.txt
│   ├── user_story.txt
│   ├── gap_analysis.txt
│   ├── review.txt
│   ├── refinement.txt
│   ├── acceptance_criteria.txt     # (unused — from V1)
│   └── effort_estimation.txt       # (unused — from V1)
│
├── routers/
│   └── approval_router.py          # Conditional edge: end vs refine
│
├── llm/                            # LLM provider system
│   ├── base_provider.py            # Abstract base
│   ├── deepseek_provider.py        # DeepSeek via OpenAI-compatible API
│   ├── ollama_provider.py          # Local Ollama stub
│   ├── provider_factory.py         # Factory (currently → DeepSeek)
│   └── settings.py                 # .env loader
│
├── tools/
│   └── retriever.py                # Hardcoded BRD context (RAG-ready stub)
│
├── utils/
│   ├── prompt_loader.py            # Reads prompt .txt files
│   └── json_parser.py              # Safe LLM JSON extraction
│
├── document/
│   └── document_processor.py       # .txt / .pdf / .docx extraction
│
├── input/
│   └── requirement.txt             # Sample requirement
│
├── .env.example                    # Environment template
├── .gitignore
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

---

## 🔐 Security

- **API keys** live in `.env` — **never committed**. See `.gitignore`.
- The `.env.example` shows the format without real secrets.
- If a key is ever leaked, rotate it immediately on the DeepSeek dashboard.

---

## 🧪 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `langgraph` | ≥0.2.60, <0.4 | Graph‑based agent orchestration |
| `langgraph-checkpoint` | ≥2.0.10, <3.0 | State persistence |
| `langgraph-checkpoint-sqlite` | ≥2.0.3, <3.0 | SQLite backend for checkpoints |
| `langchain-openai` | ≥0.2, <0.3 | DeepSeek via OpenAI‑compatible API |
| `langchain-core` | ≥0.3, <0.4 | Core LangChain types |
| `pydantic` | ≥2, <3 | Data validation |
| `python-dotenv` | ≥1.0, <2.0 | .env loading |
| `PyPDF2` | ≥3.0, <4.0 | PDF text extraction |
| `python-docx` | ≥1.1, <2.0 | DOCX text extraction |

---

## 📝 License

MIT — feel free to use and modify.

```
BA_Copilot_V2/
├── main.py                 # Entry point; handles streaming & interrupts
├── state.py                # BAState TypedDict definition
├── graph.py                # Graph construction with nodes, edges, routers
├── ba_copilot_graph.png    # Visual representation of the workflow
│
├── nodes/                  # Individual workflow steps
│   ├── retriever.py        # loads requirement file → state["requirement"]
│   ├── analyzer.py         # LLM analysis → state["analysis"]
│   ├── stories.py          # LLM user story generation → state["stories"]
│   ├── gap_analysis.py     # LLM gap detection → state["gaps"]
│   ├── prepare_review.py   # assembles review context → state["review_context"]
│   ├── review.py           # LLM review & scoring → state["review"]
│   ├── approval.py         # interrupt() for human approval → state["approved"]
│   └── refinement.py       # refines stories based on review → state["refinement"]
│
├── models/                 # Pydantic output models
│   ├── analysis.py
│   ├── stories.py
│   ├── gaps.py
│   ├── review.py
│   └── refinement.py
│
├── prompts/                # Prompt templates (with {placeholders})
│   ├── analysis.txt
│   ├── user_story.txt
│   ├── gap_analysis.txt
│   ├── review.txt
│   └── refinement.txt
│
├── routers/
│   └── approval_router.py  # Conditional edge logic
│
├── llm/
│   ├── provider_factory.py # Creates LLM instance based on settings
│   └── settings.py         # Reads environment variables
│
├── utils/
│   ├── prompt_loader.py    # Loads .txt prompt files
│   └── json_parser.py      # Parses LLM JSON responses safely
│
├── document/               # Document processing utilities (optional)
│   └── document_processor.py
│
├── input/
│   └── requirement.txt     # Your raw requirement document
│
├── .env.example            # Template for environment variables
├── .env                    # (ignored) Actual secrets
├── .gitignore
└── requirements.txt        # Python dependencies
```

---

## 🔐 Security

- **API keys** are stored in `.env` and **never committed**. See `.env.example`.
- Run `git grep -i "sk-"` to ensure no key leaks.
- If you ever accidentally commit a key, rotate it immediately on the DeepSeek dashboard.

---

## 🧪 Dependencies (key)

- `langgraph >= 0.2.60`
- `langgraph-checkpoint >= 2.0.10`
- `langgraph-checkpoint-sqlite >= 2.0.3`
- `python-dotenv`
- `langchain-openai` (for DeepSeek‑compatible API)
- `pydantic`

See `requirements.txt` for the exact list.

---

## 📝 License

MIT – feel free to use and modify.
```