import os

from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_classic.output_parsers.pydantic import PydanticOutputParser
from langchain_classic.prompts import PromptTemplate
# External LangChain integrations
from langchain_ollama import ChatOllama
from langchain_openai import OpenAI
from langchain_tavily import TavilySearch

from prompts import REACT_FORMAT_INSTRUCTION
# Your local project files
from schemas import AgentResponse

# langchain_classic is a temporary backward compatibility layer — it exists only so that old code keeps working without rewriting
# everything when LangChain reorganized its packages.




load_dotenv()

tool = [TavilySearch()]
llm = ChatOllama(model="llama3.1:8b", temperature=0)

#react_prompt = hub.pull("hwchase17/react")   # Use the langchain_classic ReAct prompt
#react_prompt = hub.pull("hwchase17/react-json") # Use the langchain ReAct JSON prompt (modern version)

# instead of using prebuild or community output format, PydanticOutputParser help us to create our own output response
newOutputParser = PydanticOutputParser(pydantic_object=AgentResponse)

react_prompt = PromptTemplate(template=REACT_FORMAT_INSTRUCTION,input_variables=["input","agent_scratchpad","tool_names"]).partial(format_instructions =newOutputParser.get_format_instructions())

agent = create_react_agent(llm=llm, tools=tool, prompt=react_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True)
chain = agent_executor

def main():
    print("Hello from langchain-course!")

result = chain.invoke(
    input={"input": "Find the 3 most recent tutorials or blogs about learning LangChain published this month."}
)
print("\nResult:", result)

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



