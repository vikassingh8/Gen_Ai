from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver


class State(TypedDict):
    message: Annotated[list, add_messages]


llm = init_chat_model(model_provider="openai", model="gpt-4.1")


def chat_bot(state: State):
    response = llm.invoke(state["message"])
    return {"message": [response]}


graph_builder = StateGraph(State)
graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

# graph = graph_builder.compile()


def checkpoint_saver(checkpointer):
    graph_with_checkpoint = graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpoint


def main():
    use_input = input("Enter your query: ")
    db_url = "mongodb://localhost:27017"

    config = {"configurable": {"thread_id": 1}}
    with MongoDBSaver.from_conn_string(db_url) as checkpointer:
        graph_with_mongo = checkpoint_saver(checkpointer)
        

        _state = {"message": [{"role": "user", "content": use_input}]}
        graph_result = graph_with_mongo.invoke(_state, config=config)
    print(graph_result)


main()
