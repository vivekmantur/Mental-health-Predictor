# ---------------------------------------------------------
# PHQ-9 Scoring Service
# ---------------------------------------------------------
def calculate_phq9_score(answers):
    score = sum(answers)

    if score == 0:
        severity = "None"
    elif score <= 4:
        severity = "None Minimal"
    elif score <= 9:
        severity = "Mild"
    elif score <= 14:
        severity = "Moderate"
    elif score <= 19:
        severity = "Moderately Severe"
    else:
        severity = "Severe"

    return score, severity