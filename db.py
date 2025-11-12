import sqlite3
from datetime import datetime

DB_PATH = "retail_feedback.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product TEXT,
                    feedback_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feedback_id INTEGER,
                    sentiment TEXT,
                    topics TEXT,
                    ai_reply TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(feedback_id) REFERENCES feedback(id)
                )''')
    conn.commit()
    conn.close()

def insert_feedback(product, feedback_text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (product, feedback_text) VALUES (?, ?)", (product, feedback_text))
    conn.commit()
    feedback_id = c.lastrowid
    conn.close()
    return feedback_id

def insert_analysis(feedback_id, sentiment, topics, ai_reply):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO analysis (feedback_id, sentiment, topics, ai_reply) VALUES (?, ?, ?, ?)",
        (feedback_id, sentiment, topics, ai_reply)
    )
    conn.commit()
    conn.close()
