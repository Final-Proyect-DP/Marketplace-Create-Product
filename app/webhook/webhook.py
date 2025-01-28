import requests

WEBHOOK_URL = "http://localhost:5003/webhook"  # Webhook URL of the get microservice

def send_webhook(data):
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 200:
        print(f"Error synchronizing data: {response.text}")
