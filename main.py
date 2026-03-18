import os
import requests

# Берём токен и чат ID из Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Проверка, что переменные есть
if not TOKEN or not CHAT_ID:
    print("ERROR: BOT_TOKEN or CHAT_ID is missing")
    exit(1)

# Сообщение для отправки
message = "Тест: всё работает"

# Формируем URL для Telegram API
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Отправка сообщения
try:
    resp = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })
    print("Response status code:", resp.status_code)
    print("Response text:", resp.text)
except Exception as e:
    print("ERROR sending message:", e)
    exit(1)
