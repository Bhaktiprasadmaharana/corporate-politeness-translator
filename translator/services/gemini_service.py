import os
from dotenv import load_dotenv
import openai


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
    load_dotenv()  # Ensure .env changes are read immediately without server restarts
    
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
            "IMPORTANT: If the message contains any offensive language, profanity, or rude words, completely remove them or translate the underlying intent into polite, respectful language. Do not retain any insults. "
            "Return ONLY one short sentence. Do NOT explain."
        ),
        "professional": (
            "Rewrite the following message in a polite, professional corporate tone. "
            "IMPORTANT: If the message contains any offensive language, profanity, or rude words, completely remove them or translate the underlying intent into polite, respectful language. Do not retain any insults. "
            "Return ONLY one sentence. No explanations."
        ),
        "corporate": (
            "Rewrite the following message in a very formal corporate tone suitable for senior management. "
            "IMPORTANT: If the message contains any offensive language, profanity, or rude words, completely remove them or translate the underlying intent into polite, respectful language. Do not retain any insults. "
            "Return ONLY one sentence."
        ),
    }

    system_prompt = f"{sender_map.get(sender, sender_map['team_member'])}\n{tone_map.get(level, tone_map['professional'])}"

    try:
        client = openai.OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Message:\n{text}"}
            ]
        )

        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()

        return rule_based_polite(text, level, sender)

    except Exception as e:
        # Fallback when quota is hit, model is unavailable, or API fails
        print(f"Groq API Error: {e}")
        return rule_based_polite(text, level, sender)