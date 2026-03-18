import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

message = "Тест: всё работает"

url = f"https://api.telegram.org/bot{8704824778:AAF1ISSK3UAYdvuHki6IriA-LDeVMlrnA6c}/sendMessage"

requests.post(url, data={
    "chat_id": 447181422,
    "text": все работает
})
