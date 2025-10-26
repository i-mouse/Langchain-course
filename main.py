import json
import os

from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_classic.agents.react.agent import create_react_agent
from langchain_classic.output_parsers.pydantic import PydanticOutputParser
from langchain_classic.prompts import PromptTemplate

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

# --- Define ReAct prompt with correct input variables ---
react_prompt = PromptTemplate(
    template=REACT_FORMAT_INSTRUCTION,
    input_variables=["input", "agent_scratchpad", "tool_names", "tools"],
    partial_variables={
        "format_instructions": new_output_parser.get_format_instructions()
    },
)

# --- Create agent and executor ---
agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)
chain = agent_executor


def main():
    print("\n🚀 Hello from langchain-course!\n")

    query = "Find the 3 most recent tutorials or blogs about learning LangChain published this month."
    result = chain.invoke({"input": query})
    print(f"\n\nresult :{result} ")
    # raw_output = result.get("output", "")

    # # --- Safe JSON parsing ---
    # try:
    #     json_start = raw_output.find("{")
    #     if json_start == -1:
    #         raise ValueError("No JSON found in output.")
    #     json_output = raw_output[json_start:]
    #     json_output = json_output.replace("```json", "").replace("```", "").strip()
    #     parsed = json.loads(json_output)
    #     print("\n✅ Final Parsed Output:\n", json.dumps(parsed, indent=2))
    # except Exception as e:
    #     print("\n⚠️ Could not parse JSON output:", e)
    #     print("\nRaw Output:\n", raw_output)


if __name__ == "__main__":
    main()


# This os the nerw way to  create agent
# import os
# from dotenv import load_dotenv

# # Modern LangChain imports
# from langchain.agents import create_agent
# from langchain.agents.structured_output import ToolStrategy
# from langchain_ollama import ChatOllama
# from langchain_tavily import TavilySearch

# # Your local project files
# from schemas import AgentResponse
# from prompts import REACT_FORMAT_INSTRUCTION

# load_dotenv()

# # Initialize tools and model
# tools = [TavilySearch()]
# llm = ChatOllama(model="llama3.1:8b", temperature=0)

# # Create agent with structured output
# agent = create_agent(
#     model=llm,
#     tools=tools,
#     system_prompt=REACT_FORMAT_INSTRUCTION,  # Your custom prompt as system prompt
#     response_format=ToolStrategy(AgentResponse)  # Structured output using your Pydantic schema
# )

# def main():
#     print("Hello from langchain-course!")

#     # Invoke the agent with the new message format
#     result = agent.invoke({
#         "messages": [{"role": "user", "content": "Find the 3 most recent tutorials or blogs about learning LangChain published this month."}]
#     })

#     # Access the structured response
#     print("\nFinal Answer:",result)

# if __name__ == "__main__":
#     result = main()
