import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("ERROR: BOT_TOKEN or CHAT_ID is missing")
    exit(1)

message = "Тест: всё работает"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

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
