import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from start.assistants_quickstart import save_conversation

# Example conversation
test_conversation = {"user_message": "Hello", "bot_response": "Hi there!"}
save_conversation(test_conversation)
