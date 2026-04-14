from app.llm.llm_client import generate_insight as llm_call


# ---------------------------------------------------------
# Recommendation Generation Service
# ---------------------------------------------------------
def generate_recommendation(answers, severity):
    """
    Generates personalized mental health recommendations based on:
    - User's severity level
    - (Optional context) user responses

    Args:
        answers (list[str]): User's PHQ-9 textual responses
        severity (str): Calculated severity level

    Returns:
        str: AI-generated recommendations
    """

    # -----------------------------------------------------
    # Prompt construction for LLM
    # -----------------------------------------------------
    prompt = f"""
        You are a mental health assistant.

        User condition: {severity}

        Provide:
        - Practical suggestions
        - Daily improvements
        - When to seek help

        Keep it simple and supportive.
        """

    # -----------------------------------------------------
    # Call LLM client and return recommendations
    # -----------------------------------------------------
    return llm_call(prompt)