import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Telegram bot token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = 'https://huge-ravens-care.loca.lt/webhook'

# Set the webhook
response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}')
print(response.json())
