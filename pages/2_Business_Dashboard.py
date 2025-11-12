import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from db import DB_PATH

st.title("📊 Business Dashboard")
st.write("Insights and analytics from customer feedback.")

conn = sqlite3.connect(DB_PATH)

feedback_df = pd.read_sql_query("SELECT * FROM feedback", conn)
analysis_df = pd.read_sql_query("""
    SELECT a.*, f.product, f.feedback_text, f.created_at
    FROM analysis a
    JOIN feedback f ON a.feedback_id = f.id
    ORDER BY f.created_at DESC
""", conn)

conn.close()

if len(analysis_df) == 0:
    st.warning("No analyzed feedback yet. Once feedback is processed by AI, results will appear here.")
else:
    # Sentiment distribution
    sentiment_count = analysis_df['sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['Sentiment', 'Count']
    fig1 = px.pie(sentiment_count, names='Sentiment', values='Count', title='Sentiment Distribution')
    st.plotly_chart(fig1, use_container_width=True)

    # Top topics
    analysis_df['topics'] = analysis_df['topics'].fillna('')
    topics = analysis_df['topics'].str.split(',').explode().str.strip()
    topic_counts = topics.value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    fig2 = px.bar(topic_counts.head(10), x='Topic', y='Count', title='Top Mentioned Topics')
    st.plotly_chart(fig2, use_container_width=True)

    # Recent feedback table
    st.subheader("🧾 Recent Feedback and AI Responses")
    st.dataframe(analysis_df[['product', 'feedback_text', 'sentiment', 'topics', 'ai_reply', 'created_at']], use_container_width=True)
