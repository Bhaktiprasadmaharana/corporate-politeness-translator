from google import genai
import os
from google.genai.errors import ClientError


def rule_based_polite(text, level, sender):
    text = text.strip()

    if not text:
        return "Could you please clarify your request?"

    sender_prefix = {
        "manager": "Please",
        "team_member": "Could you please",
        "hr": "Kindly",
        "client": "We would appreciate if you could",
        "teacher": "Please make sure to",
        "friend": "Hey, can you",
    }.get(sender, "Please")

    if level == "casual":
        return f"Hey, could you {text.lower()}?"

    if level == "corporate":
        return f"{sender_prefix} {text.lower()} at your earliest convenience."

    # professional (default)
    return f"{sender_prefix} {text.lower()}."


def rewrite_polite(text, level, sender):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    sender_map = {
    "manager": "The message is being sent by a manager to a team member.",
    "team_member": "The message is being sent by a team member to a colleague.",
    "hr": "The message is being sent by an HR representative.",
    "client": "The message is being sent by a client to an organization.",
    "teacher": "The message is being sent by a teacher to a student.",
    "friend": "The message is being sent by a friend in an informal but polite manner.",
}

    tone_map = {
        "casual": (
            "Rewrite the following message in a friendly, casual tone. "
            "Return ONLY one short sentence. Do NOT explain."
        ),
        "professional": (
            "Rewrite the following message in a polite, professional corporate tone. "
            "Return ONLY one sentence. No explanations."
        ),
        "corporate": (
            "Rewrite the following message in a very formal corporate tone suitable for senior management. "
            "Return ONLY one sentence."
        ),
    }

    prompt = f"""{sender_map.get(sender, sender_map['team_member'])}
{tone_map.get(level, tone_map['professional'])}

Message:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return rule_based_polite(text, level, sender)

    except ClientError:
        # Fallback when quota is hit or API fails
        return rule_based_polite(text, level, sender)