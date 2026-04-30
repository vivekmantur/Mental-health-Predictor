"""
Trend Analysis Service

Generates comparative insights between two PHQ-9 assessments.

Responsibilities:
- Compare latest vs previous assessment
- Identify improvement or decline
- Generate contextual insights and recommendations using LLM
- Ensure structured JSON response with fallback handling

Design Notes:
- Uses LLM for natural language reasoning
- Includes robust JSON extraction/parsing logic
- Prevents system failure due to malformed LLM responses
"""

from app.llm.llm_client import get_llm_response
import json
import re


# ---------------------------------------------------------
# Helper: Extract JSON from LLM Text
# ---------------------------------------------------------
def extract_json(text: str):
    """
    Extract JSON object from a text string using regex.

    Args:
        text (str): Raw LLM response

    Returns:
        dict | None:
            - Parsed JSON if found
            - None if extraction fails

    Notes:
        - Useful when LLM wraps JSON with extra text
    """
    try:
        # Extract first JSON-like block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return None


# ---------------------------------------------------------
# Generate Trend Analysis
# ---------------------------------------------------------
def generate_trend_analysis(latest, previous):
    """
    Generate trend analysis between two assessments.

    Args:
        latest (Assessment): Most recent assessment
        previous (Assessment): Previous assessment

    Returns:
        dict:
            {
                "insight": str,
                "recommendation": List[str]
            }

    Workflow:
        1. Build structured prompt
        2. Call LLM
        3. Handle multiple response formats (dict / string / malformed)
        4. Return safe structured output

    Notes:
        - Ensures non-breaking response even if LLM fails
        - Encourages cautious and non-diagnostic language
    """

    # ---------------------------------------------------------
    # Construct Prompt
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Call LLM
    # ---------------------------------------------------------
    response = get_llm_response(prompt)

    # Debug logging (can be removed in production)
    print("RAW LLM OUTPUT:", response)

    # ---------------------------------------------------------
    # Case 1: Already a dictionary (ideal scenario)
    # ---------------------------------------------------------
    if isinstance(response, dict):
        return response

    # ---------------------------------------------------------
    # Case 2: Response is a JSON string
    # ---------------------------------------------------------
    if isinstance(response, str):
        try:
            return json.loads(response)
        except Exception:
            pass

        # -----------------------------------------------------
        # Case 3: Extract JSON from messy string
        # -----------------------------------------------------
        try:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass

    # ---------------------------------------------------------
    # Fallback (Critical for system stability)
    # ---------------------------------------------------------
    return {
        "insight": "Unable to generate insight at the moment.",
        "recommendation": ["Try again later"]
    }