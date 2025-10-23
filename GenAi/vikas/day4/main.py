from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)
system_promt="""you are a maths expert and you only answer the question in json format only if it is math question otherwise say sorry i am not able to answer"""
user_input=input("Enter your question: ")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_promt),
    contents=user_input
)

print(response.text)