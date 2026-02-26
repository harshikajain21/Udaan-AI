import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEGREE_PATH = os.path.join(BASE_DIR, "data", "degrees.json")


def load_degrees():
    with open(DEGREE_PATH, "r") as f:
        return json.load(f)


def normalize_0_10(value):
    """
    Normalize 0–10 scale to 0–1
    """
    return min(max(value / 10, 0), 1)


def rank_degrees(profile, predicted_stream):

    degrees = load_degrees()
    ranked_degrees = []

    # ----------------------------
    # Normalize profile inputs safely
    # ----------------------------
    academic_score = min(max(profile.academic_index, 0), 1)
    stress_factor = normalize_0_10(profile.stress_level)
    risk_factor = normalize_0_10(profile.risk_level)

    for degree in degrees:

        if degree["stream"] != predicted_stream:
            continue

        difficulty = degree.get("difficulty", 0.7)
        competition = degree.get("competition_level", 0.7)

        # ----------------------------
        # Core Suitability Logic
        # ----------------------------

        difficulty_alignment = 1 - abs(difficulty - academic_score)

        suitability = (
            0.5 * academic_score +
            0.2 * stress_factor +
            0.1 * risk_factor +
            0.2 * difficulty_alignment
        )

        # Competition penalty (controlled, not aggressive)
        if competition > 0.8 and stress_factor < 0.4:
            suitability *= 0.9

        # ----------------------------
        # Hard Clamp (CRITICAL FIX)
        # ----------------------------
        suitability = min(max(suitability, 0), 1)

        ranked_degrees.append({
            "degree": degree["degree"],
            "suitability_score": round(suitability * 100, 2),
            "competition_level": competition,
            "difficulty": difficulty
        })

    ranked_degrees = sorted(
        ranked_degrees,
        key=lambda x: x["suitability_score"],
        reverse=True
    )

    return ranked_degrees