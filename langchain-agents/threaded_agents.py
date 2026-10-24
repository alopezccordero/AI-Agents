import config
import subprocess
import threading
from langchain.agents import create_agent
from langchain.tools import tool




@tool
def terminal(command: str) -> str:
    """
    Execute a shell command and return its output
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
            output += f"STDERR:\n{result.stderr}\n"
        output += f"\nExit Code: {result.returncode}"

        return output

    except subprocess.TimeoutExpired:
        return "ERROR: command timed out after 30 seconds."



@tool 
def new_agent(prompt: str) -> str:
    """Use this tool to delegate tasks to a worker
    agent. You can use this tool repeatedly
    to delegate multiple tasks"""

    print("\n[Worker Started]\n")

    result = worker.invoke({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    print("\n[Worker Finished]\n")

    return result["messages"][-1].content

@tool
def threaded_agents(num_threads: int, prompt: str):
    """
    This tool is to create multiple threaded agents
    that can execute in parallel and have access to terminal  
    num_threads =  num_agents
    prompt = the single prompt that each agent will execute

    """
    threads = []
    results = [None] * num_threads

    def worker_wrapper(index):
        results[index] = new_agent.invoke(prompt)

    for i in range(num_threads):
        t = threading.Thread(target=worker_wrapper, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("All threaded agents have completed")

    return "\n\n".join(
        f"agent {i} : {result}"
        for i, result in enumerate(results)
    )


@tool
def threaded_agents_multiple_prompts(prompts: list ):
    """
    this tool is to create multiple_threaded_agents that execute multiple
    prompts
    prompts is a list. len(prompts) is the number of agents that will be created
    each agent will execute its prompt respectively 
    """
    threads = []
    results = [None] * len(prompts)
    def worker_wrapper(index, prompt):
        results[index] = new_agent.invoke(prompt)
    for i in range(len(prompts)):
        t = threading.Thread(target=worker_wrapper, args=(i, prompts[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("All threaded agents have completed")

    return "\n\n".join(
        f"agent {i} : {result}"
        for i, result in enumerate(results)
    )



worker = create_agent(
    model = config.employee,
    tools=[terminal],
    system_prompt="""
You are a worker agent.
Your job is to complete the prompts that are given to you
You can use the tool terminal to handle files and commands
"""
)

manager = create_agent(
    model = config.llm,
    tools=[terminal, threaded_agents, threaded_agents_multiple_prompts, new_agent],
    system_prompt="""
You are a an assistant with access to tools terminal, create_agent, threaded_agents

use:
- terminal for commands, create, delete files, shell usage.
- new_agent for delegating a task to a new agent.
- threaded_agents for delegating multiple tasks to multiple agents (they are threaded so 
they execute in parallel) - num_threads (num of agents) - prompt (single prompt that will be executed
by different agents)
- threaded_agents_multiple_prompts for delegating multiple tasks to multiple agents (they are threaded
so they execute in parallel) - it takes a list of prompts, and each index in the list is an agent
that executes the prompt in that index

after receiving the repsonse. provide a final answer
"""
)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ("exit", quit):
        break

    try:
        print("\n[Main agent running]\n")
        result = manager.invoke({
            "messages" : [
                {
                    "role" : "user",
                    "content" : user_input
                }
            ]
        })

        print("\nMain agent finished\n")
        print(f"Answer:\n{result['messages'][-1].content}")

    except Exception as e:
        print(f"\nError {e}")