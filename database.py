import apsw
import sqlite_vec
from config import config

def get_db_connection():
    conn = apsw.Connection(config.DB_PATH)
    conn.enable_load_extension(True)
    conn.load_extension(sqlite_vec.loadable_path())
    conn.enable_load_extension(False)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create documents table for metadata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create vector table using sqlite-vec
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_items USING vec0(
            document_id INTEGER,
            embedding float[4096]
        )
    """)
    
    # APSW doesn't need commit for DDL usually, but let's be safe if we were using transactions
    # APSW is in auto-commit mode by default unless inside a transaction
    conn.close()

if __name__ == "__main__":
    init_db()
