from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv

dotenv.load_dotenv()
parser = StrOutputParser()

llm = init_chat_model(model_provider="openai", model="gpt-4.1")

tem = PromptTemplate.from_template(
    template="Tell me about {topic} in an {fun} way",
    validate_template=True
)

chain = tem | llm | parser
# res = chain.invoke({"topic": "python", "fun": "essay"})
chain.get_graph().print_ascii()


