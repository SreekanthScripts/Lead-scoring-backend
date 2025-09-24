# 👉 ai.py
# This file handles AI reasoning.
# We ask AI: "Given the offer and this lead, how likely are they to buy?"

import openai
import os

# Load API key from environment variable (you'll add it later in Render/Railway).
openai.api_key = os.getenv("OPENAI_API_KEY")

def ai_score(lead: dict, offer: dict):
    """
    Ask AI to classify intent as High/Medium/Low with reasoning.
    Returns (intent, points, reasoning).
    """

    prompt = f"""
    Product/Offer: {offer['name']}
    Value Propositions: {offer['value_props']}
    Ideal Use Cases: {offer['ideal_use_cases']}

    Prospect Info: {lead}

    Task: Classify this prospect's buying intent as High, Medium, or Low.
    Explain briefly in 1–2 sentences.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",   # Can change to gpt-3.5-turbo if cheaper
        messages=[{"role": "user", "content": prompt}]
    )

    text = response["choices"][0]["message"]["content"]

    # Map AI classification to points
    if "High" in text:
        points = 50
        intent = "High"
    elif "Medium" in text:
        points = 30
        intent = "Medium"
    else:
        points = 10
        intent = "Low"

    return intent, points, text
