''' from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI

from langchain_community.document_loaders import TextLoader

from  langchain_core.prompts import ChatPromptTemplate

data = TextLoader("document loaders/ML_DL_Notes.txt")

docs = data.load()


template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that summarizes the text"),
    ("human", "{data}")
])

prompt = template.format_messages(data = docs[0].page_content)

 
model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

result = model.invoke(prompt)

print(result.content) '''

from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from  langchain_core.prompts import ChatPromptTemplate

data = PyPDFLoader("document loaders/ML_DL_Notes.pdf")

docs = data.load()

template = ChatPromptTemplate.from_messages([
    ("system","You are an AI that is specialist in summarizing text"),
    ("human","{data}")
])

prompt = template.format_messages(data=docs)

model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

result = model.invoke(prompt)

print(result.content)
