from langgraph.graph import StateGraph, START, END

from app.state import State
from app.nodes import (
    classifier_node,
    academic_node,
    fee_node,
    general_node,
    answer_node,
    router_function
)

# Create StateGraph
builder = StateGraph(State)


# Register Nodes
builder.add_node("classifier", classifier_node)
builder.add_node("academic", academic_node)
builder.add_node("fee", fee_node)
builder.add_node("general", general_node)
builder.add_node("answer", answer_node)

builder.add_edge(START, "classifier")
builder.add_conditional_edges(
    "classifier",router_function, {
        "academic": "academic",
        "fee": "fee",
        "general": "general"
    })
builder.add_edge("academic", "answer")
builder.add_edge("fee", "answer")
builder.add_edge("general", "answer")

builder.add_edge("answer", END)


graph = builder.compile()


