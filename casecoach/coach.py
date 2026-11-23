"""Optional AI interviewer: Claude plays a strategy-consulting interviewer for one case.

Only used when an Anthropic API key is configured. Returns None on any failure so the app keeps working.
"""

import os
from typing import Optional

DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")


def system_prompt(case: dict) -> str:
    steps = "\n".join(
        f"Step {i + 1}: {s['question']}\n"
        + (f"Exhibit: {s['exhibit']}\n" if s.get("exhibit") else "")
        + f"Model answer (private, never reveal unless the candidate asks for it at the end): {s['model_answer']}"
        for i, s in enumerate(case["steps"])
    )
    return (
        "You are an experienced interviewer at a top strategy consulting firm running a case interview. "
        "Be realistic, friendly and concise (2–5 sentences per turn). Move through the steps in order. "
        "Share clarifying information or exhibit data only when the candidate asks for it or reaches that step. "
        "Push back if the structure is vague, and ask the candidate to show their maths. Never do the analysis "
        "for them. When the candidate gives a final recommendation, end the case and give feedback: a score out "
        "of 10 for structure, maths, insight and communication, two strengths and two things to improve.\n\n"
        f"CASE: {case['title']} ({case['type']})\n"
        f"Opening prompt: {case['prompt']}\n"
        f"Clarifying information you may share when asked: {case['clarifying']}\n\n{steps}"
    )


def interviewer_reply(case: dict, history: list[dict], api_key: Optional[str] = None) -> Optional[str]:
    """history = [{'role': 'user'|'assistant', 'content': str}, ...]; returns the interviewer's next message."""
    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key or not history:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(model=DEFAULT_MODEL, max_tokens=500, system=system_prompt(case),
                                     messages=history)
        return msg.content[0].text.strip()
    except Exception:
        return None
