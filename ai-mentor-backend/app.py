from ai_engine.main_recommendation_pipeline import run_recommendation

raw_input = {
    "math": 85,
    "science": 78,
    "english": 72,
    "logical_score": 8,
    "creativity_score": 6,
    "scientific_interest": 7,
    "communication": 7,
    "leadership": 6,
    "stress_level": 2,
    "risk_level": 1,
    "budget": 600000,
    "location": "MP",
    "education_level": "class_10"
}

result = run_recommendation(raw_input)

print(result)