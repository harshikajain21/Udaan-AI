# ai_engine/rule_engine.py

def apply_rules(profile, affinities):

    restricted = []
    risk_flags = []

    # Hard rule
    if profile.subject_scores["math"] < 0.5:
        restricted.append("PCM")

    # Stress rule
    if profile.stress_level == 0:
        risk_flags.append("Low stress tolerance")

    eligible = {
        k: v for k, v in affinities.items()
        if k not in restricted
    }

    return {
        "eligible_paths": eligible,
        "restricted_paths": restricted,
        "risk_flags": risk_flags
    }