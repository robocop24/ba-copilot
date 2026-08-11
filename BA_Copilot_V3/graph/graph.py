import json as _json
import sqlite3
from pathlib import Path

# Monkey-patch JsonPlusSerializer to add missing dumps/loads methods
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

if not hasattr(JsonPlusSerializer, 'dumps'):
    def _dumps(self, obj):
        return _json.dumps(obj, default=str)
    JsonPlusSerializer.dumps = _dumps
if not hasattr(JsonPlusSerializer, 'loads'):
    def _loads(self, data):
        if not data:
            return {}
        return _json.loads(data)
    JsonPlusSerializer.loads = _loads

# Register Pydantic models for msgpack checkpoint (de)serialization
_serde = JsonPlusSerializer().with_msgpack_allowlist([
    ("models.plan", "PlanOutput"),
    ("models.analysis", "AnalysisOutput"),
    ("models.story", "StoryOutput"),
    ("models.acceptance", "AcceptanceOutput"),
    ("models.estimation", "EstimationOutput"),
    ("models.gaps", "GapOutput"),
    ("models.review", "ReviewOutput"),
    ("models.refinement", "RefinementOutput"),
])

from nodes.acceptance_node import acceptance_node
from nodes.analyzer_node import analyzer_node
from nodes.approval_node import approval_node
from nodes.estimation_node import estimation_node
from nodes.gap_node import gap_node
from nodes.planner_node import planner_node
from nodes.refinement_node import refinement_node
from nodes.review_node import review_node
from nodes.story_node import story_node
from routers.approval_router import approval_router
from routers.planner_router import planner_router
from state import BAState

BASE_DIR = Path(__file__).parent.parent
conn = sqlite3.connect(str(BASE_DIR / 'ba_copilot_v3.db'), check_same_thread=False)
checkpointer = SqliteSaver(conn, serde=_serde)

builder = StateGraph(BAState)
builder.add_node('planner', planner_node)
builder.add_node('analyzer', analyzer_node)
builder.add_node('gap_analysis', gap_node)
builder.add_node('story', story_node)
builder.add_node('acceptance_criteria', acceptance_node)
builder.add_node('estimation', estimation_node)
builder.add_node('review', review_node)
builder.add_node('approval', approval_node)
builder.add_node('refinement', refinement_node)

builder.add_edge(START, 'planner')
builder.add_conditional_edges(
    "planner",
    planner_router,
    {
        "analyze_requirements": "analyzer",
        "done": END,
    }
)
builder.add_edge('analyzer', 'story')
builder.add_edge('analyzer', 'gap_analysis')
builder.add_edge('story', 'acceptance_criteria')
builder.add_edge('story', 'estimation')
builder.add_edge('acceptance_criteria', 'review')
builder.add_edge('estimation', 'review')
builder.add_edge('gap_analysis', 'review')
builder.add_edge('review', 'approval')
builder.add_conditional_edges(
    'approval',
    approval_router,
    {
        "refinement": "refinement",
        "end": END,
    })
builder.add_edge('refinement', 'planner')

graph = builder.compile(checkpointer=checkpointer)
