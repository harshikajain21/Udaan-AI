# ai_engine/main_recommendation_pipeline.py

from .profile_processor import process_raw_input
from .context_router import route_pipeline

# Stage-based pipelines
from .pipelines.class10_pipeline import run_class10_pipeline
from .pipelines.class12_pipeline import run_class12_pipeline


def run_recommendation(raw_input):

    # ----------------------------
    # Profile Processing
    # ----------------------------
    profile = process_raw_input(raw_input)

    # ----------------------------
    # Determine Education Stage
    # ----------------------------
    pipeline_type = route_pipeline(profile)

    # ----------------------------
    # Route to Appropriate Pipeline
    # ----------------------------
    if pipeline_type == "stream_recommendation":
        return run_class10_pipeline(profile)

    elif pipeline_type == "degree_recommendation":
        return run_class12_pipeline(profile)

    elif pipeline_type == "career_recommendation":
        return {
            "message": "UG pipeline not implemented yet."
        }

    elif pipeline_type == "specialization_recommendation":
        return {
            "message": "Graduate pipeline not implemented yet."
        }

    else:
        return {
            "error": "Unsupported education level."
        }