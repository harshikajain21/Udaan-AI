from copy import deepcopy
from .profile_processor import process_raw_input
from .pipelines.class12_pipeline import run_class12_pipeline


def apply_overrides(profile_dict, overrides):
    updated = deepcopy(profile_dict)

    for key, value in overrides.items():
        if key in updated:
            updated[key] = value

    return updated


def run_simulation(base_input, scenario_overrides):

    # ----------------------------
    # Baseline Run
    # ----------------------------
    baseline_profile = process_raw_input(base_input)
    baseline_output = run_class12_pipeline(baseline_profile)

    # ----------------------------
    # Apply Overrides
    # ----------------------------
    updated_input = apply_overrides(base_input, scenario_overrides)

    # ----------------------------
    # Scenario Run
    # ----------------------------
    scenario_profile = process_raw_input(updated_input)
    scenario_output = run_class12_pipeline(scenario_profile)

    # ----------------------------
    # Compare Scores
    # ----------------------------
    baseline_score = baseline_output["decision_intelligence"]["decision_score"]
    scenario_score = scenario_output["decision_intelligence"]["decision_score"]

    score_delta = round(scenario_score - baseline_score, 3)

    return {
        "baseline_decision_score": baseline_score,
        "scenario_decision_score": scenario_score,
        "score_improvement": score_delta,
        "baseline_risks": baseline_output["decision_intelligence"]["risk_flags"],
        "scenario_risks": scenario_output["decision_intelligence"]["risk_flags"],
        "scenario_weights": scenario_output["decision_intelligence"]["applied_weights"]
    }