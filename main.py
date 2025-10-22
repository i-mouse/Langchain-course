import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch


# langchain_classic is a temporary backward compatibility layer — it exists only so that old code keeps working without rewriting 
# everything when LangChain reorganized its packages.
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent

load_dotenv()



def main():
    print("Hello from langchain-course!")


if __name__ == "__main__":
    main()
