import joblib
import os
import pandas as pd


# Safe absolute path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "stream_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "stream_encoder.pkl")

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)


def predict_stream(profile):

    input_df = pd.DataFrame([{
        "academic_index": profile.academic_index,
        "math": profile.subject_scores["math"],
        "science": profile.subject_scores["science"],
        "english": profile.subject_scores["english"],
        "logical": profile.psychological_vector[0],
        "creativity": profile.psychological_vector[1],
        "scientific": profile.psychological_vector[2],
        "communication": profile.psychological_vector[3],
        "leadership": profile.psychological_vector[4],
    }])

    probabilities = model.predict_proba(input_df)[0]

    labels = encoder.inverse_transform(range(len(probabilities)))

    result = {
    label: float(prob)
    for label, prob in zip(labels, probabilities)
    }

    return dict(
        sorted(result.items(), key=lambda x: x[1], reverse=True)
    )