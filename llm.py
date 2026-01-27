import json
from datetime import datetime
from groq import Groq
import re
from dotenv import load_dotenv
load_dotenv()
# Initialize Groq client
client = Groq(
    api_key=os.getenv("code")
)

SYSTEM_PROMPT = """
You are an AI support triage assistant for a SaaS company.

Your task:
- Read a customer support ticket
- Identify the underlying issue (not just keywords)
- Classify the issue category
- Determine urgency
- Suggest next actions for a human support agent
- Explain your reasoning clearly and concisely

You MUST return a valid JSON object only.
No markdown. No extra text.
"""

USER_PROMPT_TEMPLATE = """
Analyze the following customer support ticket.

Ticket:
\"\"\"
{ticket_text}
\"\"\"

Return a JSON object with exactly these fields:
- issue (string)
- category (one of: Authentication, Billing, Performance, UI Bug, Integration, Other)
- urgency (one of: Critical, High, Medium, Low)
- suggested_actions (array of strings)
- explanation (string)
- confidence (number between 0 and 1)
"""

def _extract_json(text: str) -> dict:
    """
    Extract the first JSON object found in text.
    Handles cases where the model outputs chain-of-thought.
    """
    # Remove <think> blocks if present
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # Find JSON object
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in model output:\n{text}")

    return json.loads(match.group())

def analyze_ticket(ticket_text: str, model: str = "llama-3.1-8b-instant"):
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(ticket_text=ticket_text)
            }
        ]
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        parsed = _extract_json(raw_output)
    except Exception as e:
        raise ValueError(f"Failed to parse model output:\n{raw_output}") from e

    # Attach system metadata
    parsed["timestamp"] = datetime.now().isoformat(timespec="seconds")
    parsed["ticket_text"] = ticket_text
    parsed["model_used"] = model

    # Safety clamps
    parsed["confidence"] = max(0.0, min(1.0, float(parsed.get("confidence", 0.75))))

    return parsed
