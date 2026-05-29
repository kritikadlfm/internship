from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
texts=[
    "Hello this is Kritika Dadheech",       
    "I am learning about embedding models",
    "I am learning about GenAI",
    "world is a beautiful place to live in"
]
vector=embeddings.embed_documents(texts)
print(vector)