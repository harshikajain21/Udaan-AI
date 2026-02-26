def generate_improvement_plan(profile, decision_output, institution_matches):

    dimension_scores = decision_output["dimension_scores"]
    risk_flags = decision_output["risk_flags"]

    plan = {}

    # ----------------------------
    # Academic Improvement
    # ----------------------------
    if dimension_scores.get("academic_strength", 1.0) < 0.6:
        plan["academic_action"] = (
            "Improve core subject performance, especially mathematics and science. "
            "Focus on concept clarity and structured problem-solving practice."
        )

    # ----------------------------
    # Competition Strategy
    # ----------------------------
    if dimension_scores.get("competition_readiness", 1.0) < 0.5:
        plan["exam_strategy"] = (
            "Your competition readiness is currently low. "
            "Develop a percentile-targeted preparation strategy. "
            "Focus on mock test performance analysis and weak-topic reinforcement."
        )

    # ----------------------------
    # Financial Strategy
    # ----------------------------
    if dimension_scores.get("financial_feasibility", 1.0) < 0.6:
        plan["financial_strategy"] = (
            "Consider exploring scholarships, government aid, education loans, "
            "or identifying lower-cost institutions with strong ROI."
        )

    # ----------------------------
    # Psychological Stability
    # ----------------------------
    if dimension_scores.get("psychological_alignment", 1.0) < 0.5:
        plan["stress_strategy"] = (
            "Work on stress management and workload balance. "
            "Consider gradual preparation planning instead of high-intensity bursts."
        )

    # ----------------------------
    # Backup Institution Strategy
    # ----------------------------
    if institution_matches and len(institution_matches) > 1:
        backup = institution_matches[1]
        college_name = backup.get('name') or backup.get('college') or 'Unknown College'
        tier = backup.get('tier', 'Standard')
        plan["backup_strategy"] = (
            f"Keep {college_name} (Tier {tier}) as a parallel realistic target "
            "while preparing for higher-tier institutions."
        )

    # ----------------------------
    # If Strong Profile
    # ----------------------------
    if not plan:
        plan["status"] = (
            "Your profile is well-aligned with your selected pathway. "
            "Focus on consistent preparation and performance optimization."
        )

    return plan