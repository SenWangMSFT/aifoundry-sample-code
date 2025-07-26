import os
import time
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool, FilePurpose, MessageRole

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential(),
)

# ✅ Upload file via agents.files.upload_and_poll
file = project_client.agents.files.upload_and_poll(
    file_path="electronics_products.csv",
    purpose=FilePurpose.AGENTS
)
print(f"Uploaded CSV file, ID = {file.id}")

# ✅ Instantiate Code Interpreter tool
code_interpreter = CodeInterpreterTool(file_ids=[file.id])

# ✅ Create agent configured with the tool
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions="You are helpful agent",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)

thread = project_client.agents.threads.create()
project_client.agents.messages.create(
    thread_id=thread.id,
    role=MessageRole.USER,
    content="Please visualize the uploaded CSV file and return the generated file.",
)

run = project_client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id
)

messages = project_client.agents.messages.list(thread_id=thread.id)

# Save generated images or files
for message in messages:
    # 🖼 Save image responses
    for img in message.image_contents:
        file_id = img.image_file.file_id
        local_name = f"{file_id}.png"
        project_client.agents.files.save(
            file_id=file_id,
            file_name=local_name
        )
        print(f"Saved image locally: {local_name}")

    # 💬 Print message text
    if message.content:
        print(f"\n[{message.role}] Message:\n{message.content}")

    # 📂 Show any file path annotations
    for annotation in getattr(message, "file_path_annotations", []):
        print("\n📁 File Path Annotation:")
        print(f"Type: {annotation.type}")
        print(f"Text: {annotation.text}")
        print(f"File ID: {annotation.file_path.file_id}")

# Step: Delete the original uploaded file to free up storage
project_client.agents.files.delete(file.id)
print(f"Deleted uploaded file: {file.id}")
