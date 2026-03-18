import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN or not CHAT_ID:
    print("ERROR: BOT_TOKEN or CHAT_ID is missing")
    exit(1)

if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY is missing")
    exit(1)

# --- Запрос к Groq ---
def ask_groq():
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = """Ты эксперт...  # ← теперь 4 пробела, как и у url

Посмотри сегодняшнюю дату и дай актуальную информацию на этот месяц. Люди активно обсуждают:
- стоимость родов в 2026 году
- сроки оформления документов (паспорт ребёнка за 10 дней, ВНЖ родителям 2–2,5 месяца)
- домашние роды
- Digital Nomad Visa + рождение ребёнка
- гражданство для старших детей и всей семьи
- роль долы (медицинский перевод + психологическая поддержка + защита плана родов)

Дай список из 7 максимально актуальных идей для Reels на следующую неделю.

Формат каждой идеи строго:
🎬 [цепляющий заголовок для видео 15–30 сек]
💡 [1 короткая строка — почему это ОЧЕНЬ актуально именно сейчас в марте 2026]

Пиши живо, эмоционально, по-дружески, как советуешь подруге-блогерше. Используй реальные боли и тренды русскоязычного комьюнити (Флорианополис и вся Бразилия)."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.3-70b-versatile",  # или "llama-3.1-8b-instant" для ещё большей скорости
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_completion_tokens": 800,  # лимит токенов на ответ
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()  # поднимает исключение при 4xx/5xx
        data = response.json()
        
        if "choices" not in data or not data["choices"]:
            print("Groq error: нет choices в ответе", data)
            exit(1)
        
        return data["choices"][0]["message"]["content"]
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Groq HTTP error: {http_err}")
        print("Ответ сервера:", response.text)
        exit(1)
    except Exception as e:
        print("Groq request error:", e)
        exit(1)

# --- Получаем идеи ---
print("Запрашиваю идеи у Groq...")
ideas = ask_groq()
print("Ответ получен")

# --- Формируем сообщение ---
message = "🎬 *Идеи для Reels на этой неделе*\n_(оформление документов в России)_\n\n" + ideas

# --- Отправка в Telegram ---
tg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

try:
    resp = requests.post(tg_url, data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })
    print("Telegram response status code:", resp.status_code)
    print("Telegram response text:", resp.text)
except Exception as e:
    print("ERROR sending message to Telegram:", e)
    exit(1)
