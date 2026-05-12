from typing import TypedDict

class AgentState(TypedDict):
    query: str
    decision: str
    search_results: str
    final_answer: str
