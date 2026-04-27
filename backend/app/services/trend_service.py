from app.llm.llm_client import get_llm_response
import json
import re

def extract_json(text: str):
    try:
        # extract JSON block using regex
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return None


def generate_trend_analysis(latest, previous):
    prompt = f"""
        You are a mental health assistant.

        Compare these two PHQ-9 assessments:

        Latest:
        Score: {latest.score}
        Severity: {latest.severity}
        Category: {latest.category}
        Disorder: {latest.disorder}

        Previous:
        Score: {previous.score}
        Severity: {previous.severity}

        Tasks:
        1. Give a short insight (1-2 lines) including:
        - whether condition improved or worsened
        - possible contributing factors (based on symptoms and notes)
        - DO NOT make definitive claims, use phrases like "may be related to"

        2. Provide highly specific recommendations tailored to the detected disorder

        IMPORTANT:
        - Do NOT say "you have this because..."
        - Use cautious, supportive language
        - Keep it professional and non-judgmental

        Return ONLY valid JSON.

        Format:
        {{
        "insight": "string",
        "recommendation": [
            "step 1",
            "step 2",
            "step 3"
        ]
        }}
        """

    response = get_llm_response(prompt)

    print("RAW LLM OUTPUT:", response)

    # ✅ CASE 1: already dict
    if isinstance(response, dict):
        return response

    # ✅ CASE 2: string → try JSON parse
    if isinstance(response, str):
        try:
            return json.loads(response)
        except Exception:
            pass

        # ✅ CASE 3: extract JSON from messy string
        try:
            import re
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass

    # ❌ fallback
    return {
        "insight": "Unable to generate insight at the moment.",
        "recommendation": ["Try again later"]
    }