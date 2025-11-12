import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_feedback(feedback_text, product):
    prompt = f"""
    You are an AI assistant analyzing customer feedback for a retail product.

    Given the following feedback about a {product}, you must respond in this *exact JSON format*:
    {{
        "Sentiment": "Positive / Neutral / Negative",
        "Topics": "comma-separated list of key aspects mentioned",
        "Reply": "short, polite company response message"
    }}

    Feedback: "{feedback_text}"
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    content = response.choices[0].message.content.strip()

    # Try parsing JSON-style response robustly
    sentiment, topics, reply = "Neutral", "", ""
    try:
        import json, re
        # Extract JSON-like content
        json_str = re.search(r'\{.*\}', content, re.DOTALL)
        if json_str:
            data = json.loads(json_str.group(0))
            sentiment = data.get("Sentiment", "Neutral")
            topics = data.get("Topics", "")
            reply = data.get("Reply", "")
        else:
            # fallback manual parse
            for line in content.split("\n"):
                if "Sentiment" in line:
                    sentiment = line.split(":", 1)[1].strip()
                elif "Topics" in line:
                    topics = line.split(":", 1)[1].strip()
                elif "Reply" in line:
                    reply = line.split(":", 1)[1].strip()
    except Exception as e:
        print("Parse error:", e, "Raw content:", content)

    return sentiment, topics, reply
