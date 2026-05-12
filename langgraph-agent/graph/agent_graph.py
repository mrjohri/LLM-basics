from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import planner_node, search_node, summarize_node, direct_answer_node

workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("search", search_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("direct_answer", direct_answer_node)

def router(state):
    return "search" if state["decision"] == "search" else "direct_answer"

workflow.set_entry_point("planner")
workflow.add_conditional_edges("planner", router, {"search": "search", "direct_answer": "direct_answer"})
workflow.add_edge("search", "summarize")
workflow.add_edge("summarize", END)
workflow.add_edge("direct_answer", END)

graph = workflow.compile()
