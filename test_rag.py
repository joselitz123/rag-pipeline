import os
import time
from fastapi.testclient import TestClient
from main import app
from config import config
from database import init_db

# Use a test database to avoid affecting the real one
TEST_DB = "test_rag.db"
config.DB_PATH = TEST_DB

# Initialize the test database
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
init_db()

print(f"Using OLLAMA_BASE_URL: {config.OLLAMA_BASE_URL}")

# Check Ollama connectivity
try:
    from ollama import Client
    ollama_client = Client(host=config.OLLAMA_BASE_URL)
    ollama_client.list()
    print("Ollama connection successful.")
except Exception as e:
    print(f"WARNING: Could not connect to Ollama at {config.OLLAMA_BASE_URL}: {e}")
    print("Tests involving embeddings might fail or hang.")

client = TestClient(app)

def test_ingest():
    print("Testing Ingestion (Real)...")
    # Create a dummy file
    test_filename = "test_doc.md"
    with open(test_filename, "w") as f:
        f.write("This is a test document content for ingestion. It contains information about testing RAG pipelines.")
    
    try:
        with open(test_filename, "rb") as f:
            files = {'file': (test_filename, f, 'text/markdown')}
            response = client.post("/ingest", files=files)
            
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["chunks_processed"] > 0
        
    finally:
        if os.path.exists(test_filename):
            os.remove(test_filename)

def test_chat():
    print("\nTesting Chat (Real)...")
    # Give some time for any async processing if needed (though sqlite is sync here)
    time.sleep(1)
    
    payload = {"query": "What does the document contain information about?"}
    
    response = client.post("/chat", json=payload)
            
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    answer = response.json().get("answer")
    assert answer is not None
    assert isinstance(answer, str)
    assert len(answer) > 0
    # Check if the answer is relevant (optional, but good sanity check)
    # The document mentions "testing RAG pipelines", so the answer should likely contain "testing" or "RAG".
    print(f"Answer received: {answer}")

if __name__ == "__main__":
    try:
        test_ingest()
        test_chat()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        exit(1)
    finally:
        # Cleanup test database
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
