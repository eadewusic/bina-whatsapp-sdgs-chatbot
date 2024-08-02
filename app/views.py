import logging
import json
from flask import Blueprint, request, jsonify, current_app
from .decorators.security import signature_required
from .utils.whatsapp_utils import process_whatsapp_message, is_valid_whatsapp_message

webhook_blueprint = Blueprint("webhook", __name__)

def handle_message():
    """Handles incoming WhatsApp messages and processes them."""
    body = request.get_json()
    logging.info(f"Received webhook body: {body}")

    # Check for status updates
    if body.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("statuses"):
        logging.info("Received a WhatsApp status update.")
        return jsonify({"status": "ok"}), 200

    try:
        if is_valid_whatsapp_message(body):
            process_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            logging.warning("Not a valid WhatsApp message")
            return jsonify({"status": "error", "message": "Not a WhatsApp API event"}), 404
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), 400
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

def verify():
    """Verifies the webhook setup with WhatsApp API."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    expected_token = current_app.config.get('VERIFY_TOKEN')
    logging.info(f"Verification attempt - Mode: {mode}, Token: {token}, Challenge: {challenge}")
    logging.info(f"Expected token: '{expected_token}'")

    if mode and token:
        if mode == "subscribe" and token == expected_token:
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            logging.error(f"VERIFICATION_FAILED - Expected token: '{expected_token}', Provided token: '{token}'")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        logging.error("MISSING_PARAMETER - Mode or token not provided")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_get():
    """Handles GET requests to verify the webhook."""
    logging.info(f"Received GET request: {request.args}")
    return verify()

@webhook_blueprint.route("/webhook", methods=["POST"])
@signature_required
def webhook_post():
    """Handles POST requests for incoming messages."""
    logging.info(f"Received POST request: {request.get_json()}")
    return handle_message()

@webhook_blueprint.errorhandler(Exception)
def handle_exception(e):
    """Handles any unhandled exceptions."""
    logging.error(f"Unhandled exception: {str(e)}")
    return jsonify({"status": "error", "message": "Internal server error"}), 500

@webhook_blueprint.route("/socketcluster/", methods=["GET"])
def socketcluster():
    """Handles GET requests to the SocketCluster endpoint."""
    return jsonify({"status": "success", "message": "SocketCluster Endpoint"}), 200
