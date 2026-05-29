from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
load_dotenv()
embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=64
)
vector = embeddings.embed_query("You are going to learn about embedding models to learn GenAI")
print(vector)
texts=[
    "Hello this is Kritika Dadheech",
    "I am learning about embedding models",
    "I am learning about GenAI",
    "world is a beautiful place to live in"
]
docs=embeddings.embed_documents(texts)
print(docs)