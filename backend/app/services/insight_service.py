from app.llm.llm_client import client


def generate_insight(context: str, severity: str) -> str:
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
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You must always respond with helpful content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        output = response.choices[0].message.content.strip()

        return output if output else "You may be experiencing some emotional strain. It's important to take care of your mental well-being."

    except Exception as e:
        print("❌ INSIGHT ERROR:", str(e))
        return "Unable to generate insight."
    prompt = f"""
    You are a mental health assistant.

    Based on the PHQ-9 assessment:

    {context}

    Provide:
    - A short, empathetic insight (3–4 lines)
    - Do NOT sound robotic
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful mental health assistant."},
                {"role": "user", "content": prompt}
            ], 
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ INSIGHT ERROR:", str(e))
        return "Unable to generate insight at the moment."