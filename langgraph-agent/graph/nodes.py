from langchain_community.tools import DuckDuckGoSearchRun
from utils.groq_llm import get_llm

search_tool = DuckDuckGoSearchRun()
llm = get_llm()

def planner_node(state):
    query = state["query"].lower()
    decision = "search" if any(k in query for k in ["latest", "news", "2026"]) else "direct"
    return {"decision": decision}

def search_node(state):
    return {"search_results": search_tool.run(state["query"])}

def direct_answer_node(state):
    response = llm.invoke(f"Answer this question clearly and simply:\n\nQuestion:\n{state['query']}")
    return {"final_answer": response.content}

def summarize_node(state):
    prompt = f"""You are an AI research assistant.

USER QUERY:
{state['query']}

SEARCH RESULTS:
{state['search_results']}

Create:
- A detailed explanation
- Beginner-friendly answer
- Bullet points where needed
- Important technologies/tools

FINAL ANSWER:
"""
    response = llm.invoke(prompt)
    return {"final_answer": response.content}
