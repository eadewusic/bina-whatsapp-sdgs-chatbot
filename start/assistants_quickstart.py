import google.generativeai as genai
import shelve
from dotenv import load_dotenv
import os
import time
import logging

print("Files in the current directory:", os.listdir())
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the PDF file
pdf_path = os.path.join(current_dir, '..', 'data', 'sdgs-faq.pdf')
print("PDF path:", pdf_path)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables/ Set the GEMINI API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.api_key = GEMINI_API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
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
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You are Bina, a helpful SDG chatbot. You can introduce yourself as the user's new BFF minus the drama but this time, you are the user's SDGs Bestie. Use your knowledge base to provide short, detailed but simple and easy-to-understand information about Sustainable Development Goals (SDGs) - its targets and indicators, answer user queries about SDGs, offer project analysis for user's project or project ideas, and potentially generate SDGs-related professional advice on aligning projects with the SDGs. If you don't know the answer, say simply that you cannot help with that question and suggest alternative resources. Be informative, friendly, and engaging.",
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini(pdf_path, mime_type="application/pdf"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Hello",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Hey there! 👋 I'm Bina, your new SDGs Bestie! 💖 No drama, just goals and vibes - sustainable ones! 🌎. Think of me as your guide to making the world a better place by taking you through the journey of understanding the Sustainable Development Goals. What's got you interested in the SDGs today? 😊",
      ],
    },
  ]
)

def remove_repetitions(text):
    lines = text.split('\n')
    return '\n'.join(dict.fromkeys(lines))

response = chat_session.send_message("What are the main targets of SDG 7?")

cleaned_response = remove_repetitions(response.text)
print(cleaned_response)
