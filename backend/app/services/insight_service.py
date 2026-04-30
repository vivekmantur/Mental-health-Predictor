"""
Insight Generation Service

Generates empathetic mental health insights using LLM
based on PHQ-9 assessment context.

Design Notes:
- Uses LLM (Groq / LLaMA) for natural language generation
- Includes fallback responses for reliability
- Ensures non-empty output for better UX
"""

from app.llm.llm_client import client


def generate_insight(context: str, severity: str) -> str:
    """
    Generate an empathetic mental health insight.

    Args:
        context (str): Structured PHQ-9 context (score, severity, notes)
        severity (str): Severity level (currently not directly used in prompt)

    Returns:
        str: Generated insight text

    Behavior:
        - Produces a 3–4 line empathetic paragraph
        - Ensures non-empty fallback response
        - Handles API failures gracefully
    """

    # ---------------------------------------------------------
    # Primary Prompt (Main Active Logic)
    # ---------------------------------------------------------
    prompt = f"""
    You are a mental health assistant.

    Based on the PHQ-9 result below:

    {context}

    Write a short, empathetic paragraph (3-4 lines).
    Be specific and helpful.

    IMPORTANT:
    - Do NOT return empty response
    - Always give meaningful output
    """

    try:
        # Call LLM API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You must always respond with helpful content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5  # Balanced creativity + stability
        )

        # Extract response text
        output = response.choices[0].message.content.strip()

        # Fallback if model returns empty response
        return output if output else (
            "You may be experiencing some emotional strain. "
            "It's important to take care of your mental well-being."
        )

    except Exception as e:
        # Log error (should be replaced with proper logging in production)
        print("❌ INSIGHT ERROR:", str(e))

        return "Unable to generate insight."

