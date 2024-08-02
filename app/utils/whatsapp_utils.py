import logging
from flask import current_app, jsonify
import json
import requests
import re

from start.assistants_quickstart import generate_response

def log_http_response(response):
    """Logs details of HTTP responses."""
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

def get_text_message_input(recipient, text):
    """Formats the message payload for sending via WhatsApp."""
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
    """Sends a message to the WhatsApp API."""
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )
        response.raise_for_status()
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except requests.RequestException as e:
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        log_http_response(response)
        return response

def process_text_for_whatsapp(text):
    """Cleans and formats the text for WhatsApp messages."""
    # Remove text enclosed in 【】 brackets
    pattern = r"\【.*?\】"
    text = re.sub(pattern, "", text).strip()
    # Convert **bold** text to *italic* style
    pattern = r"\*\*(.*?)\*\*"
    replacement = r"*\1*"
    whatsapp_style_text = re.sub(pattern, replacement, text)
    return whatsapp_style_text

def process_whatsapp_message(body):
    """Processes incoming WhatsApp messages and generates a response."""
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # Generate a response from the chatbot
    response = generate_response(message_body)
    # Format response for WhatsApp
    response = process_text_for_whatsapp(response)

    # Send response back to the user
    data = get_text_message_input(wa_id, response)
    send_message(data)

def is_valid_whatsapp_message(body):
    """Checks if the incoming request contains a valid WhatsApp message."""
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
