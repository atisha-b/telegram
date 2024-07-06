from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
import json
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get the Telegram bot token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

# File to store chat IDs
subscribers_file = 'subscribers.json'

def load_subscribers():

    if os.path.exists(subscribers_file):
        with open(subscribers_file, 'r') as file:
            return json.load(file)
    return []

def save_subscribers(subscribers):
    with open(subscribers_file, 'w') as file:
        json.dump(subscribers, file)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        
        # Handle subscription
        if text.lower() == '/subscribe':
            subscribers = load_subscribers()
            if chat_id not in subscribers:
                subscribers.append(chat_id)
                save_subscribers(subscribers)
                send_telegram_message(chat_id, "You have been subscribed to notifications.")
                logging.info(f'New subscriber added: {chat_id}')
            else:
                send_telegram_message(chat_id, "You are already subscribed.")
                logging.info(f'Subscriber already exists: {chat_id}')
        
        # Respond to the message
        else:
            send_telegram_message(chat_id, f"You said: {text}")
    
    return {"ok": True}

def send_telegram_message(chat_id, text):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    # Log the response for debugging
    logging.info(f'Sent message to {chat_id}: {text}')
    logging.info(f'Response: {response.json()}')

@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    message = data['message']
    
    subscribers = load_subscribers()
    for chat_id in subscribers:
        send_telegram_message(chat_id, message)
    
    return {"ok": True}

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, port=5000)
