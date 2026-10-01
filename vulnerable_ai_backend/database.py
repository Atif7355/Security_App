# database.py
import sqlite3
from config import DATABASE_URL

def get_db_connection():
    conn = sqlite3.connect("test.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users (id, username, role) VALUES (1, 'admin', 'administrator')")
    conn.commit()
    conn.close()

def unsafe_find_user(username: str):
    """
    FORTIFY & SONARQUBE VULNERABILITY: SQL Injection
    Directly concatenating user input into the SQL string allows attackers 
    to manipulate the query structure.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vulnerable query construction
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return [dict(row) for row in result]
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
