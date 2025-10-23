# from typing import TypedDict,Annotated
# from langchain.chat_models import init_chat_model

# class State(TypedDict):
#     name: Annotated[str, "The name of the person"]
#     age: Annotated[int, "The age of the person"] 

# llm=init_chat_model(model_provider="openai", model="gpt-4.1")
# structured=llm.with_structured_output(State)

# print(structured.invoke("my name is vikas  and i am 20"))





from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from typing import Optional,Literal


class State(BaseModel):
    name: str = Field(description="The name of the person")
    age: int =Field(description="The age of the person")
    likes: Optional[list[str]] = Field(default=None,description="The likes of the person")
    is_coding: Optional[Literal["yes","no"]] = Field(default=None,description="The coding of the person")

llm=init_chat_model(model_provider="openai", model="gpt-4.1")
structured=llm.with_structured_output(State)

print(structured.invoke("my name is vikas  and i am 20"))


