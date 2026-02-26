# stream_decision_scorer.py


def clamp(value, min_value=0, max_value=1):
    return max(min_value, min(value, max_value))


# ---------------------------------------
# Stream Stability (Probability Gap)
# ---------------------------------------
def calculate_stream_stability(probabilities):
    sorted_probs = sorted(probabilities.values(), reverse=True)

    if len(sorted_probs) < 2:
        return 1

    gap = sorted_probs[0] - sorted_probs[1]
    return clamp(gap)


# ---------------------------------------
# Academic Alignment
# ---------------------------------------
def calculate_academic_alignment(profile):
    return clamp(round(profile.academic_index, 3))


# ---------------------------------------
# Psychological Alignment
# ---------------------------------------
def calculate_psychological_alignment(profile):
    logical = profile.psychological_vector[0]
    creativity = profile.psychological_vector[1]
    communication = profile.psychological_vector[3]

    score = (logical + creativity + communication) / 3
    return clamp(round(score, 3))


# ---------------------------------------
# Risk Flags
# ---------------------------------------
def generate_stream_risk_flags(stability, academic):
    flags = []

    if stability < 0.15:
        flags.append("High Stream Ambiguity")

    if academic < 0.5:
        flags.append("Low Academic Foundation")

    return flags


# ---------------------------------------
# Main Decision Score (FIXED VERSION)
# ---------------------------------------
def compute_stream_decision_score(profile, probabilities):

    stability = calculate_stream_stability(probabilities)
    academic = calculate_academic_alignment(profile)
    psychological = calculate_psychological_alignment(profile)

    # Balanced scoring (no double counting)
    raw_score = (
        0.4 * stability +
        0.35 * academic +
        0.25 * psychological
    )

    # Soft cap to prevent overconfidence
    final_score = round(min(clamp(raw_score), 0.9), 3)

    risk_flags = generate_stream_risk_flags(stability, academic)

    return {
        "decision_score": final_score,
        "dimension_scores": {
            "stream_stability": stability,
            "academic_alignment": academic,
            "psychological_alignment": psychological
        },
        "risk_flags": risk_flags
    }