# ai_utils.py

from openai import OpenAI
import os
from dotenv import load_dotenv
from rag_utils import retrieve_similar_feedbacks

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_feedback(feedback_text, product_name):
    """
    Analyze sentiment, topics, and generate a contextual AI reply.
    Uses RAG to fetch similar feedbacks for better context.
    """

    # --- Step 1: Retrieve similar feedbacks from FAISS ---
    similar_feedbacks = retrieve_similar_feedbacks(feedback_text, k=3)
    context = ""
    if similar_feedbacks:
        context = "\n\nHere are some similar customer feedbacks:\n"
        for i, fb in enumerate(similar_feedbacks, 1):
            context += f"{i}. {fb}\n"

    # --- Step 2: Create system + user prompt ---
    system_prompt = """You are an AI assistant for a retail company. 
You analyze customer feedback and generate structured responses.
Detect sentiment (Positive, Negative, Neutral), extract topics, and write a short, empathetic reply."""

    user_prompt = f"""
Product: {product_name}
Customer Feedback: "{feedback_text}"
{context}

Now respond in this exact format:
Sentiment: <Positive/Negative/Neutral>
Topics: <comma-separated keywords>
AI Reply: <short natural response to the customer>
"""

    # --- Step 3: Send to GPT ---
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    ai_text = response.choices[0].message.content.strip()

    # --- Step 4: Parse structured output ---
    import re
    sentiment_match = re.search(r"Sentiment:\s*(.*)", ai_text)
    topics_match = re.search(r"Topics:\s*(.*)", ai_text)
    reply_match = re.search(r"AI Reply:\s*(.*)", ai_text)

    sentiment = sentiment_match.group(1).strip() if sentiment_match else "Neutral"
    topics = topics_match.group(1).strip() if topics_match else "General"
    ai_reply = reply_match.group(1).strip() if reply_match else ai_text

    return sentiment, topics, ai_reply
