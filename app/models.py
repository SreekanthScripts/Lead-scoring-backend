# 👉 models.py
# Pydantic models = blueprints for how data should look in requests & responses.
# They make sure your APIs only accept & return valid data.

from pydantic import BaseModel
from typing import List

# When someone uploads a product/offer, it will look like this:
class Offer(BaseModel):
    name: str
    value_props: List[str]          # e.g., ["24/7 outreach", "6x more meetings"]
    ideal_use_cases: List[str]      # e.g., ["B2B SaaS mid-market"]

# Each lead has this structure when uploaded from CSV
class Lead(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: str

# After scoring, we return the same lead info + score + intent + reasoning
class ScoredLead(Lead):
    intent: str
    score: int
    reasoning: str
