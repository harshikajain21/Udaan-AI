import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTITUTION_PATH = os.path.join(BASE_DIR, "data", "institutions.json")


def load_institutions():
    with open(INSTITUTION_PATH, "r") as f:
        return json.load(f)


def classify_risk(student_percentile, cutoff_percentile):
    diff = student_percentile - cutoff_percentile

    if diff >= 3:
        return "Safe"
    elif -3 <= diff < 3:
        return "Target"
    else:
        return "Dream"


def calculate_roi(total_cost, avg_package, placement_rate):
    if total_cost == 0:
        return 0
    return (avg_package * placement_rate) / total_cost


def match_institutions(profile, stream):

    institutions = load_institutions()

    student_percentile = profile.academic_index * 100
    student_budget = profile.budget
    student_location = profile.location.lower()

    ranked_colleges = []

    for inst in institutions:

        # ----------------------------
        # Stream Filter
        # ----------------------------
        if inst["program"]["stream"] != stream:
            continue

        cutoff_percentile = inst["admission"]["cutoff_percentile"]
        exam = inst["admission"]["exam"]

        annual_fees = inst["financials"]["annual_fees"]
        hostel_fees = inst["financials"]["hostel_fees"]
        total_cost = annual_fees + hostel_fees

        avg_package = inst["financials"]["average_package"]
        placement_rate = inst["financials"]["placement_rate"]

        tier = inst["tier"]
        college_state = inst["location"]["state"].lower()

        # ----------------------------
        # Risk classification
        # ----------------------------
        category = classify_risk(student_percentile, cutoff_percentile)

        # ----------------------------
        # ROI
        # ----------------------------
        roi_score = calculate_roi(total_cost, avg_package, placement_rate)

        # ----------------------------
        # Financial Risk
        # ----------------------------
        financial_risk = total_cost > student_budget

        # ----------------------------
        # Tier Weight
        # ----------------------------
        if tier == 1:
            tier_weight = 1.2
        elif tier == 2:
            tier_weight = 1.0
        else:
            tier_weight = 0.8

        # ----------------------------
        # Location Boost
        # ----------------------------
        location_bonus = 1.1 if college_state == student_location else 1.0

        # ----------------------------
        # Risk Multiplier
        # ----------------------------
        if category == "Safe":
            risk_multiplier = 1.1
        elif category == "Target":
            risk_multiplier = 1.0
        else:
            risk_multiplier = 0.75

        # ----------------------------
        # Financial Multiplier
        # ----------------------------
        financial_multiplier = 0.7 if financial_risk else 1.0

        # ----------------------------
        # Final Ranking Score
        # ----------------------------
        ranking_score = (
            roi_score *
            tier_weight *
            location_bonus *
            risk_multiplier *
            financial_multiplier
        )

        ranked_colleges.append({
            "college": inst["college_name"],
            "degree": inst["program"]["degree"],
            "branch": inst["program"]["branch"],
            "exam": exam,
            "tier": tier,
            "category": category,
            "cutoff_percentile": cutoff_percentile,
            "total_cost": total_cost,
            "roi_score": round(roi_score, 2),
            "placement_rate": placement_rate,
            "financial_risk": financial_risk,
            "ranking_score": round(ranking_score, 2)
        })

    ranked_colleges = sorted(
        ranked_colleges,
        key=lambda x: x["ranking_score"],
        reverse=True
    )

    return ranked_colleges