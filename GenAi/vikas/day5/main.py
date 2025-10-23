from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="you are girl friend who is flirting with user",
    ),
)

while True:
    query = input("Enter your question: ")
    response = chat.send_message(query)
    print(response.text)
