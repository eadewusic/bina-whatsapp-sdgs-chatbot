import openai
import shelve
from dotenv import load_dotenv
import os
import time

load_dotenv()
OPENAI_API_KEY = "sk-proj-95HwF9Orx2d4JmGoE7IUT3BlbkFJxluyw4htws7cBdgt62fH"
openai.api_key = OPENAI_API_KEY

# --------------------------------------------------------------
# Upload file of data to OpenAI
# --------------------------------------------------------------
def upload_file(path):
    # Upload a file with an "assistants" purpose
    file = openai.File.create(file=open(path, "rb"), purpose="assistants")
    return file

file = upload_file("../data/sdgs-faq.pdf")

# --------------------------------------------------------------
# Generate response using fine-tuned model or existing model
# --------------------------------------------------------------
def generate_response(message_body, wa_id, name):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        print(f"Creating new thread for {name} with wa_id {wa_id}")
        # For demo purposes, this is replaced with a direct call to OpenAI's API
        thread_id = wa_id  # Use wa_id as a thread_id placeholder

    # Otherwise, retrieve the existing thread
    else:
        print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        # Placeholder for actual thread retrieval if needed
        pass

    # Generate response using OpenAI's Completion API
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Replace with your fine-tuned model ID if applicable
        prompt=message_body,
        max_tokens=150,
    )

    new_message = response.choices[0].text.strip()
    print(f"Generated message: {new_message}")
    return new_message

# --------------------------------------------------------------
# Thread management (placeholder)
# --------------------------------------------------------------
def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)

def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id

# --------------------------------------------------------------
# Test assistant
# --------------------------------------------------------------
new_message = generate_response("What are the Sustainable Development Goals?", "123", "Bob")
new_message = generate_response("How many SDGs do we have?", "456", "Louisa")
new_message = generate_response("Where can I find data on gender equality?", "123", "Bob")
new_message = generate_response("What are the main targets of SDG 7?", "456", "Louisa")
