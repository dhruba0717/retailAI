# rag_utils.py

import os
import faiss
import numpy as np
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_PATH = "retail_feedback.db"
FAISS_INDEX = "feedback_index.faiss"
EMBED_MODEL = "text-embedding-3-small"

# --- Create embedding for a given text ---
def get_embedding(text: str):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

# --- Initialize FAISS index (load if exists) ---
def load_or_create_index(dimension=1536):
    try:
        index = faiss.read_index(FAISS_INDEX)
        print("✅ Loaded existing FAISS index.")
    except Exception:
        index = faiss.IndexFlatL2(dimension)
        print("🆕 Created new FAISS index.")
    return index

# --- Build embeddings from existing feedback data ---
def build_faiss_index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, feedback_text FROM feedback")
    rows = cursor.fetchall()
    conn.close()

    index = load_or_create_index()
    id_map = []

    for fid, text in rows:
        emb = get_embedding(text)
        index.add(np.array([emb]))
        id_map.append(fid)

    faiss.write_index(index, FAISS_INDEX)
    np.save("id_map.npy", np.array(id_map))
    print(f"✅ Indexed {len(id_map)} feedbacks in FAISS.")

# --- Retrieve top-k similar feedbacks ---
def retrieve_similar_feedbacks(query_text, k=3):
    query_emb = get_embedding(query_text)
    index = load_or_create_index()
    id_map = np.load("id_map.npy")

    if index.ntotal == 0:
        return []

    distances, indices = index.search(np.array([query_emb]), k)
    ids = [int(id_map[i]) for i in indices[0] if i < len(id_map)]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ",".join(["?"] * len(ids))
    cursor.execute(f"SELECT feedback_text FROM feedback WHERE id IN ({placeholders})", ids)
    results = [row[0] for row in cursor.fetchall()]
    conn.close()

    return results

# --- Add a single feedback to FAISS dynamically ---
def add_feedback_to_faiss(feedback_id, feedback_text):
    import os
    import numpy as np
    import faiss

    emb = get_embedding(feedback_text)
    index = load_or_create_index()
    id_map = []

    # Load existing id_map if it exists
    if os.path.exists("id_map.npy"):
        id_map = np.load("id_map.npy").tolist()

    index.add(np.array([emb]))
    id_map.append(feedback_id)

    # Save updated index and id_map
    faiss.write_index(index, FAISS_INDEX)
    np.save("id_map.npy", np.array(id_map))
    print(f"🧩 Added feedback ID {feedback_id} to FAISS.")

