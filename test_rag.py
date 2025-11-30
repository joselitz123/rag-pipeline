import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_ingest():
    print("Testing Ingestion...")
    # Create a dummy file
    with open("test_doc.md", "w") as f:
        f.write("This is a test document content for ingestion.")
    
    # Mock embedding generation
    with patch("ingestion.get_embedding") as mock_embedding:
        # Return a dummy embedding of length 4096 (matching database schema)
        mock_embedding.return_value = [0.1] * 4096
        
        with open("test_doc.md", "rb") as f:
            files = {'file': ('test_doc.md', f, 'text/markdown')}
            response = client.post("/ingest", files=files)
            
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    os.remove("test_doc.md")

def test_chat():
    print("\nTesting Chat...")
    payload = {"query": "What is this document about?"}
    
    # Mock embedding for the query
    with patch("rag.retrieve_context") as mock_retrieve:
        mock_retrieve.return_value = ["This is a test document content."]
        
        # Mock Azure OpenAI client
        with patch("rag.client.chat.completions.create") as mock_create:
            mock_response = MagicMock()
            mock_response.choices[0].message.content = "This document is about testing."
            mock_create.return_value = mock_response
            
            response = client.post("/chat", json=payload)
            
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()["answer"] == "This document is about testing."

if __name__ == "__main__":
    test_ingest()
    test_chat()
