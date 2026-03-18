import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN or not CHAT_ID:
    print("ERROR: BOT_TOKEN or CHAT_ID is missing")
    exit(1)

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY is missing")
    exit(1)

# --- Запрос к Gemini ---
def ask_gemini():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = """Ты эксперт по контенту для социальных сетей в России.

Дай список из 7 актуальных идей для Reels на тему оформления документов в России (МФЦ, паспорта, пропись, СНИЛС, ИНН, нотариус, недвижимость и т.д.).

Формат каждой идеи:
🎬 [цепляющий заголовок для видео]
💡 [1 строка — почему это актуально сейчас]

Пиши живо, как советуешь другу-блогеру."""

    body = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, json=body)
    data = response.json()
    
    if "candidates" not in data:
        print("Gemini error:", data)
        exit(1)
    
    return data["candidates"][0]["content"]["parts"][0]["text"]

# --- Получаем идеи ---
print("Запрашиваю идеи у Gemini...")
ideas = ask_gemini()
print("Ответ получен")

# --- Формируем сообщение ---
message = "🎬 *Идеи для Reels на этой неделе*\n_(оформление документов в России)_\n\n" + ideas

# --- Отправка в Telegram ---
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

try:
    resp = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })
    print("Response status code:", resp.status_code)
    print("Response text:", resp.text)
except Exception as e:
    print("ERROR sending message:", e)
    exit(1)
