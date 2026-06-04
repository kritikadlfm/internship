#load pdf 
#split into chunks 
#create the embeddings 
#stroe in database 


from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma 

data = PyPDFLoader("document loaders/deep_learning_o'reilly.pdf")

docs =  data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents = chunks,
    embedding = embedding_model,
    persist_directory = "chroma-db"
)



