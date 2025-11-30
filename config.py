import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure AI Foundry Configuration
    # Azure AI Foundry Configuration
    AZURE_TARGET_URI = os.getenv("AZURE_TARGET_URI")
    
    if AZURE_TARGET_URI:
        import urllib.parse
        parsed = urllib.parse.urlparse(AZURE_TARGET_URI)
        PROJECT_ENDPOINT = f"{parsed.scheme}://{parsed.netloc}"
        
        # Extract deployment name from path
        # Expected format: /openai/deployments/{deployment-name}/chat/completions
        path_parts = parsed.path.strip("/").split("/")
        try:
            deployments_index = path_parts.index("deployments")
            AZURE_DEPLOYMENT_NAME = path_parts[deployments_index + 1]
        except (ValueError, IndexError):
             # Fallback or error if structure is unexpected, but for now let's assume standard format
             # or maybe user set it manually as well.
             AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")

        # Extract API version from query params
        query_params = urllib.parse.parse_qs(parsed.query)
        API_VERSION = query_params.get("api-version", [os.getenv("API_VERSION", "2024-10-21")])[0]
    else:
        PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
        AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
        API_VERSION = os.getenv("API_VERSION", "2024-10-21")

    API_KEY = os.getenv("API_KEY")

    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "nomic-embed-text") # Default embedding model

    # Database
    DB_PATH = os.getenv("DB_PATH", "rag.db")

config = Config()
