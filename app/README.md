# Lead Scoring Backend Service

This backend service allows you to upload a **product/offer** and a **list of leads (CSV)**, then scores each lead's buying intent (**High / Medium / Low**) using **rule-based logic + AI reasoning**.

**Technologies Used:** FastAPI, Python, Pandas, Uvicorn, OpenAI API (optional)

**Endpoints:** `/offer`, `/leads/upload`, `/score`, `/results`

---

## Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/lead-scoring-backend.git
cd lead-scoring-backend
```

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the environment:**
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **(Optional) Set your OpenAI API key for AI scoring:**
```bash
setx OPENAI_API_KEY "your_openai_api_key_here"
```

6. **Run the backend:**
```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://127.0.0.1:8000`.

---

## API Usage Examples

### 1️⃣ Upload Offer
**POST** `/offer`  
Content-Type: `application/json`

```json
{
  "name": "AI Outreach Automation",
  "value_props": ["24/7 outreach", "6x more meetings"],
  "ideal_use_cases": ["B2B SaaS mid-market"]
}
```

### 2️⃣ Upload Leads CSV
**POST** `/leads/upload`  
Body → **form-data**  
- Key: `file` (must be exactly `file`)  
- Type: File → select your CSV file  

**CSV format example:**
```csv
name,role,company,industry,location,linkedin_bio
Ava Patel,Head of Growth,FlowMetrics,B2B SaaS,New York,"Helping SaaS companies grow with data-driven marketing"
John Doe,Software Engineer,TechWorks,IT Services,Boston,"Backend engineer with 5 years experience"
Emma Singh,Marketing Manager,SalesFlow,B2B SaaS,San Francisco,"Marketing leader focused on lead generation"
```

### 3️⃣ Run Scoring
**POST** `/score`  
- No body required  
- Returns a message: `{"message": "Scoring complete!", "count": <number_of_leads>}`

### 4️⃣ Get Results
**GET** `/results`  
- Returns JSON array of scored leads with:
  - `name`, `role`, `company`, `intent`, `score`, `reasoning`

**Example:**
```json
[
  {
    "name": "Ava Patel",
    "role": "Head of Growth",
    "company": "FlowMetrics",
    "industry": "B2B SaaS",
    "location": "New York",
    "linkedin_bio": "Helping SaaS companies grow with data-driven marketing",
    "intent": "High",
    "score": 85,
    "reasoning": "Fits ICP SaaS mid-market and role is decision maker."
  }
]
```

---

## Scoring Logic

### Rule Layer (max 50 points)
- **Role relevance:**  
  - Decision maker: +20  
  - Influencer: +10  
  - Else: 0  
- **Industry match:**  
  - Exact ICP: +20  
  - Adjacent: +10  
  - Else: 0  
- **Data completeness:** all fields present +10  

### AI Layer (max 50 points)
- Sends lead + offer details to OpenAI  
- **Prompt used:**  
  `"Classify intent (High/Medium/Low) and explain reasoning in 1–2 sentences."`  
- **Mapping:**  
  - High → 50 points  
  - Medium → 30 points  
  - Low → 10 points  

**Final Score = Rule points + AI points**

---

## Optional / Bonus
- Export results as CSV via `/export` endpoint (if implemented)  
- Unit tests for rule layer  
- Dockerfile for containerization  

---

## Notes
- Always **upload the offer first**, then leads, then run `/score`.  
- Data is stored **in memory**; restarting the server clears offers and leads.  
- If OpenAI API key is missing, AI scoring will **fallback to default Medium intent**.
