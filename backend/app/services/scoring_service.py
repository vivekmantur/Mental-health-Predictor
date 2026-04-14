# ---------------------------------------------------------
# PHQ-9 Scoring Service
# ---------------------------------------------------------
def calculate_phq9_score(scores):
    """
    Calculates total PHQ-9 score and determines severity level.

    Args:
        scores (list[int]): List of 9 scores (each between 0–3)

    Returns:
        tuple:
            total_score (int): Sum of all scores (0–27)
            severity (str): Severity category
    """

    # -----------------------------------------------------
    # Calculate total score
    # -----------------------------------------------------
    total_score = sum(scores)

    # -----------------------------------------------------
    # Determine severity based on PHQ-9 standard ranges
    # -----------------------------------------------------
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

    # -----------------------------------------------------
    # Return results
    # -----------------------------------------------------
    return total_score, severity