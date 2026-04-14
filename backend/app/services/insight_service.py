from app.llm.llm_client import generate_insight as llm_call


# ---------------------------------------------------------
# Insight Generation Service
# ---------------------------------------------------------
def generate_insight(answers, severity):
    """
    Generates a concise mental health insight based on:
    - User's free-text responses
    - Computed severity level

    Args:
        answers (list[str]): User's PHQ-9 textual responses
        severity (str): Calculated severity level

    Returns:
        str: AI-generated emotional insight
    """

    # -----------------------------------------------------
    # Prompt construction for LLM
    # -----------------------------------------------------
    prompt = f"""
        You are a mental health assistant.

        User responses:
        {answers}

        Severity: {severity}

        Give:
        - Emotional summary
        - Key struggles

        Keep it short, empathetic, human-like.
        """

    # -----------------------------------------------------
    # Call LLM client and return generated insight
    # -----------------------------------------------------
    return llm_call(prompt)