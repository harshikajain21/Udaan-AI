import json
import os
import re
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai_engine.main_recommendation_pipeline import run_recommendation
from ai_engine.simulation_engine import run_simulation

app = FastAPI(
    title="AI Mentor Recommendation Engine",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Database Parsing
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'DATABASE'))

def load_colleges():
    college_file = os.path.join(DATABASE_DIR, "college_master.txt")
    if not os.path.exists(college_file):
        return []
    with open(college_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    # Parse multiple JSON arrays by merging them
    content = re.sub(r'\]\s*\[', ',', content)
    try:
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing college_master.txt: {e}")
        return []

def load_hard_rules():
    rules_file = os.path.join(DATABASE_DIR, "hard_rules.json")
    if not os.path.exists(rules_file):
        return []
    with open(rules_file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(f"Error parsing hard_rules.json: {e}")
            return []

COLLEGES = load_colleges()
HARD_RULES = load_hard_rules()

def filter_institutions(recommended_stream: str):
    rejected_streams = set()
    for rule in HARD_RULES:
        condition = rule.get("if", {})
        stream_cond = condition.get("stream", {})
        if "$ne" in stream_cond:
            required_stream = stream_cond["$ne"]
            if recommended_stream != required_stream:
                if required_stream == "PCB": rejected_streams.add("PCB")
                if required_stream == "Commerce": rejected_streams.add("Commerce")
                if required_stream == "PCM": rejected_streams.add("PCM")
                
    filtered = []
    for c in COLLEGES:
        c_stream = c.get("stream")
        if c_stream in rejected_streams:
            continue
            
        match_score = 95 if c_stream == recommended_stream else 70
        filtered.append({
            "name": c.get("name"),
            "tier": c.get("type", "Standard"),
            "match_score": match_score,
            "location": c.get("state", "Unknown")
        })
        
    filtered.sort(key=lambda x: x["match_score"], reverse=True)
    return filtered[:5]

# ----------------------------
# Request Schema
# ----------------------------
class StudentInput(BaseModel):
    math: float
    science: float
    english: float
    logical: float
    creativity: float
    scientific_interest: float
    communication: float
    leadership: float
    stress_level: int
    risk_level: int
    budget: int
    location: str
    education_level: str

# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def root():
    return {"message": "AI Mentor API is running 🚀"}

# ----------------------------
# Recommendation Endpoint
# ----------------------------
@app.post("/recommend")
def recommend(student: StudentInput):
    engine_input = student.dict()
    # Map back to pipeline required fields
    engine_input["logical_score"] = engine_input.pop("logical")
    engine_input["creativity_score"] = engine_input.pop("creativity")
    
    base_result = run_recommendation(engine_input)
    recommended_stream = base_result.get("recommended_stream", "PCM")
    
    institution_matches = filter_institutions(recommended_stream)
    
    # Format explanation if it's a dict
    explanation_raw = base_result.get("pathway_explanation", "Based on your inputs, this is the optimal pathway.")
    if isinstance(explanation_raw, dict):
        explanation_str = "\n\n".join(f"{v}" for k, v in explanation_raw.items() if v)
    else:
        explanation_str = str(explanation_raw)
        
    # Return structure perfectly matching frontend/types/recommendation.ts
    result = {
        "recommended_stream": recommended_stream,
        "confidence_score": base_result.get("confidence_score", 0.9),
        "decision_intelligence": base_result.get("decision_intelligence", {
            "academic_strength": 85,
            "financial_feasibility": 80,
            "competition_readiness": 75,
            "psychological_alignment": 90,
            "risk_flags": []
        }),
        "degree_matches": base_result.get("degree_matches", []),
        "career_matches": base_result.get("career_matches", []),
        "institution_matches": institution_matches,
        "improvement_plan": base_result.get("improvement_plan", []),
        "explanation": explanation_str
    }
    
    return result

@app.post("/simulate")
def simulate(data: dict):
    base_input = data.get("base_profile")
    overrides = data.get("overrides", {})

    if not base_input:
        return {"error": "base_profile is required"}

    result = run_simulation(base_input, overrides)
    return result