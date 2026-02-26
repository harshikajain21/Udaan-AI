# ai_engine/profile_processor.py

from .profile_schema import StudentProfile


def normalize_score(score, max_score=100):
    return score / max_score


def process_raw_input(raw_input):

    # ----------------------------
    # Academic Scores (Normalized)
    # ----------------------------
    subject_scores = {
        "math": normalize_score(raw_input.get("math", 0)),
        "science": normalize_score(raw_input.get("science", 0)),
        "english": normalize_score(raw_input.get("english", 0))
    }

    academic_index = sum(subject_scores.values()) / len(subject_scores)

    # ----------------------------
    # Psychological Vector (0–1 scale)
    # ----------------------------
    psychological_vector = [
        raw_input.get("logical_score", 0) / 10,
        raw_input.get("creativity_score", 0) / 10,
        raw_input.get("scientific_interest", 0) / 10,
        raw_input.get("communication", 0) / 10,
        raw_input.get("leadership", 0) / 10
    ]

    # ----------------------------
    # Return Unified Profile Object
    # ----------------------------
    return StudentProfile(
        academic_index=academic_index,
        subject_scores=subject_scores,
        psychological_vector=psychological_vector,
        stress_level=raw_input.get("stress_level", 2),
        risk_level=raw_input.get("risk_level", 1),
        budget=raw_input.get("budget", 0),
        location=raw_input.get("location", "Any"),  # FIXED
        education_level=raw_input.get("education_level", "class_10")
    )