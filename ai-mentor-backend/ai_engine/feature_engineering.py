# ai_engine/feature_engineering.py

def calculate_stream_affinities(profile):

    pcm_affinity = (
        0.4 * profile.subject_scores["math"] +
        0.4 * profile.subject_scores["science"] +
        0.2 * profile.psychological_vector[0]
    )

    pcb_affinity = (
        0.5 * profile.subject_scores["science"] +
        0.3 * profile.psychological_vector[2] +
        0.2 * profile.psychological_vector[0]
    )

    commerce_affinity = (
        0.5 * profile.subject_scores["math"] +
        0.3 * profile.psychological_vector[3] +
        0.2 * profile.psychological_vector[4]
    )

    arts_affinity = (
        0.6 * profile.psychological_vector[1] +
        0.4 * profile.psychological_vector[3]
    )

    return {
        "PCM": pcm_affinity,
        "PCB": pcb_affinity,
        "Commerce": commerce_affinity,
        "Arts": arts_affinity
    }