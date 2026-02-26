def generate_full_explanation(
    profile,
    stream,
    degree_matches,
    career_matches,
    institution_matches,
    confidence_score
):

    explanation = {}

    # ----------------------------
    # Stream Reason
    # ----------------------------
    explanation["stream_reason"] = (
        f"{stream} aligns strongly with your academic strengths, "
        f"particularly your mathematical and logical aptitude."
    )

    # ----------------------------
    # Degree Reason
    # ----------------------------
    if degree_matches:
        top_degree = degree_matches[0]
        explanation["degree_reason"] = (
            f"{top_degree['degree']} shows highest suitability "
            f"({top_degree['suitability_score']}%) based on your academic strength "
            f"and psychological profile."
        )
    else:
        explanation["degree_reason"] = "No strong degree preference detected."

    # ----------------------------
    # Career Reason
    # ----------------------------
    if career_matches:
        top_career = career_matches[0]
        explanation["career_reason"] = (
            f"{top_career['career']} aligns with your profile "
            f"with {top_career['compatibility']}% compatibility."
        )
    else:
        explanation["career_reason"] = "Career alignment requires further exploration."

    # ----------------------------
    # Institutional Reasoning (Risk-Sensitive)
    # ----------------------------
    if institution_matches:

        top_college = institution_matches[0]

        student_percentile = round(profile.academic_index * 100, 2)
        cutoff_percentile = top_college["cutoff_percentile"]
        academic_gap = round(student_percentile - cutoff_percentile, 2)

        financial_risk = top_college["financial_risk"]

        # Academic Tone
        if academic_gap >= 3:
            academic_tone = "You are academically well-positioned for this institution."
        elif -3 <= academic_gap < 3:
            academic_tone = "Your profile is closely aligned with the cutoff, making this moderately competitive."
        elif -10 <= academic_gap < -3:
            academic_tone = "This institution is competitive for your current profile and may require improvement."
        else:
            academic_tone = "This institution is highly competitive relative to your current academic standing."

        # Financial Tone
        if financial_risk:
            financial_tone = "However, it may exceed your financial budget."
        else:
            financial_tone = "It falls within your financial capacity."

        explanation["institution_reason"] = (
            f"{top_college['college']} (Tier {top_college['tier']}) "
            f"requires approximately {cutoff_percentile}% percentile via {top_college['exam']}. "
            f"Your percentile difference is {academic_gap}. "
            f"{academic_tone} {financial_tone}"
        )

        # Backup Suggestion
        if len(institution_matches) > 1:
            backup = institution_matches[1]
            explanation["backup_strategy"] = (
                f"A strategic alternative is {backup['college']} "
                f"(Tier {backup['tier']}) categorized as {backup['category']}."
            )

    else:
        explanation["institution_reason"] = (
            "No institution matches found within your academic or financial constraints."
        )

    # ----------------------------
    # Confidence Reason
    # ----------------------------
    if confidence_score >= 0.85:
        level = "High"
    elif confidence_score >= 0.65:
        level = "Moderate"
    else:
        level = "Low"

    explanation["confidence_reason"] = (
        f"Overall recommendation confidence is {level} "
        f"({confidence_score * 100:.1f}%)."
    )

    return explanation