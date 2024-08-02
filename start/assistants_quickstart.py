import google.generativeai as genai
import shelve
from dotenv import load_dotenv
import os
import time
import logging
import json

# Load environment variables from .env file
load_dotenv()

# Set the Gemini API key for authentication
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.api_key = GEMINI_API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads a file to Gemini and returns the file object."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    file = genai.upload_file(path, mime_type=mime_type)
    return file

def wait_for_files_active(files):
    """Waits for the given files to be processed and active."""
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

# Configure the generation model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="You are Bina, a helpful SDGs chatbot. You can introduce yourself as the user's new BFF minus the drama but this time, you are the user's SDGs Bestie. Use your knowledge base to provide short, detailed but simple and easy-to-understand information about Sustainable Development Goals (SDGs) - its targets and indicators, answer user queries about SDGs, offer project analysis for user's project or project ideas, and potentially generate SDGs-related professional advice on aligning projects with the SDGs. If you don't know the answer, say simply that you cannot help with that question and suggest alternative resources. Be informative, friendly, and engaging.",
)

def generate_response(user_message):
    """Generates a response from the chatbot based on the user message."""
    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [user_message],
        },
      ]
    )
    response = chat_session.send_message(user_message)
    cleaned_response = remove_repetitions(response.text)
    return cleaned_response

def remove_repetitions(text):
    """Removes repetitive or irrelevant parts from the generated text."""
    return text.strip()

def save_conversation(conversation):
    """Saves the conversation data to a file."""
    try:
        with open('conversations.json', 'a') as file:
            json.dump(conversation, file)
            file.write('\n')
    except Exception as e:
        logging.error(f"Error saving conversation: {e}")
