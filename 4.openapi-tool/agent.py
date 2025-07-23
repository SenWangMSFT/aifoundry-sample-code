import os, time
from dotenv import load_dotenv
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
# import the folloing 
from azure.ai.agents.models import OpenApiTool, OpenApiAnonymousAuthDetails

load_dotenv()

# Retrieve the project endpoint from environment variables
project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)


with project_client:
# Load the OpenAPI specification for the weather service from a local JSON file
    with open(os.path.join(os.path.dirname(__file__), "weather.json"), "r") as f:
         openapi_weather = jsonref.loads(f.read())

    # Create Auth object for the OpenApiTool (note: using anonymous auth here; connection or managed identity requires additional setup)
    auth = OpenApiAnonymousAuthDetails()
    # for connection setup
    # auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id=os.environ["CONNECTION_ID"]))
    # for managed identity set up
    # auth = OpenApiManagedAuthDetails(security_scheme=OpenApiManagedSecurityScheme(audience="https://your_identity_scope.com"))

    # Initialize the main OpenAPI tool definition for weather
    openapi_tool = OpenApiTool(
        name="get_weather", spec=openapi_weather, description="Retrieve weather information for a location", auth=auth
    )

# Create an agent configured with the combined OpenAPI tool definitions
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="my-agent",
        instructions="You are a helpful agent",
        tools=openapi_tool.definitions,
    )
    print(f"Created agent, ID: {agent.id}")

# Create a new conversation thread for the interaction
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Create the initial user message in the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="What's the weather in Seattle?",
    )
    print(f"Created message, ID: {message.id}")

# Create and automatically process the run, handling tool calls internally
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Retrieve the steps taken during the run for analysis
    run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)

    # Loop through each step to display information
    for step in run_steps:
        print(f"Step {step['id']} status: {step['status']}")

        tool_calls = step.get("step_details", {}).get("tool_calls", [])
        for call in tool_calls:
            print(f"  Tool Call ID: {call.get('id')}")
            print(f"  Type: {call.get('type')}")
            function_details = call.get("function", {})
            if function_details:
                print(f"  Function name: {function_details.get('name')}")
                print(f" function output: {function_details.get('output')}")

        print()

# Delete the agent resource to clean up
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages exchanged during the conversation thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for msg in messages:
        print(f"Message ID: {msg.id}, Role: {msg.role}, Content: {msg.content}")