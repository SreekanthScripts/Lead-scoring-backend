
# 👉 main.py
# This is the brain of the backend — all API routes live here.
# FastAPI automatically generates interactive docs at /docs 🚀

from fastapi import FastAPI, UploadFile, File
import pandas as pd
from models import Offer
from rules import rule_based_score
from ai import ai_score

# Create FastAPI app
app = FastAPI(
    title="Lead Scoring Backend",
    description="Scores leads using rules + AI",
    version="1.0.0"
)

# In-memory storage (simple for assignment — normally we'd use DB)
offers = {}
leads_df = None
results = []


# 👇 Root route for health check + welcome message
@app.get("/")
def root():
    return {
        "message": "✅ Lead Scoring Backend is running!",
        "docs_url": "/docs",
        "endpoints": ["/offer", "/leads/upload", "/score", "/results"]
    }


@app.post("/offer")
def upload_offer(offer: Offer):
    """
    Upload the product/offer details (name, value props, ICP).
    Example input:
    {
      "name": "AI Outreach Automation",
      "value_props": ["24/7 outreach", "6x more meetings"],
      "ideal_use_cases": ["B2B SaaS mid-market"]
    }
    """
    offers["current"] = offer.dict()
    return {"message": "Offer uploaded successfully!"}


@app.post("/leads/upload")
def upload_leads(file: UploadFile = File(...)):
    """
    Upload a CSV file with columns:
    name,role,company,industry,location,linkedin_bio
    """
    global leads_df
    leads_df = pd.read_csv(file.file)
    return {"message": f"{len(leads_df)} leads uploaded successfully!"}


@app.post("/score")
def score_leads():
    """
    Run scoring for all uploaded leads.
    Combines RULES (0–50 points) + AI (0–50 points).
    """
    global results
    offer = offers.get("current")
    if offer is None:
        return {"error": "No offer uploaded yet!"}

    results = []
    for _, row in leads_df.iterrows():
        lead = row.to_dict()

        # Rule-based part
        rule_score = rule_based_score(lead, offer)

        # AI part (currently mocked for testing)
        # intent, ai_points, reasoning = ai_score(lead, offer)
        intent = "Medium"
        ai_points = 30
        reasoning = "AI scoring skipped for testing."

        # Final score
        final_score = rule_score + ai_points

        results.append({
            **lead,
            "intent": intent,
            "score": final_score,
            "reasoning": reasoning
        })

    return {"message": "Scoring complete!", "count": len(results)}


@app.get("/results")
def get_results():
    """
    Fetch all scored leads as JSON.
    """
    return results
