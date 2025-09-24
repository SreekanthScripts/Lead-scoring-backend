# 👉 rules.py
# These functions represent our RULE-BASED logic (0–50 points).
# Think of this like a “pre-screening” before AI adds its magic.

def role_score(role: str) -> int:
    """
    Rule 1: Check how important the role is.
    - Decision maker (CEO, Head, Director) → +20
    - Influencer (Manager, Lead) → +10
    - Everyone else → +0
    """
    role = role.lower()
    if "head" in role or "chief" in role or "director" in role:
        return 20
    elif "manager" in role or "lead" in role:
        return 10
    return 0


def industry_score(industry: str, ideal_use_cases: list) -> int:
    """
    Rule 2: Check if the lead's industry matches the offer's ideal use cases.
    - Exact ICP (match found) → +20
    - Adjacent (tech, software, IT) → +10
    - Else → 0
    """
    industry = industry.lower()
    for case in ideal_use_cases:
        if case.lower() in industry:
            return 20
    return 10 if any(word in industry for word in ["tech", "software", "it"]) else 0


def completeness_score(lead: dict) -> int:
    """
    Rule 3: If all fields are filled → +10
    """
    return 10 if all(lead.values()) else 0


def rule_based_score(lead: dict, offer: dict) -> int:
    """
    Combine all 3 rule checks → max 50 points.
    """
    return (
        role_score(lead["role"]) +
        industry_score(lead["industry"], offer["ideal_use_cases"]) +
        completeness_score(lead)
    )
