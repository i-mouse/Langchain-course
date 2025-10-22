import os

from dotenv import load_dotenv

# langchain_classic is a temporary backward compatibility layer — it exists only so that old code keeps working without rewriting
# everything when LangChain reorganized its packages.
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_ollama import ChatOllama
from langchain_openai import OpenAI
from langchain_tavily import TavilySearch

load_dotenv()

tool = [TavilySearch()]
llm = ChatOllama(model="gemma3:270m", temperature=0)
react_prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm=llm, tools=tool, prompt=react_prompt)


agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True,handle_parsing_errors=True, max_iterations=2  )
chain = agent_executor


def main():
    print("Hello from langchain-course!")


result = chain.invoke(
    input={"input": "fastest way to lean langhchain? i need ateast 3 reasons."}
)
print("\nResult:", result)

if __name__ == "__main__":
    main()
