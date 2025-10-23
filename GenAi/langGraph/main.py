from typing_extensions import TypedDict
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from typing import Literal

client = OpenAI()


# ✅ Pydantic model for JSON output
class MessageType(BaseModel):
    is_coding: bool


# LangGraph State
class State(TypedDict):
    query: str
    is_coding: bool
    accuracy: str
    message: str | None


def chat_bot(state: State):
    system_prompt = """You are an AI assistant. Your job is to detect if the user's query is
    related to coding question or not.
    Return strictly JSON like:
    {
      "is_coding": true
    }"""

    response = client.beta.chat.completions.parse(
        model="gpt-4o",  # ✅ must support response_format='json'
        response_format=MessageType,  # ✅ must be Pydantic model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": state["query"]},
        ],
    )

    result = response.choices[0].message.parsed.is_coding
    print("Parsed:", result)

    state["is_coding"] = result
    return state


def router(state: State) -> Literal["coding", "non_coding"]:
    is_coding = state["is_coding"]
    if is_coding:
        return "coding"
    else:
        return "non_coding"


def non_coding(state: State):
    query = state["query"]
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": query},
        ],
    )
    result = response.choices[0].message.content
    state["message"] = result
    return state


def coding(state: State):
    system_prompt = """you are coding expert agent ai"""

    query = state["query"]
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
    )
    result = response.choices[0].message.content
    state["message"] = result
    return state


def accuracy(state: State):
    query = state["query"]
    message = state["message"]
    system_prompt = f"""you are expert ai who can give accuracy of coding question in percentage
    User Query: {query}
        Code: {message}
"""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
    )
    result = response.choices[0].message.content
    state["accuracy"] = result
 
    return state


# LangGraph
graph_builder = StateGraph(State)
graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("coding", coding)
graph_builder.add_node("non_coding", non_coding)
graph_builder.add_node("accuracy_cheack", accuracy)
graph_builder.add_node("router", router)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_conditional_edges("chat_bot", router)
graph_builder.add_edge("non_coding", END)
graph_builder.add_edge("coding", "accuracy_cheack")
graph_builder.add_edge("accuracy_cheack", END)

graph = graph_builder.compile()


# Main
def main():
    use_input = input("Enter your query: ")
    _state = {"query": use_input, "message": None, "is_coding": False, "accuracy": None}
    graph_result = graph.invoke(_state)
    print(graph_result)
    # for event in graph.stream(_state):
    #     print("Event", event)

main()
