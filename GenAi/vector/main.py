# from dotenv import load_dotenv
# from openai import OpenAI
# from os

# load_dotenv()
# client = OpenAI()

# response = client.embeddings.create(
#     input="Your text string goes here",
#     model="text-embedding-3-small"
# )

# print(response.data[0].embedding)


# response=client.models.embed_content(
#         model="gemini-embedding-exp-03-07",
#         contents="What is the meaning of life?")

# print(response.embeddings)


from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os

load_dotenv()

apiKey = os.getenv("API_KEY")

client = genai.Client(api_key=apiKey)
messages = []
systemPrompt = """
you are  only able to ans the questions related to mathematics
if user ask any other things then say sorry i m not able to answer
rules:
output must be always in json format 
example:
input:what is sum of 2 and 3
output:{"step":"analyse","content":"analyse the question"}
output:{"step":"validate","content":"the sum of 2 and 3 is 5"}
output:{"step":"result","content":"the sum of 2 and 3 is 5"}

"""
userInput = input("enter the question ")

messages.append(userInput)

while True:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=systemPrompt),
        contents=messages,
    )

    messages.append(response.text)

    print(json.loads(response.text))
    # if res.get("step")!="result":
    #     print(f"🧠🧠🦕🦕:- {res.get('content')}")
    # else:
    #     print(f"🧠🧠🦕🦕:- {res.get('content')}")
    #     break
