from django.shortcuts import render
from .services.gemini_service import rewrite_polite

def home(request):
    output_text = ""
    input_text = ""
    level = "professional"
    error = ""
    sender = "team_member"

    if request.method == "POST":
        print("POST request received")

        input_text = request.POST.get("input_text", "")
        level = request.POST.get("level", "professional")
        sender = request.POST.get("sender", "team_member")

        print("Input text:", input_text)
        print("Level:", level)
        print("Sender:", sender)

        if input_text.strip():
            try:
                output_text = rewrite_polite(input_text, level, sender)
                print("Gemini output:", output_text)
            except Exception as e:
                print("Gemini error:", e)
                error = "AI service is temporarily unavailable. Please try again."

    return render(request, "translator/home.html", {
        "output_text": output_text,
        "input_text": input_text,
        "level": level,
        "error": error,
        "sender": sender
    })