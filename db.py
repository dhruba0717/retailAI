import sqlite3
from datetime import datetime

DB_PATH = "retail_feedback.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Feedback table: stores raw user input
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            feedback_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Analysis table: stores AI results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id INTEGER,
            sentiment TEXT,
            topics TEXT,
            ai_reply TEXT,
            embedding_id TEXT,
            FOREIGN KEY (feedback_id) REFERENCES feedback(id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_feedback(product, text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (product, feedback_text, created_at) VALUES (?, ?, ?)",
                   (product, text, datetime.now()))
    feedback_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return feedback_id

def insert_analysis(feedback_id, sentiment, topics, ai_reply, embedding_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO analysis (feedback_id, sentiment, topics, ai_reply, embedding_id) VALUES (?, ?, ?, ?, ?)",
                   (feedback_id, sentiment, topics, ai_reply, embedding_id))
    conn.commit()
    conn.close()
