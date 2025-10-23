
from langchain.chat_models import init_chat_model
import dotenv

dotenv.load_dotenv()

llm = init_chat_model(
    model_provider="openai",
    model="gpt-4.1"
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("Chat started! (type 'exit' to quit)\n")

while True:
   
    user_input = input("You: ")
    
    messages.append({"role": "user", "content": user_input})

    response = llm.invoke(messages)

    print("Assistant:", response.content)

    messages.append({"role": "assistant", "content": response.content})
