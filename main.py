"""
🧠 LangChain ReAct Agent (Manual vs Structured Output)

This script runs a ReAct agent using Ollama (llama3.1) + TavilySearch.

- The agent reasons step-by-step (Thought → Action → Observation → Final Answer)
- Final answer is parsed into a structured Pydantic model (AgentResponse)
- Two versions shown: manual parser and structured_output()

⚠️ Note:
If you see OutputParserException, just re-run the script — local LLMs sometimes miss
the ReAct format. Switching to GPT-4o fixes this completely.
"""


import json
import os

from dotenv import load_dotenv
# from langchain_classic.agents import AgentExecutor
# from langchain_classic.agents.react.agent import create_react_agent
# from langchain_classic.output_parsers.pydantic import PydanticOutputParser
# from langchain_classic.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.agents import create_agent
from langchain.tools import tool

# External LangChain integrations
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch

# Local project files
from prompts import REACT_FORMAT_INSTRUCTION
from schemas import AgentResponse

# Load .env
load_dotenv()

# --- Define tools and LLM ---
tools = [TavilySearch()]

@tool("smart_search", return_direct=False)
def smart_search(query: str) -> str:
    """
    A smarter fake search tool for testing agents.
    Returns realistic search-like JSON for the query.
    """
    results = [
        {
            "title": f"{query} – Official LangChain Blog",
            "url": "https://blog.langchain.com/langchain-0-2-0-release"
        },
        {
            "title": f"{query} – Medium Tutorial",
            "url": "https://medium.com/@langchain/intro-tutorial",
        },
        {
            "title": f"{query} – Towards Data Science Guide",
            "url": "https://towardsdatascience.com/langchain-getting-started"
        }
    ]

    # Return structured, clean data
    return {"query": query, "results": results}

Simpletools = [smart_search]

llm = ChatOllama(model="gpt-oss:20b", temperature=0 ,format="json")
extract_structured = RunnableLambda(lambda x: x.get("structured_response"))

#------- using newest approach v1.0 create_agent()-------------------
agent = create_agent(model= llm , tools=Simpletools, response_format=AgentResponse)
chain = agent | extract_structured
def main():
    print("\n🚀 Hello from langchain-course!\n")
    query = "Find the 3 most recent tutorials or blogs about learning LangChain published this month."
  

    result = chain.invoke({"messages": [{"role": "user", "content":query}]})
    print(f"\n\nresult :{result} ")


if __name__ == "__main__":
    main()
