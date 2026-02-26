def get_adaptive_weights(profile):

    academic = 0.40
    financial = 0.25
    competition = 0.20
    psychological = 0.15

    # ----------------------------
    # Risk Tolerance Adjustment
    # ----------------------------
    if profile.risk_level >= 7:
        competition -= 0.05
        academic += 0.05

    # ----------------------------
    # Budget Sensitivity
    # ----------------------------
    if profile.budget < 250000:
        financial += 0.10
        academic -= 0.05
        competition -= 0.05

    # ----------------------------
    # Stress Sensitivity
    # ----------------------------
    if profile.stress_level >= 7:
        psychological += 0.10
        academic -= 0.05
        competition -= 0.05

    # ----------------------------
    # Normalize
    # ----------------------------
    total = academic + financial + competition + psychological

    academic /= total
    financial /= total
    competition /= total
    psychological /= total

    return {
        "academic": round(academic, 3),
        "financial": round(financial, 3),
        "competition": round(competition, 3),
        "psychological": round(psychological, 3)
    }