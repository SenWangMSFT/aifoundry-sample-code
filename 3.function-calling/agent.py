import os, time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FunctionTool
from function import fetch_weather, user_functions

load_dotenv()

# Retrieve the project endpoint from environment variables
project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

# Initialize the FunctionTool with user-defined functions
functions = FunctionTool(functions=user_functions)

with project_client:
    # Create an agent with custom functions
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="my-code-test-agent",
        instructions="You are a helpful agent",
        tools=functions.definitions,
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hello, send an email with the datetime and weather information in New York?",
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process a run for the agent to handle the message
    run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)
    print(f"Created run, ID: {run.id}")

    # Poll the run status until it is completed or requires action
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                print(tool_call)
                if tool_call.function.name == "fetch_weather":
                    output = fetch_weather("New York")
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
            project_client.agents.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

    print(f"Run completed with status: {run.status}")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message['role']}, Content: {message['content']}")

    # Delete the agent after use
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")