from langchain_community.vectorstores import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

from langchain_core.documents import Document 

load_dotenv()

docs = [
    Document(
        page_content="Python is widely used in Artificial Intelligence, Machine Learning, Data Science, and Web Development.",
        metadata={"source": "python_guide"}
    ),

    Document(
        page_content="Machine Learning is a subset of Artificial Intelligence that enables systems to learn patterns from data without being explicitly programmed.",
        metadata={"source": "ml_guide"}
    ),

    Document(
        page_content="Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers to solve complex tasks such as image recognition and natural language processing.",
        metadata={"source": "dl_guide"}
    ),

    Document(
        page_content="Retrieval-Augmented Generation (RAG) combines information retrieval with Large Language Models to provide accurate and context-aware responses.",
        metadata={"source": "rag_guide"}
    )
]

embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents = docs,
    embedding = embedding_model,
    persist_directory = "chroma-db"
)

result = vectorstore.similarity_search("what is RAG and DL", k=2)
for r in result:
    print(r.page_content)
    print(r.metadata)

retriver = vectorstore.as_retriever()

docs = retriver.invoke("explain deep learning")

for d in docs:
    print(d.page_content)
    print(d.metadata)
