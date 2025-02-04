import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Webhook URL from environment variable

def send_webhook(data):
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 200:
        print(f"Error synchronizing data: {response.text}")
