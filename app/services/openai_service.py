import openai
import shelve
from dotenv import load_dotenv
import os
import time
import logging

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key and assistant ID from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

def upload_file(path):
    # Upload a file with an "assistants" purpose
    response = openai.File.create(
        file=open(path, "rb"), purpose="assistants"
    )
    return response

def create_assistant(file_id):
    """
    You currently cannot set the temperature for Assistant via the API.
    """
    response = openai.Assistant.create(
        name="Bina AI - Your SDGs Bestie",
        instructions="You are Bina, a helpful SDG chatbot. Use your knowledge base to provide detailed but simple and easy-to-understand information about Sustainable Development Goals (SDGs) - its targets and indicators, answer user queries about SDGs, offer project analysis for user's project or project ideas, and potentially generate SDGs-related professional advice on aligning projects with the SDGs. If you don't know the answer, say simply that you cannot help with that question and suggest alternative resources. Be informative, friendly, and engaging.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file_id],
    )
    return response

def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)

def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id

def run_assistant(thread_id, name):
    # Retrieve the Assistant
    response = openai.Assistant.retrieve(OPENAI_ASSISTANT_ID)

    # Run the assistant
    run_response = openai.Thread.run(
        thread_id=thread_id,
        assistant_id=OPENAI_ASSISTANT_ID
    )

    # Wait for completion
    while run_response['status'] != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run_response = openai.Thread.retrieve(thread_id=thread_id, run_id=run_response['id'])

    # Retrieve the Messages
    messages = openai.Thread.messages.list(thread_id=thread_id)
    new_message = messages['data'][0]['content']['text']['value']
    logging.info(f"Generated message: {new_message}")
    return new_message

def generate_response(message_body, wa_id, name):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        logging.info(f"Creating new thread for {name} with wa_id {wa_id}")
        response = openai.Thread.create()
        thread_id = response['id']
        store_thread(wa_id, thread_id)

    # Otherwise, retrieve the existing thread
    else:
        logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")

    # Add message to thread
    message = openai.Thread.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread_id, name)

    return new_message
