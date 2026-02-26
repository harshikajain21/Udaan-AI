import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM_PATH = os.path.join(BASE_DIR, "data", "entrance_exams.json")


def load_exams():
    with open(EXAM_PATH, "r") as f:
        return json.load(f)


def rank_entrance_exams(profile, selected_degree):

    exams = load_exams()

    ranked_exams = []

    for exam in exams:

        if exam["degree"] != selected_degree:
            continue

        competition = exam.get("competition_level", 0.7)
        difficulty = exam.get("difficulty", 0.7)

        academic_score = profile.academic_index
        stress_factor = profile.stress_level / 2  # normalize 0–2 → 0–1
        risk_factor = profile.risk_level / 2

        # Suitability formula
        suitability = (
            0.5 * academic_score +
            0.2 * stress_factor +
            0.1 * risk_factor +
            0.2 * (1 - abs(difficulty - academic_score))
        )

        # Penalize very competitive exams if low stress tolerance
        if competition > 0.85 and stress_factor < 0.5:
            suitability *= 0.8

        ranked_exams.append({
            "exam": exam["exam"],
            "suitability_score": round(suitability * 100, 2),
            "competition_level": competition,
            "difficulty": difficulty
        })

    ranked_exams = sorted(
        ranked_exams,
        key=lambda x: x["suitability_score"],
        reverse=True
    )

    return ranked_exams