import config
import subprocess

from langchain.agents import create_agent
from langchain.tools import tool


# ======================
# Terminal Tool
# ======================

@tool
def terminal(command: str) -> str:
    """
    Execute a shell command and return its output.
    """

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = ""

        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"

        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}\n"

        output += f"\nExit Code: {result.returncode}"

        return output

    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 30 seconds."


# ======================
# Worker Agent
# ======================

worker = create_agent(
    model=config.employee,
    tools=[terminal],
    system_prompt="""
You are a worker agent.
Your job is to complete the prompts that are given to you
You can use the tool terminal to handle files
"""
)


# ======================
# Employee Tool
# ======================

@tool
def employees(prompt: str) -> str:
    """
    Use this tool to delegate tasks to a worker
    agent. you can use this tool repeatedly
    to delegate multiple tasks.
    """

    print("\n[WORKER STARTED]")

    result = worker.invoke({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    print("[WORKER FINISHED]\n")

    return result["messages"][-1].content


# ======================
# Supervisor Agent
# ======================

agent = create_agent(
    model=config.llm,
    tools=[terminal, employees],
    system_prompt="""
You are an assistant with access to a terminal and worker agents.

Use:
- terminal for simple filesystem or command tasks.
- employees for delegating tasks to new agents.

Do not repeatedly call employees for the same task.

After receiving a worker response, provide a final answer.
"""
)


# ======================
# Chat Loop
# ======================

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ("exit", "quit"):
        break

    try:

        print("\n[MAIN AGENT RUNNING]\n")

        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        })

        print("\n[MAIN AGENT FINISHED]\n")

        print(
            f"Answer:\n{result['messages'][-1].content}"
        )

    except Exception as e:
        print(f"\nERROR: {e}")