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
# AI-Based PHQ-9 Scoring Function
# ---------------------------------------------------------
def ai_score_answers(answers):
    """
    Converts free-text user answers into PHQ-9 scores (0–3)
    using an LLM (Groq API).

    Args:
        answers (list[str]): List of 9 textual answers

    Returns:
        list[int]: Validated PHQ-9 scores
    """

    # Debug log (replace with logger in production)
    print("INPUT ANSWERS:", answers)

    # ---------------------------------------------------------
    # Prompt Engineering: Provide structured instructions
    # ---------------------------------------------------------
    prompt = f"""
    You are an expert clinical PHQ-9 scoring assistant. 
    A user has provided free-text descriptions of their mental health symptoms over the last 2 weeks. 
    
    The responses do NOT contain standard frequency choices (like "Several days"). Instead, they describe their feelings and habits qualitatively.

    Your task: Assess the severity and implied frequency in each answer and assign a clinical PHQ-9 score (0-3).

    SCORING RUBRIC (Adapted for Free-Text):
    0 = Normal/Absent
    1 = Mild/Occasional
    2 = Moderate/Frequent
    3 = Severe/Constant

    CRITICAL RULES:
    - Use intensity modifiers (e.g., "always", "barely", "normal")
    - If ambiguous → default to 1
    - Q9 (self-harm) must be handled carefully

    QUESTIONS AND USER ANSWERS:
    1. {PHQ9_QUESTIONS[0]} | Answer: "{answers[0]}"
    2. {PHQ9_QUESTIONS[1]} | Answer: "{answers[1]}"
    3. {PHQ9_QUESTIONS[2]} | Answer: "{answers[2]}"
    4. {PHQ9_QUESTIONS[3]} | Answer: "{answers[3]}"
    5. {PHQ9_QUESTIONS[4]} | Answer: "{answers[4]}"
    6. {PHQ9_QUESTIONS[5]} | Answer: "{answers[5]}"
    7. {PHQ9_QUESTIONS[6]} | Answer: "{answers[6]}"
    8. {PHQ9_QUESTIONS[7]} | Answer: "{answers[7]}"
    9. {PHQ9_QUESTIONS[8]} | Answer: "{answers[8]}"

    Return ONLY JSON:
    {{"scores": [s1, s2, s3, s4, s5, s6, s7, s8, s9]}}
    """

    try:
        # ---------------------------------------------------------
        # Call Groq LLM API
        # ---------------------------------------------------------
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You output ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}  # Enforce JSON
        )

        raw_output = response.choices[0].message.content.strip()

        # Debug log
        print("🔴 RAW LLM OUTPUT:", raw_output)

        # ---------------------------------------------------------
        # Parse and validate scores
        # ---------------------------------------------------------
        return extract_scores(raw_output)

    except Exception as e:
        # Fallback in case of API failure
        print("❌ API ERROR:", str(e))
        return [0] * 9


# ---------------------------------------------------------
# SAFE JSON PARSER (CRITICAL FOR RELIABILITY)
# ---------------------------------------------------------
def extract_scores(json_str):
    """
    Validates and extracts PHQ-9 scores from LLM JSON output.

    Ensures:
    - Correct JSON format
    - Exactly 9 scores
    - Values are integers in range [0–3]
    """

    try:
        data = json.loads(json_str)
        scores = data.get("scores", [])

        # Validate structure
        if not isinstance(scores, list) or len(scores) != 9:
            print(f"❌ PARSE ERROR: Length is {len(scores)}, expected 9")
            return [0] * 9

        # Validate values
        validated = []
        for s in scores:
            if isinstance(s, int) and s in [0, 1, 2, 3]:
                validated.append(s)
            else:
                print(f"⚠️ INVALID SCORE FOUND: {s}, defaulting to 0.")
                validated.append(0)

        print("🟢 PARSED SCORES:", validated)
        return validated

    except json.JSONDecodeError as e:
        print("❌ JSON FORMAT ERROR:", str(e))
        return [0] * 9

    except Exception as e:
        print("❌ UNEXPECTED PARSE ERROR:", str(e))
        return [0] * 9


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