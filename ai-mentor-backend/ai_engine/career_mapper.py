import json
import os
import numpy as np


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAREER_PATH = os.path.join(BASE_DIR, "data", "careers.json")


def load_careers():
    with open(CAREER_PATH, "r") as f:
        return json.load(f)


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot / (norm1 * norm2)


def map_careers(profile, selected_degree):

    careers = load_careers()

    student_vector = [
        profile.subject_scores["math"],
        profile.psychological_vector[0],  # logic
        profile.psychological_vector[1],  # creativity
        profile.psychological_vector[3],  # communication
        profile.stress_level / 2
    ]

    matches = []

    for career in careers:

        # 🔥 Filter by DEGREE now (not stream)
        if career["degree"] != selected_degree:
            continue

        career_vector = [
            career["math"],
            career["logic"],
            career["creativity"],
            career["communication"],
            career["stress"]
        ]

        similarity = cosine_similarity(student_vector, career_vector)

        matches.append({
            "career": career["career"],
            "compatibility": round(float(similarity * 100), 2)
        })

    matches = sorted(matches, key=lambda x: x["compatibility"], reverse=True)

    return matches