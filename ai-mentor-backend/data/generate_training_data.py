import random
import pandas as pd


def generate_sample():
    math = random.uniform(0.3, 1)
    science = random.uniform(0.3, 1)
    english = random.uniform(0.3, 1)

    logical = random.uniform(0.3, 1)
    creativity = random.uniform(0.3, 1)
    scientific = random.uniform(0.3, 1)
    communication = random.uniform(0.3, 1)
    leadership = random.uniform(0.3, 1)

    academic_index = (math + science + english) / 3

    # Simple logic-based label generation
    if math > 0.7 and logical > 0.7:
        label = "PCM"
    elif science > 0.7 and scientific > 0.7:
        label = "PCB"
    elif math > 0.6 and communication > 0.6:
        label = "Commerce"
    else:
        label = "Arts"

    return [
        academic_index, math, science, english,
        logical, creativity, scientific,
        communication, leadership,
        label
    ]


data = [generate_sample() for _ in range(2000)]

df = pd.DataFrame(data, columns=[
    "academic_index", "math", "science", "english",
    "logical", "creativity", "scientific",
    "communication", "leadership",
    "label"
])

df.to_csv("data/stream_training_data.csv", index=False)