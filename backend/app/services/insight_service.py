from app.llm.llm_client import generate_insight as llm_call

def generate_insight(answers, severity):

    prompt = f"""
You are a mental health assistant.

User responses:
{answers}

Severity: {severity}

Give:
- Emotional summary
- Key struggles

Keep it short, empathetic, human-like.
"""

    return llm_call(prompt)