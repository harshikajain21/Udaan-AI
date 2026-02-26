# ai_engine/confidence_calculator.py

def calculate_confidence(probabilities):

    values = list(probabilities.values())

    if len(values) < 2:
        return 0.6

    margin = values[0] - values[1]

    confidence = min(0.95, max(0.5, margin + 0.5))

    return round(confidence, 2)