REACT_FORMAT_INSTRUCTION = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question should follow {format_instructions}

Important:
- Always include 'Action:' after every 'Thought:' except before the final answer.
- The final output must be plain JSON — no extra text or formatting.
Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
