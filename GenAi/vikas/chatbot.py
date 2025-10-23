
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

message=[
    SystemMessage(content="You are a helpful assistant.")]
while True:
    query=input("Enter your query: ")
    message.append(HumanMessage(content=query))
    llm = init_chat_model(model_provider="openai", model="gpt-4.1")
    response=llm.invoke(query)
    message.append(AIMessage(content=response.content))
    print(response.content)


