from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Initialize embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="rag",
    embedding=embedding_model
)

# User query
# query = input("Enter your question: ")
def chat(query):
    
    # Retrieve similar documents
    results = vector_db.similarity_search(query=query)

    # Create context from results
    context = [
        f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page')}\nLocation: {result.metadata.get('source')}"
        for result in results
    ]

    # Join context into a string
    joined_context = "\n\n".join(context)

    # Define prompt for LLM
    system_prompt = f"""
    You are a helpful AI assistant who answers user queries based only on the provided context.

    You should only respond using the following context and guide the user to the correct page number if applicable.

    Context:
    {joined_context}

    User Query:
    {query}
    """

    # Print to verify
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]
    )

    return (response.choices[0].message.content)
