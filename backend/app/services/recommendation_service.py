"""
Recommendation Generation Service

Generates actionable mental health recommendations using LLM
based on PHQ-9 assessment context.

Design Notes:
- Produces 4–5 bullet-point suggestions
- Ensures non-empty output for consistent UX
- Includes fallback responses for reliability
"""

from app.llm.llm_client import client


def generate_recommendation(context: str, severity: str) -> str:
    """
    Generate actionable recommendations based on PHQ-9 result.

    Args:
        context (str): Structured PHQ-9 context (score, severity, notes)
        severity (str): Severity level (currently not directly used in prompt)

    Returns:
        str: Bullet-point recommendations

    Behavior:
        - Produces 4–5 actionable suggestions
        - Ensures non-empty fallback response
        - Handles API failures gracefully
    """

    # ---------------------------------------------------------
    # Primary Prompt (Main Active Logic)
    # ---------------------------------------------------------
    prompt = f"""
    Based on this PHQ-9 result:

    {context}

    Provide 4-5 clear bullet point recommendations.

    IMPORTANT:
    - Always return useful suggestions
    - Do NOT return empty
    """

    try:
        # Call LLM API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Always provide helpful actionable advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5  # Balanced creativity and clarity
        )

        # Extract output
        output = response.choices[0].message.content.strip()

        # Fallback if model returns empty
        return output if output else (
            "• Maintain a routine\n"
            "• Get enough sleep\n"
            "• Talk to someone\n"
            "• Practice relaxation"
        )

    except Exception as e:
        # Log error (replace with proper logging in production)
        print("❌ RECOMMENDATION ERROR:", str(e))

        return (
            "• Try relaxation\n"
            "• Stay active\n"
            "• Seek support"
        )


