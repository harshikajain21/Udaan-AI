# API CONTRACT

## POST /recommend

Request Body:
{
  "math": int,
  "science": int,
  "english": int,
  "logical_score": int,
  "creativity_score": int,
  "scientific_interest": int,
  "communication": int,
  "leadership": int,
  "stress_level": int,
  "risk_level": int,
  "budget": int,
  "location": string,
  "education_level": "class_10" | "class_12"
}

Response:
{
  "education_stage": string,
  "recommended_stream": string,
  "degree_matches": [],
  "career_matches": [],
  "institution_matches": [],
  "decision_intelligence": {},
  "confidence_score": float
}

## POST /simulate

Used for what-if scenario testing.