from docling.document_converter import DocumentConverter
from database import get_db_connection
from embeddings import get_embedding
import struct
import os

def ingest_file(file_path: str):
    """
    Ingest a file using Docling, chunk it, embed it, and store in SQLite.
    """
    # 1. Parse document
    converter = DocumentConverter()
    result = converter.convert(file_path)
    
    # Export to markdown
    markdown_text = result.document.export_to_markdown()
    
    # Simple chunking: Split by double newlines (paragraphs)
    chunks = [c.strip() for c in markdown_text.split('\n\n') if c.strip()]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("BEGIN")
    try:
        for chunk in chunks:
            # Generate embedding
            embedding = get_embedding(chunk)
            
            # Insert into documents table
            cursor.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (os.path.basename(file_path), chunk))
            doc_id = conn.last_insert_rowid()
            
            # Insert into vector table
            vec_blob = struct.pack(f'{len(embedding)}f', *embedding)
            cursor.execute("INSERT INTO vec_items (document_id, embedding) VALUES (?, ?)", (doc_id, vec_blob))
        cursor.execute("COMMIT")
    except:
        cursor.execute("ROLLBACK")
        raise
        
    conn.close()
    return {"status": "success", "chunks_processed": len(chunks)}
