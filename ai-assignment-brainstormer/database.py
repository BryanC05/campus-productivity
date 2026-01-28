# Database module for storing user prompts
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "prompts.db"


def init_db():
    """Initialize the SQLite database with prompts table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            generation_type TEXT NOT NULL,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_prompt(topic: str, generation_type: str, response: str = None) -> int:
    """Save a user prompt to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prompts (topic, generation_type, response, created_at) VALUES (?, ?, ?, ?)",
        (topic, generation_type, response, datetime.now())
    )
    prompt_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prompt_id


def get_prompt_history(limit: int = 10) -> list:
    """Retrieve recent prompt history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, topic, generation_type, response, created_at 
           FROM prompts ORDER BY created_at DESC LIMIT ?""",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "topic": row[1],
            "generation_type": row[2],
            "response": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]
