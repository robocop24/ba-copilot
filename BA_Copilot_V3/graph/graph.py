import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
# Monkey-patch JsonPlusSerializer to add missing dumps/loads methods
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
import json as _json
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
from state import BAState
from nodes.planner_node import planner_node
from nodes.analyzer_node import analyzer_node
from nodes.gap_node import gap_node
from nodes.story_node import story_node
from nodes.review_node import review_node
from nodes.approval_node import approval_node
from nodes.refinement_node import refinement_node
from routers.planner_router import planner_router
from routers.approval_router import approval_router

conn = sqlite3.connect('ba_copilot_v3.db', check_same_thread=False)
checkpointer = SqliteSaver(conn)

builder = StateGraph(BAState)
builder.add_node('planner', planner_node)
builder.add_node('analyzer', analyzer_node)
builder.add_node('gap_analysis', gap_node)
builder.add_node('story', story_node)
builder.add_node('review', review_node)
builder.add_node('approval', approval_node)
builder.add_node('refinement', refinement_node)

builder.add_edge(START, 'planner')
builder.add_conditional_edges(
    "planner",
    planner_router,
    {
        "analyze_requirements": "analyzer",
        "gap_analysis": "gap_analysis",
        "done": END,
    }
)
builder.add_edge('analyzer', 'story')
builder.add_edge('analyzer', 'gap_analysis')
builder.add_edge('story','review')
builder.add_edge('gap_analysis','review')
builder.add_edge('review', "approval")
builder.add_conditional_edges(
    'approval', 
    approval_router,
    {
        "refinement":"refinement",
        "end":END
    })

graph = builder.compile(checkpointer=checkpointer)
