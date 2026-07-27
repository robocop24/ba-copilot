import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
# Monkey-patch JsonPlusSerializer to add missing dumps method
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
if not hasattr(JsonPlusSerializer, 'dumps'):
    def _dumps(self, obj):
        result = self.dumps_typed(obj)
        return result[0] if isinstance(result, tuple) else result
    JsonPlusSerializer.dumps = _dumps
from state import BAState
from nodes.retriever import retriever_node
from nodes.analyzer import analyzer_node
from nodes.stories import stories_node
from nodes.gap_analysis import gap_analysis_node
from nodes.prepare_review import prepare_review_node
from nodes.review import review_node
from nodes.refinement import refinement_node
from nodes.approval import approval_node
from routers.approval_router import approval_router

conn = sqlite3.connect('ba_copilot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn)

builder = StateGraph(BAState)
builder.add_node('retriever', retriever_node)
builder.add_node('analyze_requirements', analyzer_node)
builder.add_node('build_stories', stories_node)
builder.add_node('gap_analysis', gap_analysis_node)
builder.add_node('prepare_review', prepare_review_node)
builder.add_node('review_output', review_node)
builder.add_node('approval', approval_node)
builder.add_node('refinement_output', refinement_node)

builder.add_edge(START, 'retriever')
builder.add_edge('retriever', 'analyze_requirements')
builder.add_edge('analyze_requirements', 'build_stories')
builder.add_edge('analyze_requirements', 'gap_analysis')
builder.add_edge('build_stories', 'prepare_review')
builder.add_edge('gap_analysis', 'prepare_review')
builder.add_edge('prepare_review', 'review_output')
builder.add_edge('review_output', 'approval')
builder.add_conditional_edges('approval',approval_router,
    {'end':END,"refine":'refinement_output'}
)
# Refinement loops back to prepare_review (or review_output)
builder.add_edge('refinement_output', 'prepare_review')

graph = builder.compile(checkpointer=checkpointer)
