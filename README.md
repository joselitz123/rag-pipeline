# RAG Pipeline with Docling, SQLite-Vec, and Azure AI

This project implements a Retrieval-Augmented Generation (RAG) pipeline using FastAPI. It leverages **Docling** for advanced document ingestion, **SQLite-Vec** for local vector storage, **Ollama** for embeddings, and **Azure AI Foundry** for LLM generation.

## Architecture Flow

1.  **Ingestion (`/ingest` endpoint)**
    *   **Upload**: User uploads a document (PDF, DOCX, etc.).
    *   **Parsing**: `Docling` parses the document, extracting text and structure (layout, headers, etc.).
    *   **Chunking**: The text is split into meaningful chunks (currently paragraph-based).
    *   **Embedding**: Each chunk is passed to **Ollama** (e.g., `nomic-embed-text`) to generate a vector embedding.
    *   **Storage**: The chunk text and its embedding are stored in a local SQLite database using `sqlite-vec` for vector indexing.

2.  **Retrieval & Generation (`/chat` endpoint)**
    *   **Query**: User sends a text query.
    *   **Embedding**: The query is embedded using the same Ollama model.
    *   **Vector Search**: The system queries `sqlite-vec` to find the most similar document chunks (based on cosine similarity/distance).
    *   **Context Assembly**: The retrieved chunks are combined into a context block.
    *   **Generation**: The context and user query are sent to **Azure AI Foundry** (GPT-4, etc.) to generate a final answer.

## Prerequisites

- **Python 3.10+**
- **Ollama**: Running locally (default `http://localhost:11434`) with an embedding model pulled (e.g., `ollama pull nomic-embed-text`)
- **Azure AI Foundry Access**: Project endpoint and API Key

## Configuration

Create a `.env` file in the root directory (copy from `.env.example`) and set the following variables:

```ini
# Azure AI Foundry Configuration
# NOTE: API_KEY is required for both configuration options
API_KEY=your_api_key_here

# Option 1: Use Target URI (Recommended)
AZURE_TARGET_URI=https://<project>.cognitiveservices.azure.com/openai/deployments/<deployment>/chat/completions?api-version=2024-05-01-preview

# Option 2: Individual Variables
# PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project-name
# AZURE_DEPLOYMENT_NAME=gpt-4o
# API_VERSION=2024-10-21

# Ollama Configuration (for embeddings)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=nomic-embed-text

# Database
DB_PATH=rag.db
```

## Dev Container Configuration

The project includes a `.devcontainer` configuration designed to access the Ollama service running on the host machine.

*   **Network Mode**: The container uses `--network=host` to share the host's network stack, providing direct access to services running on `localhost`.
*   **Environment Variable**: `OLLAMA_BASE_URL` is automatically set to `http://localhost:11434`.
*   **Python Version**: Uses Python 3.14.0 base image.
*   **Auto-setup**: Dependencies are automatically installed via `postCreateCommand` after container creation.

> [!NOTE]
> The host networking mode allows the container to access Ollama running on the host machine without requiring specific IP address configuration. This makes the setup more portable across different environments.

## Running the Application

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Server**:
    ```bash
    python main.py
    ```
    Or directly with uvicorn:
    ```bash
    uvicorn main:app --reload
    ```

3.  **Test**:
    Run the included test script:
    ```bash
    python test_rag.py
    ```
