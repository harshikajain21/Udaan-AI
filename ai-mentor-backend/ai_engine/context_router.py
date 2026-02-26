# ai_engine/context_router.py

def route_pipeline(profile):
    level = profile.education_level.lower()

    if level == "class_10":
        return "stream_recommendation"

    elif level == "class_12":
        return "degree_recommendation"

    elif level == "ug":
        return "career_recommendation"

    elif level == "graduate":
        return "specialization_recommendation"

    else:
        raise ValueError("Unsupported education level")