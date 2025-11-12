import streamlit as st
import pandas as pd
import sqlite3
from db import insert_feedback, insert_analysis, init_db, DB_PATH
from ai_utils import analyze_feedback
from rag_utils import add_feedback_to_faiss

init_db()

st.title("🗣️ Customer Feedback Portal")
st.write("Share your experience with our products!")

with st.form("feedback_form"):
    product = st.selectbox("Select Product", ["Shoes", "Headphones", "T-shirt", "Laptop Bag", "Watch"])
    feedback_text = st.text_area("Your Feedback", placeholder="Type your feedback here...")
    submit_btn = st.form_submit_button("Submit Feedback")

if submit_btn:
    if feedback_text.strip() == "":
        st.warning("Please enter your feedback before submitting.")
    else:
        feedback_id = insert_feedback(product, feedback_text)
        st.success("✅ Thank you for your feedback! Analyzing now...")

        with st.spinner("🤖 AI analyzing your feedback..."):
            sentiment, topics, ai_reply = analyze_feedback(feedback_text, product)
            insert_analysis(feedback_id, sentiment, topics, ai_reply)
            # 🧩 Add this line to auto-learn new feedback into RAG index
            add_feedback_to_faiss(feedback_id, feedback_text)
        st.subheader("💬 AI Response:")
        st.write(ai_reply)
        st.caption(f"**Sentiment:** {sentiment} | **Topics:** {topics}")

# Show recent feedbacks
st.subheader("🗂️ Recent Feedback Submissions")
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("""
    SELECT f.id, f.product, f.feedback_text, a.sentiment, a.topics, a.ai_reply, f.created_at
    FROM feedback f
    LEFT JOIN analysis a ON f.id = a.feedback_id
    ORDER BY f.created_at DESC LIMIT 10
""", conn)
conn.close()
st.dataframe(df, use_container_width=True)
