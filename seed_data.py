import random
import time
from db import insert_feedback, insert_analysis, init_db
from ai_utils import analyze_feedback

# Initialize DB
init_db()

products = ["Shoes", "Headphones", "T-shirt", "Laptop Bag", "Watch"]

sample_feedbacks = [
    "The product quality is amazing, I'm very satisfied!",
    "It stopped working after just two weeks.",
    "Looks good but feels uncomfortable to wear.",
    "Excellent sound quality and battery life.",
    "The delivery was late and packaging was poor.",
    "I'm really impressed with the comfort and fit.",
    "Not worth the price, feels cheap.",
    "Customer service was very responsive.",
    "The design is sleek and modern.",
    "It’s okay, nothing special honestly.",
    "Colors faded after one wash.",
    "The strap broke after a few uses.",
    "Totally loved it, will buy again!",
    "Size doesn’t match the chart.",
    "Battery drains too quickly.",
    "Very lightweight and comfortable.",
    "Feels durable and stylish.",
    "Received a defective item, disappointed.",
    "Perfect for daily use.",
    "Material quality could be better.",
]

print("🚀 Seeding AI-analyzed feedback data...\n")

for i in range(1, 101):  # 100 entries
    product = random.choice(products)
    feedback = random.choice(sample_feedbacks)
    
    print(f"Processing {i}/100 → {product}: {feedback[:40]}...")

    # Insert feedback
    feedback_id = insert_feedback(product, feedback)

    # Run AI analysis
    try:
        sentiment, topics, ai_reply = analyze_feedback(feedback, product)
        insert_analysis(feedback_id, sentiment, topics, ai_reply)
    except Exception as e:
        print(f"⚠️ Error analyzing feedback {i}: {e}")

    # Sleep slightly to avoid rate limits
    time.sleep(2)

print("\n✅ Done! 100 feedback entries with AI analysis added successfully.")
