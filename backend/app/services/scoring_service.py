"""
PHQ-9 Scoring Service

Calculates total score and severity level based on PHQ-9 responses.

PHQ-9 Overview:
- 9 questions, each scored from 0 to 3
- Total score range: 0 to 27
- Used to assess depression severity

Severity Classification:
- 0            → None
- 1–4          → Minimal depression
- 5–9          → Mild depression
- 10–14        → Moderate depression
- 15–19        → Moderately severe depression
- 20–27        → Severe depression
"""


# ---------------------------------------------------------
# Calculate PHQ-9 Score & Severity
# ---------------------------------------------------------
def calculate_phq9_score(answers):
    """
    Calculate PHQ-9 total score and severity.

    Args:
        answers (list[int]): List of 9 responses (each value 0–3)

    Returns:
        tuple:
            - score (int): Total PHQ-9 score (0–27)
            - severity (str): Severity category

    Notes:
        - Input validation (length and range) is handled upstream
        - This function is purely deterministic (no AI involved)
    """

    # ---------------------------------------------------------
    # Step 1: Calculate total score
    # ---------------------------------------------------------
    score = sum(answers)

    # ---------------------------------------------------------
    # Step 2: Map score to severity level
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Return result
    # ---------------------------------------------------------
    return score, severity