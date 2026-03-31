from app.llm.llm_client import generate_insight as llm_call

def generate_recommendation(answers, severity):

    prompt = f"""
You are a mental health assistant.

User condition: {severity}

Provide:
- Practical suggestions
- Daily improvements
- When to seek help

Keep it simple and supportive.
"""

    return llm_call(prompt)