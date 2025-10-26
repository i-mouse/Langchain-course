REACT_FORMAT_INSTRUCTION = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
...(this Thought/Action/Action Input/Observation can repeat N times)...
Thought: I now know the final answer

Final Answer: The final answer to the question should be valid JSON matching this schema:
{format_instructions}

--- RULES ---
- You must start the final section with exactly "Final Answer:" (no extra text or newlines before JSON)
- Do NOT include markdown, code fences, or explanations outside the JSON
- Output ONLY one valid JSON object

Begin!

Question: {input}
{agent_scratchpad}
"""
