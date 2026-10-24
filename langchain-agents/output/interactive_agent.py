import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import AIMessage, ToolMessage
from dotenv import load_dotenv
import config

load_dotenv()

llm = config.llm

@tool
def multiply(a: int, b: int):
    """this function returns the result of a multiplication"""
    return a * b

def minutes_to_hours(minutes: int) -> float:
    """this function takes minutes as input and returns it converted
    into hours"""
    return minutes/60

agent = create_agent(
    model=llm,
    tools=[multiply, minutes_to_hours],
    system_prompt=(
        "You are an assistant" #who are you
        "Use the provided tools" #
    )
)

##define the result

result = agent.invoke(
    {
        "messages": [
            {
                "role" : "user",
                "content" : (
                    "I have 5 workshops each lasts 130 minutes"
                    "How many hours total"
                )
            }
        ] 
    }
)

while(True):
    user_input = input("\nYou?: ")

    if user_input.lower() in ("exit", "quit"):
        break

    result = agent.invoke({
        "messages" : [
            {"role" : "user", "content" : user_input}
        ]
    })

    print(f"Answer {result["messages"][-1].content}")


