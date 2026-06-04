from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import TokenTextSplitter

data = PyPDFLoader("document loaders/ML_DL_Notes.pdf")

docs  = data.load()

#print(docs[1].metadata)

splitter = TokenTextSplitter(
               chunk_size = 100,
               chunk_overlap = 10
)
chunks = splitter.split_documents(docs)

print (chunks[0])
print(len(chunks))

for chunk in chunks:
    print(chunk.page_content)
    print()
    print()

