from openai import AzureOpenAI
from config import config
from database import get_db_connection
import struct
from embeddings import client as ollama_client

# Initialize Azure AI Foundry client
client = AzureOpenAI(
    api_key=config.API_KEY,
    azure_endpoint=config.PROJECT_ENDPOINT,
    api_version=config.API_VERSION
)

def retrieve_context(query: str, limit: int = 5) -> list[str]:
    """
    Retrieve relevant context from SQLite using vector search.
    """
    # Generate query embedding
    response = ollama_client.embeddings(model=config.OLLAMA_MODEL, prompt=query)
    query_embedding = response["embedding"]
    
    # Serialize embedding
    query_blob = struct.pack(f'{len(query_embedding)}f', *query_embedding)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Perform vector search
    # We join with documents table to get the content
    # Note: sqlite-vec requires k parameter in the MATCH clause
    cursor.execute("""
        SELECT d.content, distance
        FROM vec_items v
        JOIN documents d ON v.document_id = d.id
        WHERE v.embedding MATCH ?
          AND k = ?
        ORDER BY distance
    """, (query_blob, limit))
    
    results = list(cursor)
    conn.close()
    
    return [row[0] for row in results]

def generate_answer(query: str) -> str:
    """
    Generate answer using RAG.
    """
    context_list = retrieve_context(query)
    context_text = "\n\n".join(context_list)
    
    system_prompt = f"""You are a helpful assistant. Use the following context to answer the user's question.
    
    Context:
    {context_text}
    """
    
    response = client.chat.completions.create(
        model=config.AZURE_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    
    return response.choices[0].message.content
