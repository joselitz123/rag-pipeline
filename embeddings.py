from ollama import Client
from config import config

# Initialize Ollama client with base URL from config
client = Client(host=config.OLLAMA_BASE_URL)

def get_embedding(text: str) -> list[float]:
    """
    Generate embedding for a given text using Ollama.
    """
    response = client.embeddings(model=config.OLLAMA_MODEL, prompt=text)
    return response["embedding"]
