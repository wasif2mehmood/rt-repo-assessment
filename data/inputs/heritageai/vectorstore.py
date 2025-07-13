import os
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import SVMRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document  # Import Document class
from dotenv import load_dotenv

# To avoid warnings in non-Streamlit contexts
try:
    import streamlit as st
    streamlit_available = True
except ImportError:
    streamlit_available = False

load_dotenv()

project = os.getenv("PROJECT_NAME")  
embeddings_model = os.getenv("EMBEDDINGS")
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)

def load_db(reset=False):
    chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")  
    data_path = os.getenv("DATA_PATH")
    
    # Check if DATA_PATH is set
    if data_path is None:
        error_msg = f"Error: DATA_PATH environment variable is not set. Please define it in the .env file to load {project} data."
        if streamlit_available:
            st.error(error_msg)
        raise ValueError(error_msg)
    
    # Verify DATA_PATH exists
    if not os.path.exists(data_path):
        error_msg = f"Error: Directory {data_path} does not exist. Ensure it contains {project} data."
        if streamlit_available:
            st.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    os.makedirs(os.path.dirname(chroma_db_path), exist_ok=True)
    docs = []
    if not reset and os.path.exists(chroma_db_path):
        if streamlit_available:
            st.write(f"Loading existing Database...")
        try:
            vector_store = Chroma(persist_directory=chroma_db_path, embedding_function=embeddings)
            if streamlit_available:
                st.write(f"Database loaded successfully.")
            # Fetch documents and metadata from Chroma
            chroma_data = vector_store.get(include=["documents", "metadatas"])
            raw_docs = chroma_data["documents"]
            metadatas = chroma_data["metadatas"]
            if not raw_docs:
                if streamlit_available:
                    st.warning(f"No documents found in {chroma_db_path}. Rebuilding database...")
                docs = []
            else:
                # Convert raw strings to Document objects
                docs = [
                    Document(page_content=doc, metadata=meta or {})
                    for doc, meta in zip(raw_docs, metadatas or [{}] * len(raw_docs))
                ]
        except Exception as e:
            error_msg = f"Error loading Database: {e}"
            if streamlit_available:
                st.error(error_msg)
            else:
                print(error_msg)
            docs = []
    else:
        if streamlit_available:
            st.write(f"Setting up the Database. Please wait...")
        else:
            print(f"Setting up the Database. Please wait...")
        try:
            loader = DirectoryLoader(data_path, glob="**/*.pdf", show_progress=True, loader_cls=PyMuPDFLoader)
            docs = loader.load()
            if not docs:
                error_msg = f"No PDF files found in {data_path} for {project}."
                if streamlit_available:
                    st.error(error_msg)
                else:
                    print(error_msg)
                raise ValueError(error_msg)
            vector_store = Chroma.from_documents(docs, embeddings, persist_directory=chroma_db_path)
            if streamlit_available:
                st.write(f"Database created and saved successfully.")
            else:
                print(f"Database created and saved successfully.")
        except Exception as e:
            error_msg = f"Error creating Database: {e}"
            if streamlit_available:
                st.error(error_msg)
            else:
                print(error_msg)
            docs = []
    
    similarity_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    svm_retriever = SVMRetriever.from_documents(docs, embeddings)
    ensemble_retriever = EnsembleRetriever(retrievers=[similarity_retriever, svm_retriever], weights=[0.7, 0.3])
    return vector_store, ensemble_retriever