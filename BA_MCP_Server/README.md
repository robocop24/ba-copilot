# BA MCP Server — Business Analyst Tools & Knowledge

A [FastMCP](https://gofastmcp.com) server that provides tools, resources, and prompts to support business analysis workflows. Used by **BA Copilot V3** as the tool backend for BRD retrieval, story point estimation, and requirement loading.

---

## 🛠️ Tools

| Tool | Description | Parameters |
|---|---|---|
| `retrieve_similar_brd` | Searches for similar BRD context based on a requirement description | `requirement: str` |
| `calculate_story_points` | Maps complexity labels to Fibonacci story points | `complexity: str` → `low`(2), `medium`(5), `high`(8), `very_high`(13) |
| `load_requirement` | Loads a requirement document from the filesystem | *(file path)* |

---

## 📦 Resources

- BA standards and checklists
- Prompt templates for user story generation and requirement review

---

## 🚀 Getting Started

```bash
cd BA_MCP_Server
pip install fastmcp

# Run as standalone server (stdio transport)
python server.py

# Or use FastMCP's CLI
fastmcp run server.py
```

---

## 🔗 Usage with BA Copilot V3

The V3 workflow connects to this server via `fastmcp.Client` with stdio transport:

```python
from fastmcp import Client

client = Client("BA_MCP_Server/server.py")
async with client:
    result = await client.call_tool("retrieve_similar_brd", {"requirement": "build portal"})
    print(result.content[0].text)
```

See `BA_Copilot_V3/mcp_client/client_wrapper.py` for the production wrapper.

---

## 📁 Structure

```
BA_MCP_Server/
├── server.py          # FastMCP server entry point
├── tools/             # MCP tool implementations
│   ├── retrieve_similar_brd.py
│   ├── calculate_story_points.py
│   └── load_requirement.py
├── resources/         # BA knowledge resources
├── prompts/           # Prompt templates
├── utils/             # Shared utilities
└── README.md
```
