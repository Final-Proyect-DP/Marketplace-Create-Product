import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Fix typo
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print(f"DATABASE_URI: {Config.SQLALCHEMY_DATABASE_URI}")
print(f"WEBHOOK_URL: {os.getenv('WEBHOOK_URL')}")  # Add this line to verify the webhook URL