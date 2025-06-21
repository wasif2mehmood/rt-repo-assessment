import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document  # Added for type hinting

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX_PATH = "faiss_index"


def format_docs(docs: list[Document]) -> str:
    """Helper function to format retrieved documents by joining their page_content."""
    page_contents = []
    for doc in docs:
        # The user's debug print can stay if they find it useful
        source_id = doc.metadata.get("id", "N/A")  # Still useful for debug print
        title = doc.metadata.get("title", "N/A")  # Still useful for debug print
        # print("Source ID:", source_id, "Title:", title)  # User's existing debug print

        # doc.page_content already has ID and Title prepended from ingest.py
        page_contents.append(doc.page_content)
    return "\n\n---\n\n".join(page_contents)


def main():
    # Load the vector store
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    try:
        vector_store = FAISS.load_local(
            FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        print("Please make sure you have run ingest.py to create the index.")
        return

    retriever = vector_store.as_retriever()

    # Define the prompt template
    template = """Answer the question based only on the following context.
If the context is empty or doesn't contain the answer, say you don't have enough information.

Context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    # Define the LLM
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

    # Create the RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("RAG Assistant is ready. Type 'exit' to quit.")
    while True:
        user_question = input("You: ")
        if user_question.lower() == "exit":
            break
        if not user_question.strip():
            continue

        try:
            response = rag_chain.invoke(user_question)
            print(f"Assistant: {response}")
        except Exception as e:
            print(f"Error during RAG chain invocation: {e}")


if __name__ == "__main__":
    main()
