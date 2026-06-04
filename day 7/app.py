from dotenv import load_dotenv
load_dotenv()

import os
import tempfile
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF RAG Chatbot")
st.write("Upload a PDF and ask questions about it.")

# --------------------------
# Upload PDF
# --------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:

    if "vectorstore" not in st.session_state:

        with st.spinner("Processing PDF..."):

            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp_file:

                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name

            # Load PDF
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            # Split documents
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(docs)

            # Embeddings
            embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Create Chroma DB
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory="chroma-db"
            )

            st.session_state.vectorstore = vectorstore

        st.success("PDF processed successfully!")

# --------------------------
# Chat Section
# --------------------------

if "vectorstore" in st.session_state:

    query = st.text_input(
        "Ask a question from the PDF"
    )

    if st.button("Get Answer") and query:

        retriever = st.session_state.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 4,
                "fetch_k": 10,
                "lambda_mult": 0.5
            }
        )

        docs = retriever.invoke(query)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a helpful AI assistant.

                    Use ONLY the provided context
                    to answer the question.

                    If the answer is not present
                    in the context, say:

                    "I could not find the answer
                    in the document."
                    """
                ),
                (
                    "human",
                    """
                    Context:
                    {context}

                    Question:
                    {question}
                    """
                )
            ]
        )

        llm = ChatMistralAI(
            model="mistral-small-2506"
        )

        final_prompt = prompt.format_messages(
            context=context,
            question=query
        )

        with st.spinner("Generating answer..."):
            response = llm.invoke(final_prompt)

        st.subheader("Answer")
        st.write(response.content)