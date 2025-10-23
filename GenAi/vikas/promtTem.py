from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

llm = init_chat_model( model_provider="openai", model="gpt-4.1")
tem=PromptTemplate.from_template(template="tell me about {topic} in way{fun}",validate_template=True)
format_tem=tem.format(topic="python", fun="essay")

print(llm.invoke(format_tem).content)