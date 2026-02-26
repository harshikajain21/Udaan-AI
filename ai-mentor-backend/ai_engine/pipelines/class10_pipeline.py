from ..feature_engineering import calculate_stream_affinities
from ..rule_engine import apply_rules
from ..ml_predictor import predict_stream
from ..degree_mapper import rank_degrees
from ..career_mapper import map_careers
from ..institution_matcher import match_institutions
from ..explanation_engine import generate_full_explanation
from ..stream_decision_scorer import compute_stream_decision_score


def run_class10_pipeline(profile):

    # -----------------------------------
    #  Stream Affinity + Rule Filtering
    # -----------------------------------
    affinities = calculate_stream_affinities(profile)
    rule_output = apply_rules(profile, affinities)

    probabilities = predict_stream(profile)

    # Remove restricted streams
    probabilities = {
        k: v for k, v in probabilities.items()
        if k not in rule_output["restricted_paths"]
    }

    # Safety fallback if all streams removed
    if not probabilities:
        probabilities = {"Undetermined": 1.0}

    # Re-normalize probabilities
    total = sum(probabilities.values())
    if total > 0:
        probabilities = {k: v / total for k, v in probabilities.items()}

    probabilities = dict(
        sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    )

    top_stream = next(iter(probabilities))

    # -----------------------------------
    # Preview Future Path
    # -----------------------------------
    degree_matches = rank_degrees(profile, top_stream)

    top_degree = degree_matches[0]["degree"] if degree_matches else None

    career_matches = []
    if top_degree:
        career_matches = map_careers(profile, top_degree)

    institution_matches = match_institutions(profile, top_stream)

    # -----------------------------------
    # Decision Intelligence
    # -----------------------------------
    decision_output = compute_stream_decision_score(
        profile,
        probabilities
    )

    confidence = round(decision_output["decision_score"], 3)

    # -----------------------------------
    #  Explanation
    # -----------------------------------
    explanation = generate_full_explanation(
        profile,
        top_stream,
        degree_matches,
        career_matches,
        institution_matches,
        confidence
    )

    # -----------------------------------
    # Final Response
    # -----------------------------------
    return {
        "education_stage": "class_10",
        "recommended_stream": top_stream,
        "confidence_score": confidence,
        "probabilities": probabilities,
        "decision_intelligence": decision_output,
        "degree_matches": degree_matches,
        "career_matches": career_matches,
        "institution_matches": institution_matches,
        "pathway_explanation": explanation,
        "restricted_paths": rule_output["restricted_paths"],
        "risk_flags": decision_output["risk_flags"]
    }