from flask import Flask
from app.config import load_configurations, configure_logging
from .views import webhook_blueprint
import logging

def create_app():
    app = Flask(__name__)

    # Load configurations and logging settings
    load_configurations(app)
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Loaded VERIFY_TOKEN in __init__: {app.config.get('VERIFY_TOKEN')}")

    # Import and register blueprints, if any
    app.register_blueprint(webhook_blueprint)

    return app
