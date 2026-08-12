# Challenge 2: Building a RAG Pipeline from Scratch

## The Problem

The MCP server's `retrieve_similar_brd` tool was backed by a hardcoded Python dictionary — 4 topics with 5 bullet points each. To make it useful for real BA workflows, it needed to retrieve relevant context from full BRD documents using semantic search.

## Design Decisions

```mermaid
flowchart TD
    A["❓ What kind of retrieval?"] --> B{"Choices"}
    B --> C["Keyword-only\n(no deep meaning)"]
    B --> D["Semantic-only\n(misses exact terms)"]
    B --> E["Hybrid\n✅ Best of both"]
    
    E --> F{"Chunking strategy?"}
    F --> G["Character-based\n(mid-word cuts)"]
    F --> H["Paragraph-based\n(works, inflexible)"]
    F --> I["Semantic\n✅ Splits where meaning shifts"]
    
    I --> J{"Vector index?"}
    J --> K["Brute-force\n(O(n), slow)"]
    J --> L["FAISS HNSW\n✅ O(log n), fast"]
```

## Chunking Evolution

| Version | Strategy | Chunks (4 files) | Quality |
|---|---|---|---|
| V1 | Character-based (100 chars, 20 overlap) | 331 | `"equirements"` — mid-word cuts |
| V2 | Paragraph-based (`\n\n` split) | 69 | Clean sections, headers preserved |
| V3 | Semantic (sentence embedding similarity) | ~69 | Splits where meaning shifts, merges undersized |

The semantic chunker uses `SentenceTransformer` to compare consecutive sentences. When cosine similarity drops below 0.5, a new chunk boundary is created.

## Two-Stage Retrieval Architecture

```mermaid
flowchart TD
    subgraph Indexing["📥 Indexing (startup)"]
        A["4 BRD .txt files"] --> B["Semantic Chunker"]
        B --> C["Metadata Enrichment\n(filename → project + module)"]
        C --> D["JSON Cache\n(freshness check via mtime)"]
    end

    subgraph Retrieval["🔍 Per Query"]
        E["User Query"] --> F["Query Enrichment\n(keyword → module filter)"]
        E --> G["Embedding\n(all-MiniLM-L6-v2, 384-dim)"]

        D --> H["Stage 1: FAISS HNSW ANN\n(top-N candidates from filtered subset)"]
        G --> H

        H --> I["Stage 2: Hybrid Re-Rank\n0.8 × cosine + 0.2 × keyword overlap"]
        G --> I
        F --> I

        I --> J["Top-K Results → LLM Agent"]
    end

    style J fill:#4CAF50,color:#fff
```

### Why Two Stages?

Running hybrid scoring (cosine + keyword) against all chunks is O(n). FAISS narrows the field to top-50 candidates in O(log n), then hybrid scoring re-ranks only those. At scale (100k+ chunks), this is the difference between milliseconds and seconds.

## Component Stack

| Layer | Technology | Purpose |
|---|---|---|
| Chunking | SentenceTransformer + sklearn | Split documents where meaning shifts |
| Metadata | Custom keyword mapping | Pre-filter by domain module before vector search |
| Embedding | `all-MiniLM-L6-v2` (384-dim) | Dense vector representations |
| Vector Index | FAISS IndexHNSWFlat | Approximate Nearest Neighbor search |
| Re-Ranking | Cosine similarity + word overlap | 80% semantic + 20% lexical scoring |
| Caching | JSON + `st_mtime` check | Auto-invalidate when source files change |

## Key Takeaway

> A production RAG pipeline is not just "embed and search." It's a layered system: chunking strategy → metadata pre-filtering → ANN candidate retrieval → hybrid re-ranking. Each layer addresses a different failure mode.
