from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

load_dotenv()
file_path = "../pdf/vikas.pdf"

loader = PyPDFLoader(str(file_path))
docs = loader.load()


text_splite = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splite.split_documents(documents=docs)

embadding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vvector_store=QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="rag",
    embedding=embadding_model
)
