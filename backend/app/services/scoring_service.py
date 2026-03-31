import json

# 🧮 REQUIRED FUNCTION (you are missing this)
def calculate_phq9_score(scores):

    total_score = sum(scores)

    if total_score <= 4:
        severity = "Minimal"
    elif total_score <= 9:
        severity = "Mild"
    elif total_score <= 14:
        severity = "Moderate"
    elif total_score <= 19:
        severity = "Moderately Severe"
    else:
        severity = "Severe"

    return total_score, severity