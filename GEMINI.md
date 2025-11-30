# Project Overview

This project is a Retrieval-Augmented Generation (RAG) pipeline built with Python and FastAPI. It uses Docling for document ingestion, Ollama for generating text embeddings, and SQLite with the `sqlite-vec` extension for storing and querying these embeddings. The final answer generation is handled by Azure AI Foundry.

The application exposes two main endpoints:
*   `/ingest`: Accepts a file (PDF, DOCX, etc.), processes it, and stores it in the vector database.
*   `/chat`: Takes a user query, retrieves relevant context from the database, and generates an answer.

# Building and Running

## Prerequisites

*   Python 3.10+
*   Ollama running locally (e.g., `ollama serve`)
*   An embedding model downloaded in Ollama (e.g., `ollama pull nomic-embed-text`)
*   Azure AI Foundry credentials

## Setup

1.  **Create a `.env` file:**
    Copy the `.env.example` file to `.env` and fill in the required values for your Azure AI Foundry and Ollama setup.

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the database:**
    ```bash
    python database.py
    ```

## Running the application

To start the FastAPI server, run:
```bash
python main.py
```
Or with auto-reload for development:
```bash
uvicorn main:app --reload
```
The application will be available at `http://localhost:9000`.

## Testing

To run the included tests, execute:
```bash
python test_rag.py
```

# Development Conventions

*   **Configuration:** All configuration is managed in the `config.py` file, which loads values from environment variables (a `.env` file is used for local development).
*   **Database:** The database is managed via `database.py`. The `init_db` function sets up the required tables.
*   **Embeddings:** The `embeddings.py` file centralizes the logic for generating embeddings using Ollama.
*   **Modular Design:** The core functionalities are separated into different modules:
    *   `main.py`: API endpoints
    *   `ingestion.py`: File processing and storage
    *   `rag.py`: Retrieval and generation logic
    *   `database.py`: Database connection and schema
    *   `embeddings.py`: Embedding generation
*   **Testing:** The project includes a `test_rag.py` file, which suggests that testing is a part of the development process.
