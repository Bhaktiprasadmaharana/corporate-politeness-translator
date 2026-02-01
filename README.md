# Corporate Politeness Translator

An AI-powered Django web application that rewrites user messages into polite, professional communication using Google Gemini LLM with persona-based sender roles.

---

## 🚀 Features

- Rewrite casual or blunt messages into professional corporate language
- Select **Politeness Level** (Casual, Professional, Corporate)
- Choose **Sender Role** (Manager, Team Member, HR, Client, Teacher, Friend)
- AI-powered rewriting using **Google Gemini**
- Fallback rule-based rewriting when AI quota is exceeded
- Clean, modern UI built with HTML & CSS
- Secure handling of API keys using environment variables

---

## 🧠 How It Works

1. User enters a message
2. Selects politeness level and sender role
3. The app sends a contextual prompt to Gemini LLM
4. Gemini rewrites the message accordingly
5. If AI is unavailable, a rule-based fallback ensures output is always returned

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **AI Model**: Google Gemini API
- **Deployment-ready**: Gunicorn, Render-compatible setup

---

## ⚙️ Installation & Setup (Local)

### 1. Clone the repository

```bash
git clone https://github.com/Bhaktiprasadmaharana/corporate-politeness-translator.git
cd corporate-politeness-translator
```
