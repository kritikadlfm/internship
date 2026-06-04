from langchain_community.document_loaders import WebBaseLoader

url = "https://www.apple.com/in-edu/shop/buy-mac?afid=p240%7Cgo~cmp-11182149775~adg-181263916687~ad-809340435031_kwd-335670223~dev-c~ext-~prd-~mca-~nt-search&cid=aos-in-kwgo-txt-mac-mac--"

data = WebBaseLoader(url)

docs = data.load()

print(len(docs))

print(docs[0].page_content)