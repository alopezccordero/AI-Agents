import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import AIMessage, ToolMessage
import config


API_KEY = os.getenv("API_KEY")


 
llm = config.llm

@tool
def multiply(a: int, b: int):
    """Multiply two integers""" #for the agent to read
    return a * b
@tool
def minutes_to_hours(minutes: int) -> bool:
    """Converts minutes into hours"""
    return minutes

agent = create_agent(
    model=llm,
    tools=[multiply, minutes_to_hours],
    system_prompt=(
        "You are a helpful assistant"
        "Use the provided tools for calculation"
    )
)

result = agent.invoke(
    {
        "messages" : [
            {
                "role" : "user",
                "content": (
                    "I have 5 workshops, each lasting"
                    "90 minutes. how many hours total?"
                )
            }
        ]
    },
    config={"recursion_limit":10}
)


for message in result["messages"]:
    if isinstance(message, AIMessage):
        for call in message.tool_calls:
            print("Tool called: ", call["name"])
            print("Arguments: ", call["args"])

    elif isinstance(message, ToolMessage):
        print("Tool result: ", message.content)

print("Final answer\n")
print(result["messages"][-1].content)