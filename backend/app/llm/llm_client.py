import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# The exact PHQ-9 questions provide better context for the LLM
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

def ai_score_answers(answers):
    print("INPUT ANSWERS:", answers)  # ✅ DEBUG
    
    prompt = f"""
    You are an expert clinical PHQ-9 scoring assistant. 
    A user has provided free-text descriptions of their mental health symptoms over the last 2 weeks. 
    
    The responses do NOT contain standard frequency choices (like "Several days"). Instead, they describe their feelings and habits qualitatively.

    Your task: Assess the severity and implied frequency in each answer and assign a clinical PHQ-9 score (0-3).

    SCORING RUBRIC (Adapted for Free-Text):
    0 = Normal/Absent: No signs of the symptom, healthy baseline. 
        (e.g., "Eating habits are normal", "I sleep well", "Energy levels are good")
    1 = Mild/Occasional: Minor disruption, happening sometimes, manageable. 
        (e.g., "I feel a bit tired sometimes", "I occasionally skip meals")
    2 = Moderate/Frequent: Noticeable disruption, happening often, struggling. 
        (e.g., "I have trouble sleeping most nights", "I often feel hopeless")
    3 = Severe/Constant: Extreme wording, happening constantly, debilitating. 
        (e.g., "I am ALWAYS exhausted", "COMPLETELY lost my appetite", "I stay in bed all day")

    CRITICAL RULES:
    - Look for intensity modifiers (e.g., "always", "completely", "barely", "normal") to determine the score.
    - If the user's answer is ambiguous or mildly negative, default to 1.
    - Q9 is extremely critical: Any hint of self-harm, wishing to not exist, or suicidal ideation must be scored at least 1. "Normal" thoughts about death score 0 only if strictly philosophical and completely non-threatening.

    --- EXAMPLES FROM REAL DATA ---
    Q: "Trouble falling or staying asleep, or sleeping too much"
    Answer: "I barely sleep at night, and when I do, nightmares wake me up." -> Score: 3 (Severe)
    
    Q: "Poor appetite or overeating"
    Answer: "Eating habits are normal, no major appetite changes." -> Score: 0 (Normal)
    
    Q: "Feeling tired or having little energy"
    Answer: "Energy levels are good, I can do my daily tasks easily." -> Score: 0 (Normal)
    
    Q: "Feeling tired or having little energy"
    Answer: "I am always exhausted, even talking feels like too much effort." -> Score: 3 (Severe)
    ----------------

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

    You MUST return ONLY a valid JSON object. 
    Format required: {{"scores": [score1, score2, score3, score4, score5, score6, score7, score8, score9]}}
    """

    try:
        response = client.chat.completions.create(
            # Switched to the best Groq reasoning model
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You output ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            # Enforce strict JSON output at the API level
            response_format={"type": "json_object"} 
        )

        raw_output = response.choices[0].message.content.strip()

        print("🔴 RAW LLM OUTPUT:", raw_output)   # ✅ DEBUG

        return extract_scores(raw_output)
    
    except Exception as e:
        print("❌ API ERROR:", str(e))
        return [0] * 9


# ---------------------------
# SAFE PARSER (VERY IMPORTANT)
# ---------------------------
def extract_scores(json_str):
    """
    Since we enforce JSON at the API level, we only need to validate 
    the structure and values, rather than relying on string searches.
    """
    try:
        data = json.loads(json_str)
        scores = data.get("scores", [])

        if not isinstance(scores, list) or len(scores) != 9:
            print(f"❌ PARSE ERROR: Length is {len(scores)}, expected 9")
            return [0] * 9

        validated = []
        for s in scores:
            if isinstance(s, int) and s in [0, 1, 2, 3]:
                validated.append(s)
            else:
                print(f"⚠️ INVALID SCORE FOUND: {s}, defaulting to 0.")
                validated.append(0)

        print("🟢 PARSED SCORES:", validated)  # ✅ DEBUG
        return validated

    except json.JSONDecodeError as e:
        print("❌ JSON FORMAT ERROR:", str(e))
        return [0] * 9
    except Exception as e:
        print("❌ UNEXPECTED PARSE ERROR:", str(e))
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
