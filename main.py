import requests
import os

TOKEN = os.getenv("8704824778:AAF1ISSK3UAYdvuHki6IriA-LDeVMlrnA6c")
CHAT_ID = os.getenv("447181422")

message = "Тест: всё работает"

url = f"https://api.telegram.org/bot{8704824778:AAF1ISSK3UAYdvuHki6IriA-LDeVMlrnA6c}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message
})
