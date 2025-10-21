import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_ollama import ChatOllama

load_dotenv()

# key = os.getenv("OPENAI_API_KEY")

def main():
    print("Hello from langchain-course!\n\n")
    
    information = """Sachin Tendulkar, known as the “God of Cricket,” is one of the greatest batsmen in the history of " \
    "the sport. Born on April 24, 1973, in Mumbai, India, he made his international debut at just 16 years old. Over his " \
    "24-year career, Sachin set numerous records, including being the first player to score 100 international centuries. " \
    "His dedication, humility, and passion for the game inspired millions. Beyond statistics, Sachin became a symbol of " \
    "excellence and perseverance, earning respect both on and off the field."""

    # here information is not a variable, its just a placeholder
    template = "Given the information {information}, I want you to create 1. Short summry 2.two bad points"

    prompt = PromptTemplate(input_variables=["information"], template=template)

    # llm = OpenAI(temperature=0,model="gpt-5")
    llm = ChatOllama(temperature=0,model="gemma3:270m")

    chain = prompt | llm

    response = chain.invoke({"information" : information})
    print(response.content)

if __name__ == "__main__":
    main()
