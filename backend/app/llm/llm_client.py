import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_score_answers(answers):
    print("INPUT ANSWERS:", answers)  # ✅ DEBUG
    prompt = f"""
    You are a clinical PHQ-9 scoring assistant.

    Each question measures how frequently the user experiences a symptom.

    Your task:
    Assign a score (0–3) for each answer based on BOTH:
    1. Explicit frequency words (preferred)
    2. Implied frequency from context (if no keywords)

    SCORING:
    0 = Not at all (no occurrence or very rare)
    1 = Several days (sometimes, occasional, few days)
    2 = More than half the days (often, frequent, many days)
    3 = Nearly every day (almost daily, constantly, all the time)

    IMPORTANT RULES:
    - First priority → explicit frequency words
    - If no explicit words → infer carefully from meaning
    - DO NOT exaggerate severity
    - If unclear → choose lower score
    - Be consistent across all answers

    QUESTION CONTEXT:
    1. Interest or pleasure
    2. Feeling depressed
    3. Sleep issues
    4. Energy levels
    5. Appetite
    6. Self-worth
    7. Concentration
    8. Movement/restlessness
    9. Self-harm thoughts (CRITICAL)

    SPECIAL RULE FOR Q9:
    - Any mention of self-harm or death → minimum score = 1

    STRICT OUTPUT:
    - Return ONLY JSON
    - No explanation
    - Format: {{"scores":[s1,s2,s3,s4,s5,s6,s7,s8,s9]}}

    INPUT:
    1. {answers[0]}
    2. {answers[1]}
    3. {answers[2]}
    4. {answers[3]}
    5. {answers[4]}
    6. {answers[5]}
    7. {answers[6]}
    8. {answers[7]}
    9. {answers[8]}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw_output = response.choices[0].message.content.strip()

    print("🔴 RAW LLM OUTPUT:", raw_output)   # ✅ DEBUG

    return extract_scores(raw_output)


# ---------------------------
# SAFE PARSER (VERY IMPORTANT)
# ---------------------------
def extract_scores(text):

    try:
        # Remove unwanted text before JSON
        start = text.find("{")
        end = text.rfind("}") + 1
        json_str = text[start:end]

        data = json.loads(json_str)

        scores = data.get("scores", [])

        if len(scores) != 9:
            raise ValueError("Invalid length")

        validated = []
        for s in scores:
            if isinstance(s, int) and s in [0,1,2,3]:
                validated.append(s)
            else:
                validated.append(0)

        print("🟢 PARSED SCORES:", validated)  # ✅ DEBUG

        return validated

    except Exception as e:
        print("❌ PARSE ERROR:", str(e))
        return [0] * 9


# ---------------------------
# KEEP YOUR EXISTING FUNCTION
# ---------------------------
def generate_insight(prompt: str) -> str:
    print("PROMPT TO LLM:", prompt)  # ✅ DEBUG
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a mental health assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()