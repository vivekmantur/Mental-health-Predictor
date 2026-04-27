from app.llm.llm_client import client


def generate_recommendation(context: str, severity: str) -> str:
    prompt = f"""
    Based on this PHQ-9 result:

    {context}

    Provide 4-5 clear bullet point recommendations.

    IMPORTANT:
    - Always return useful suggestions
    - Do NOT return empty
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Always provide helpful actionable advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        output = response.choices[0].message.content.strip()

        return output if output else "• Maintain a routine\n• Get enough sleep\n• Talk to someone\n• Practice relaxation"

    except Exception as e:
        print("❌ RECOMMENDATION ERROR:", str(e))
        return "• Try relaxation\n• Stay active\n• Seek support"
    prompt = f"""
    Based on this PHQ-9 result:

    {context}

    Provide:
    - Practical, actionable suggestions
    - Keep it simple and supportive
    - 4–5 bullet points
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a supportive mental health advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ RECOMMENDATION ERROR:", str(e))
        return "Unable to generate recommendations at the moment."