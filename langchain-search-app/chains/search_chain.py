from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate

from utils.groq_llm import get_llm

search = DuckDuckGoSearchRun()

llm = get_llm()

prompt = PromptTemplate(
    input_variables=["topic", "search_results"],
    template="""
You are an expert AI research assistant.

TOPIC:
{topic}

SEARCH RESULTS:
{search_results}

Create a detailed and beginner-friendly summary.

Instructions:
- Explain clearly
- Use bullet points
- Mention important concepts
- Give examples if possible
- Never say you couldn't find information

FINAL ANSWER:
"""
)

# Modern LangChain pipeline
chain = prompt | llm

def run_search_chain(topic):

    # Better search query
    results = search.run(f"{topic} explained latest information")

    response = chain.invoke({
        "topic": topic,
        "search_results": results
    })

    return response.content