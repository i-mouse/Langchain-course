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
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_classic.output_parsers.pydantic import PydanticOutputParser
from langchain_classic.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

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
llm = ChatOllama(model="llama3.1:8b", temperature=0)

# --- Define custom Pydantic output parser ---
new_output_parser = PydanticOutputParser(pydantic_object=AgentResponse)


# --- Define manual chain ReAct prompt  ---
react_prompt = PromptTemplate(
    template=REACT_FORMAT_INSTRUCTION,
    input_variables=["input", "agent_scratchpad", "tool_names", "tools"],
    partial_variables={
        "format_instructions": new_output_parser.get_format_instructions()
    },
)
agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# --- Define structured chain ReAct prompt  ---
structured_output = llm.with_structured_output(AgentResponse)
structed_react_prompt = PromptTemplate(
    template=REACT_FORMAT_INSTRUCTION,
    input_variables=["input", "agent_scratchpad", "tool_names", "tools"],
    partial_variables={"format_instructions": ""},
)
structed_agent = create_react_agent(llm=llm, tools=tools, prompt=structed_react_prompt)
structed_agent_executor = AgentExecutor(
    agent=structed_agent, tools=tools, verbose=True, handle_parsing_errors=True
)


extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: new_output_parser.parse(x))

# chain = agent_executor | extract_output | parse_output
structed_chain = structed_agent_executor | extract_output | structured_output


def main():
    print("\n🚀 Hello from langchain-course!\n")
    query = "Find the 3 most recent tutorials or blogs about learning LangChain published this month."
    #result = chain.invoke({"input": query})
    structured_result = structed_chain.invoke({"input": query})
    # print(f"\n\nresult :{result} ")
    # print("\n\n=== Agent Response ===")
    # print(f"Answer: {'dummy'}\n")
    # print("Sources:")
    # for i, src in enumerate(result.sources, 1):
    #     print(f"  {i}. {src.url}")
    # print("======================\n")

    print("\n\n===Structured Agent Response ===")
    print(f"Answer: {structured_result.answer}\n")
    print("Sources:") 
    for i, src in enumerate(structured_result.sources, 1):
        print(f"  {i}. {src.url}")
    print("======================\n")


if __name__ == "__main__":
    main()
