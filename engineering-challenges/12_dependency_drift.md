# Challenge 12: Dependency Drift — Docker Built Different Versions Than the Local Venv

## The Problem

The app ran fine locally, but the first `docker run` crashed instantly:

```
AttributeError: 'JsonPlusSerializer' object has no attribute 'with_msgpack_allowlist'
```

The local venv had `langgraph-checkpoint 4.1.1`, where that method exists. The
container had installed **2.x**, where it doesn't. Same `requirements.txt`, two
different worlds.

## Root Cause 1: loose ranges freeze nothing

`requirements.txt` used ranges, not pins:

```txt
langgraph>=0.2.60,<0.4
langgraph-checkpoint>=2.0.10,<3.0
langgraph-checkpoint-sqlite>=2.0.3,<3.0
langchain-openai>=0.2,<0.3
langchain-core>=0.3,<0.4
```

A range only says "any version in this window". The local venv was installed months
ago and froze at whatever was newest *then*. A fresh `docker build` re-runs `pip
install` and grabs the newest version *now*. The window was wide enough that "then"
and "now" resolved to incompatible APIs.

| Package | Local venv | Docker (fresh) |
|---|---|---|
| `langgraph` | 1.2.9 | 0.3.x (from `>=0.2.60,<0.4`) |
| `langgraph-checkpoint` | 4.1.1 | 2.x (from `>=2.0.10,<3.0`) |
| `langchain-core` | 1.5.1 | 0.3.x (from `>=0.3,<0.4`) |

`with_msgpack_allowlist` only exists in the checkpoint **4.x** API — hence the crash.

## Root Cause 2: a silently inconsistent local venv

Pinning to the local versions didn't end it. The next build failed with a resolver
conflict:

```
The user requested langgraph-checkpoint==4.1.1
langgraph 1.2.9 depends on langgraph-checkpoint<5.0.0 and >=4.1.0
langgraph-checkpoint-sqlite 2.0.11 depends on langgraph-checkpoint<3.0.0 and >=2.0.21
```

The local venv was itself **metadata-inconsistent**:

| Package | Local version | Actually requires |
|---|---|---|
| `langgraph-checkpoint` | 4.1.1 | — |
| `langgraph-checkpoint-sqlite` | 2.0.11 | checkpoint `<3.0` ❌ |
| `langchain-openai` | 0.2.14 | `langchain-core <0.4` ❌ |
| `langchain-core` | 1.5.1 | — |

These coexist locally only because packages were upgraded **one at a time** — `pip
install langgraph --upgrade` bumps `langgraph` + `langgraph-checkpoint` but leaves the
separately-installed `langgraph-checkpoint-sqlite` and `langchain-openai` untouched.
`pip` never re-validates the whole set after a partial upgrade, and Python happily
imports code whose metadata says it shouldn't work together.

The local "it works" was luck — the *code* happened to be forward-compatible even
though the *metadata* said otherwise. Docker's fresh install uses pip's strict
resolver, which refuses to reproduce an inconsistent state.

## The Fix: pin exact versions, and make them consistent

Resolve the whole set with pip in dry-run mode first (no install, just resolution):

```powershell
python -m pip install --dry-run --ignore-installed \
  langgraph==1.2.9 langgraph-checkpoint==4.1.1 langgraph-checkpoint-sqlite \
  langchain-openai
```

That revealed the compatible versions, which were then pinned:

```txt
langgraph==1.2.9
langgraph-checkpoint==4.1.1
langgraph-checkpoint-sqlite==3.1.1   # 2.0.11 → 3.1.1 (supports checkpoint 4.x)
langchain-openai==1.6.0               # 0.2.14 → 1.6.0 (supports core 1.x)
langchain-core==1.6.1                 # 1.5.1  → 1.6.1
```

And the local venv was reconciled so it stops drifting from the container:

```powershell
python -m pip install -r requirements.txt
```

## Key Takeaway

> Loose version ranges in `requirements.txt` are a promise you'll never keep — the
> local venv freezes at one point in time while a fresh build resolves to another.
> Pin direct dependencies with `==`, use `pip install --dry-run` to find a consistent
> set, and treat a Docker/CI build as the canary that exposes the drift your local
> environment has been hiding.

## Side effect worth remembering

`pip` only checks the packages you're touching. Upgrade one package and its new
dependencies silently break the metadata of the ones you *didn't* upgrade. The fix
isn't "make Docker match my venv" — it's "make both match a single, resolvable,
pinned `requirements.txt`."

## Act 2: the same drift, in the ML stack

The full image also installs the RAG stack from `BA_MCP_Server/requirements.txt`,
which contained:

```txt
numpy>=1.26,<2
```

On the container's Python 3.13, `numpy<2` resolves to **1.26.4 — which has no
cp313 wheel**. pip fell back to compiling from source, and `python:3.13-slim`
ships no C compiler:

```
ERROR: Unknown compiler(s): [['cc'], ['gcc'], ['clang'], ...]
```

The local venv actually ran **numpy 2.5.2** — the `<2` cap was stale (written back
when the project targeted an older Python). Fixed by pinning to reality:

| Package | Old pin | New pin |
|---|---|---|
| `numpy` | `>=1.26,<2` | `==2.5.2` |
| `sentence-transformers` | `>=3.0` | `==5.7.0` |
| `faiss-cpu` | `>=1.9` | `==1.15.0` |
| `scikit-learn` | `>=1.3` | `==1.9.0` |

## Act 3: a dependency that was never declared

Past numpy, `docker run` failed again:

```
from langchain.agents import create_agent
ModuleNotFoundError: No module named 'langchain'
```

`analyzer_agent` and `estimation_agent` import `langchain`. The local venv had
`langchain 1.3.14` installed — but it was **never written into requirements.txt**.
It worked locally because it happened to be present; a clean install has no way to
know it's needed.

Two extra lessons:

1. `create_agent` is **not** in `langgraph.prebuilt` in this version — it lives in
   `langchain.agents`. So "just import it from langgraph instead" was not an option.
2. `pip show langchain` proves the package is present locally, but nothing tells you
   it was never declared. The only reliable check is a clean install (Docker/CI).

The fix was `langchain==1.3.14`. (Installed as a separate Docker `RUN` step at
first, so the heavy torch layer stayed cached — the proper long-term fix is adding
it to `requirements.txt`.)

## Act 4: CPU vs CUDA torch

Once everything ran, `docker images` reported **9.83 GB**. The torch wheel pip chose:

```
torch 2.14.0+cu130
```

The `+cu130` suffix is the **CUDA** build (~3 GB) — in a container with no GPU.
`pip install torch` on Linux defaults to CUDA unless told otherwise:

```dockerfile
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
```

CPU-only torch is ~250 MB, cutting the image from ~10 GB to ~3.5 GB.

## The meta-pattern

Every failure was "works locally, breaks in Docker", each with a different face:

| Symptom | Real cause |
|---|---|
| `AttributeError: with_msgpack_allowlist` | loose range → old version |
| pip resolver conflict | locally inconsistent pins |
| `Unknown compiler(s)` (numpy source build) | pin with no wheel for this Python |
| `No module named 'langchain'` | installed but never declared |
| 9.83 GB image | CUDA torch default on Linux |
| `Unsupported provider` | `.env` values quoted — `python-dotenv` strips them, Docker's `--env-file` doesn't |

None of these showed up locally, because a venv is a frozen accident, not a spec.
The container is the spec — make it match reality, not the other way around.
