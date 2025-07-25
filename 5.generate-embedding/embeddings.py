import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint="https://azureaiagenttest.cognitiveservices.azure.com"
)

response = client.embeddings.create(
    input=["The ultimate answer to the question of life"],
    model="text-embedding-ada-002"
)

for embed in response.data:
    print("Embedding of size:", np.asarray(embed.embedding).shape)

print("Model:", response.model)
print("Usage:", response.usage)
print("Embedding:", response.data[0].embedding)