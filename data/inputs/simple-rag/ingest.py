import os
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    JSONLoader,
)  # Removed TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define file paths
# txt_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Publication Evaluation Criteria Reference Guide.txt"))
# pdf_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Publication Evaluation Criteria Reference Guide.pdf"))
json_file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "project_1_publications.json")
)


def extract_publication_metadata(record: dict, metadata: dict) -> dict:
    """Extracts specific metadata fields from a JSON record."""
    metadata["id"] = record.get("id")
    metadata["title"] = record.get("title")
    metadata["username"] = record.get("username")
    metadata["license"] = record.get("license")
    # The default metadata (like 'source' and 'seq_num') is already in the metadata dict
    return metadata


# Load documents
# txt_loader = TextLoader(txt_file_path)
# pdf_loader = PyMuPDFLoader(pdf_file_path)
# Assumes project_1_publications.json is an array of objects,
# and each object has a "publication_description" field containing the main content.
# Other fields in the JSON objects will be added to metadata.
json_loader = JSONLoader(
    json_file_path,
    jq_schema=".[]",
    content_key="publication_description",
    text_content=True,
    metadata_func=extract_publication_metadata,  # Add the metadata function here
)

# txt_documents = txt_loader.load()
# pdf_documents = pdf_loader.load()
try:
    json_documents = json_loader.load()
    if json_documents:  # Check if list is not empty
        print("--- Debug: Metadata of the first document loaded by JSONLoader ---")
        print(json_documents[0].metadata)
        print(f"--- Debug: Page content of the first document (first 200 chars) ---")
        print(f"{json_documents[0].page_content[:200]}...")
        print("--- End Debug ---")

        # Prepend ID and Title to page_content for better retrieval
        for doc in json_documents:
            doc_id = doc.metadata.get("id", "N/A")
            doc_title = doc.metadata.get("title", "N/A")
            # Make the prepended string more sentence-like
            prepend_text = f'This document is about a publication. The Publication ID is {doc_id}. The Title is "{doc_title}". The main content follows:\n\n'
            doc.page_content = prepend_text + doc.page_content

        print(
            "--- Debug: Page content of the first document after prepending metadata (first 400 chars) ---"
        )
        print(f"{json_documents[0].page_content[:400]}...")
        print("--- End Debug ---")

except ValueError as e:
    print(f"Error loading JSON file: {e}")
    print(
        "Please ensure 'project_1_publications.json' is correctly formatted and contains the 'publication_description' key."
    )
    json_documents = []  # Proceed with an empty list if JSON is problematic

# all_documents = txt_documents + pdf_documents + json_documents
all_documents = json_documents  # Use only JSON documents

# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(all_documents)

if not docs:
    print("No documents were loaded. FAISS index will not be created.")
else:
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_documents(docs, embeddings)

    # Save vector store
    vector_store.save_local("faiss_index")
    print(
        "Vector store created and saved successfully based on project_1_publications.json."
    )
