import os
import json
from groq import Groq
from dotenv import load_dotenv

# ---------------------------------------------------------
# Load environment variables (.env)
# ---------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------
# Initialize Groq client using API key
# ---------------------------------------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------------------------------------
# PHQ-9 Questions (used for better LLM context)
# ---------------------------------------------------------
PHQ9_QUESTIONS = [
    "1. Little interest or pleasure in doing things",
    "2. Feeling down, depressed, or hopeless",
    "3. Trouble falling or staying asleep, or sleeping too much",
    "4. Feeling tired or having little energy",
    "5. Poor appetite or overeating",
    "6. Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
    "7. Trouble concentrating on things, such as reading the newspaper or watching television",
    "8. Moving or speaking so slowly that other people could have noticed. Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
    "9. Thoughts that you would be better off dead, or of hurting yourself in some way"
]




# ---------------------------------------------------------
# Insight Generation (LLM-based)
# ---------------------------------------------------------
def generate_insight(prompt: str) -> str:
    """
    Generates mental health insight from user input using LLM.

    Args:
        prompt (str): User input / processed context

    Returns:
        str: Insight text
    """

    print("PROMPT TO LLM:", prompt)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a mental health assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


def get_llm_response(prompt: str) -> dict:
    """
    Calls LLM and returns structured JSON response
    with insight and recommendation.
    """

    print("PROMPT TO LLM:", prompt)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
                You are a mental health assistant.

                Always respond ONLY in valid JSON format like this:
                {
                "insight": "short supportive insight",
                "recommendation": "clear actionable recommendation"
                }
"""
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    raw_output = response.choices[0].message.content.strip()

    print("RAW LLM OUTPUT:", raw_output)

    # ✅ Try parsing JSON safely
    try:
        parsed = json.loads(raw_output)
        return {
            "insight": parsed.get("insight", ""),
            "recommendation": parsed.get("recommendation", "")
        }
    except Exception as e:
        print("JSON PARSE ERROR:", e)

        # 🔥 fallback (VERY IMPORTANT)
        return {
            "insight": raw_output,
            "recommendation": "Please consider consulting a professional for further guidance."
        }