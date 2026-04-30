"""
LLM Service (Groq Integration)

This module handles:
- Generating mental health insights using LLM
- Generating structured responses (insight + recommendation)

Design Notes:
- Uses Groq API (LLaMA model) for fast inference
- Keeps temperature low for more deterministic responses
- Includes fallback handling for invalid JSON responses
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv


# ---------------------------------------------------------
# Load environment variables (.env)
# ---------------------------------------------------------
# Ensures API keys and configs are available at runtime
load_dotenv()


# ---------------------------------------------------------
# Initialize Groq client
# ---------------------------------------------------------
# Uses API key from environment variable
# Example: GROQ_API_KEY=your_api_key_here
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------------------------------------
# PHQ-9 Questions (for contextual enrichment if needed)
# ---------------------------------------------------------
# Can be used to:
# - Build richer prompts
# - Map answers to questions for explainability
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
    Generate a mental health insight using LLM.

    Args:
        prompt (str): Structured input containing score, severity, and notes

    Returns:
        str: Generated insight text

    Notes:
        - Uses low temperature for stable output
        - Returns plain text (not structured JSON)
    """

    # Debug: Log prompt sent to LLM (can be disabled in production)
    print("PROMPT TO LLM:", prompt)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a mental health assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2  # Lower = more deterministic output
    )

    # Extract and clean response
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# Structured LLM Response (Insight + Recommendation)
# ---------------------------------------------------------
def get_llm_response(prompt: str) -> dict:
    """
    Generate structured response from LLM.

    Expected Output Format:
        {
            "insight": "...",
            "recommendation": "..."
        }

    Args:
        prompt (str): Input prompt for LLM

    Returns:
        dict:
            - insight (str)
            - recommendation (str)

    Fallback:
        - If JSON parsing fails, returns raw output as insight
        - Provides a default safe recommendation
    """

    # Debug logging
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
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3  # Slightly higher for varied recommendations
    )

    raw_output = response.choices[0].message.content.strip()

    # Debug: Raw model output
    print("RAW LLM OUTPUT:", raw_output)

    # ---------------------------------------------------------
    # Safe JSON Parsing
    # ---------------------------------------------------------
    try:
        parsed = json.loads(raw_output)

        return {
            "insight": parsed.get("insight", ""),
            "recommendation": parsed.get("recommendation", "")
        }

    except Exception as e:
        # Log parsing failure for debugging
        print("JSON PARSE ERROR:", e)

        # -----------------------------------------------------
        # Fallback Strategy (Critical for production stability)
        # -----------------------------------------------------
        return {
            "insight": raw_output,  # Use raw text if JSON fails
            "recommendation": (
                "Please consider consulting a professional for further guidance."
            )
        }