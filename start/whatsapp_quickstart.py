import json
from dotenv import load_dotenv #to load .env file
import os
import requests
import aiohttp
import asyncio


# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


# Send a template WhatsApp message

def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response


# Call the function
response = send_whatsapp_message()
print(response.status_code)
print(response.json())


# Send a custom text WhatsApp message
# NOTE: Make sure you reply to the "Hello world" message from bot on WhatsApp!


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response body: {err.response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


def send_test_messages():
    # Send a template message
    response = send_whatsapp_message()
    print(response.status_code)
    print(response.json())


    # Send a custom text message
    data = get_text_message_input(
        recipient=RECIPIENT_WAID, text="Hello, this is a test message."
    )
    response = send_message(data)


if __name__ == "__main__":
    send_test_messages()
