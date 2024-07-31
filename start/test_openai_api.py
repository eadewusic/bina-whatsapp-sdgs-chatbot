import openai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Manually set the environment variable for testing
# os.environ["OPENAI_API_KEY"] = "sk-proj-QR7qOs3R25kphXT1Cf34T3BlbkFJh7TM4QTX5Mc7dHA8Tv3y"

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the API key is set
if not OPENAI_API_KEY:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Test the API by making a simple request with a newer model
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how can I test my OpenAI API key?"}
        ]
    )
    print("API call was successful!")
    print("Response:", response.choices[0].message['content'].strip())
except Exception as e:
    print("An error occurred:", str(e))
