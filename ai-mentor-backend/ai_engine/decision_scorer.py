from .adaptive_weight_engine import get_adaptive_weights


# -------------------------------------------------
# Utility: clamp values between 0 and 1
# -------------------------------------------------
def clamp(value, min_value=0, max_value=1):
    return max(min_value, min(value, max_value))


# -------------------------------------------------
# Academic Score
# -------------------------------------------------
def calculate_academic_score(profile, top_degree, top_institution):
    student_percentile = profile.academic_index * 100
    cutoff = top_institution["cutoff_percentile"]
    gap = student_percentile - cutoff

    suitability = top_degree["suitability_score"] / 100

    if gap >= 5:
        gap_score = 1
    elif -5 <= gap < 5:
        gap_score = 0.7
    elif -15 <= gap < -5:
        gap_score = 0.4
    else:
        gap_score = 0.2

    score = (0.6 * suitability) + (0.4 * gap_score)

    return round(clamp(score), 3)


# -------------------------------------------------
# Financial Score
# -------------------------------------------------
def calculate_financial_score(profile, top_institution):
    budget = profile.budget
    cost = top_institution["total_cost"]
    roi = top_institution["roi_score"]

    if cost == 0:
        affordability_ratio = 0
    else:
        affordability_ratio = min(budget / cost, 1)

    roi_normalized = min(roi / 10, 1)

    score = (0.6 * affordability_ratio) + (0.4 * roi_normalized)

    return round(clamp(score), 3)


# -------------------------------------------------
# Competition Score
# -------------------------------------------------
def calculate_competition_score(profile, top_institution):
    tier = top_institution["tier"]
    cutoff = top_institution["cutoff_percentile"]
    student_percentile = profile.academic_index * 100

    gap = student_percentile - cutoff

    tier_penalty = {1: 0.3, 2: 0.2, 3: 0.1}.get(tier, 0.2)

    if gap >= 5:
        gap_factor = 0.9
    elif -5 <= gap < 5:
        gap_factor = 0.6
    else:
        gap_factor = 0.3

    raw_score = gap_factor - tier_penalty

    return round(clamp(raw_score), 3)


# -------------------------------------------------
# Psychological Score
# -------------------------------------------------
def calculate_psychological_score(profile, top_degree):
    stress_tolerance = 1 - (profile.stress_level / 10)
    degree_difficulty = top_degree["difficulty"]

    risk_alignment = 1 - abs(profile.risk_level - degree_difficulty)

    score = (0.5 * stress_tolerance) + (0.5 * risk_alignment)

    return round(clamp(score), 3)


# -------------------------------------------------
# Risk Flags
# -------------------------------------------------
def generate_risk_flags(academic, financial, competition):
    flags = []

    if academic < 0.5:
        flags.append("High Academic Risk")

    if financial < 0.5:
        flags.append("Financial Constraint Risk")

    if competition < 0.4:
        flags.append("High Competition Risk")

    return flags


# -------------------------------------------------
# Final Decision Score
# -------------------------------------------------
def compute_decision_score(profile, degree_matches, institution_matches):

    if not degree_matches or not institution_matches:
        return {
            "decision_score": 0,
            "dimension_scores": {},
            "applied_weights": {},
            "risk_flags": ["Insufficient Data"]
        }

    top_degree = degree_matches[0]
    top_institution = institution_matches[0]

    academic = calculate_academic_score(profile, top_degree, top_institution)
    financial = calculate_financial_score(profile, top_institution)
    competition = calculate_competition_score(profile, top_institution)
    psychological = calculate_psychological_score(profile, top_degree)

    # ----------------------------
    # Adaptive Weights
    # ----------------------------
    weights = get_adaptive_weights(profile)

    final_score = (
        (weights["academic"] * academic) +
        (weights["financial"] * financial) +
        (weights["competition"] * competition) +
        (weights["psychological"] * psychological)
    )

    final_score = round(clamp(final_score), 3)

    risk_flags = generate_risk_flags(academic, financial, competition)

    return {
        "decision_score": final_score,
        "dimension_scores": {
            "academic_strength": academic,
            "financial_feasibility": financial,
            "competition_readiness": competition,
            "psychological_alignment": psychological
        },
        "applied_weights": weights,
        "risk_flags": risk_flags
    }