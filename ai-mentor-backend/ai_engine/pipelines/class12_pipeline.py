from ..degree_mapper import rank_degrees
from ..career_mapper import map_careers
from ..institution_matcher import match_institutions
from ..explanation_engine import generate_full_explanation
from ..entrance_mapper import rank_entrance_exams
from ..decision_scorer import compute_decision_score
from ..improvement_engine import generate_improvement_plan


def run_class12_pipeline(profile):

    # ----------------------------
    # Infer Stream from Subject Strength
    # ----------------------------
    inferred_stream = "PCM" if profile.subject_scores["math"] > 0.6 else "PCB"

    # ----------------------------
    # Degree Ranking
    # ----------------------------
    degree_matches = rank_degrees(profile, inferred_stream)
    top_degree = degree_matches[0]["degree"] if degree_matches else None

    # ----------------------------
    # Entrance Exams
    # ----------------------------
    entrance_matches = []
    if top_degree:
        entrance_matches = rank_entrance_exams(profile, top_degree)

    # ----------------------------
    # Career Mapping
    # ----------------------------
    career_matches = []
    if top_degree:
        career_matches = map_careers(profile, top_degree)

    # ----------------------------
    # Institution Matching
    # ----------------------------
    institution_matches = match_institutions(profile, inferred_stream)

    # ----------------------------
    # Decision Intelligence Core
    # ----------------------------
    decision_output = compute_decision_score(
        profile,
        degree_matches,
        institution_matches
    )

    # ----------------------------
    # Confidence (Derived From Decision Score)
    # ----------------------------
    confidence = round(decision_output["decision_score"], 3)

    # ----------------------------
    # Improvement Roadmap
    # ----------------------------
    improvement_plan = generate_improvement_plan(
        profile,
        decision_output,
        institution_matches
    )

    # ----------------------------
    # Explanation
    # ----------------------------
    explanation = generate_full_explanation(
        profile,
        inferred_stream,
        degree_matches,
        career_matches,
        institution_matches,
        confidence
    )

    # ----------------------------
    # Final Response
    # ----------------------------
    return {
        "education_stage": "class_12",
        "recommended_stream": inferred_stream,
        "degree_matches": degree_matches,
        "entrance_exam_matches": entrance_matches,
        "career_matches": career_matches,
        "institution_matches": institution_matches,
        "confidence_score": confidence,
        "decision_intelligence": decision_output,
        "improvement_plan": improvement_plan,
        "pathway_explanation": explanation
    }