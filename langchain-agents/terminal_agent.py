import config
import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
import subprocess


@tool
def terminal(command: str):
    """this tool emulates a terminal"""
    result = subprocess.run(
        command, 
        shell=True,
        capture_output=True,
        text=True
    )
    return result

agent = create_agent(
    model=config.llm,
    tools=[terminal],
    system_prompt="You are an assistant with access to the directory"
)

while(True):
    user_input = input("\nYou: ")

    if user_input.lower() in ("exit", "quit"):
        break

    result = agent.invoke({
        "messages" : [
            {"role" : "user", "content" : user_input}
        ]
    })

    print(f"Answer: {result['messages'][-1].content}")