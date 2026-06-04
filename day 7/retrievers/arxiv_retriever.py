from langchain_community.retrievers import ArxivRetriever

retriever = ArxivRetriever(
    load_max_docs = 2,
    load_all_available_meta=True
)

docs = retriever.invoke("large language model")

for i, doc in enumerate(docs):
    print(f"\n Result{i+1}")
    print("Title:", doc.metadata.get("Title"))
    print("Authors:", doc.metadata.get("Authors"))
    print("Abstract:", doc.page_content)
    