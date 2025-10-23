from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
import dotenv
dotenv.load_dotenv()


llm=init_chat_model(model_provider="openai", model="gpt-4.1")

pa=StrOutputParser()

res=llm.invoke("hello")
print(pa.parse(res))