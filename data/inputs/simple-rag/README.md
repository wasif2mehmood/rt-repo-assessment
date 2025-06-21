# RAG Assistant for Custom Knowledge Base

## Project Description

This project implements a Retrieval Augmented Generation (RAG) assistant using LangChain and FAISS. The assistant is designed to answer questions based on a custom knowledge base, specifically the `project_1_publications.json` file, which contains details about various publications. This project is a part of the Agentic AI Developer Certification Program.

The core functionality involves:
1.  **Data Ingestion**: Processing the JSON data, extracting relevant text and metadata, creating embeddings, and storing them in a FAISS vector store.
2.  **Question Answering**: Allowing users to ask natural language questions, retrieving relevant documents from the vector store, and using a Large Language Model (LLM) to generate answers based on the retrieved context.

## Project Structure

The project is organized as follows:

*   `ingest.py`: Python script responsible for loading data from `project_1_publications.json`, processing it, generating embeddings, and creating/saving the FAISS vector store to the `faiss_index` directory.
*   `app.py`: The main Python application that loads the FAISS vector store and provides a command-line interface (CLI) for users to ask questions and receive answers from the RAG assistant.
*   `requirements.txt`: A file listing all Python dependencies required to run the project.
*   `faiss_index/`: Directory where the generated FAISS vector store is saved. This directory is created by `ingest.py`.
*   `project_1_publications.json`: The JSON file containing the custom knowledge base of publications. (This file is expected to be in the parent directory `../` relative to `ingest.py` and `app.py` as per current setup, or in the root if paths are adjusted).
*   `.env`: A file to store environment variables, primarily the `OPENAI_API_KEY`. This file is not committed to version control (and should be listed in `.gitignore`).
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `README.md`: This file, providing an overview and instructions for the project.

## Requirements

*   Python 3.8+
*   An OpenAI API Key
*   Dependencies listed in `requirements.txt`.

## Setup and Usage

Follow these steps to set up and run the RAG assistant locally:

1.  **Clone the Repository**:
    ```bash
    git clone AmmarAhmedl200961/simple-rag
    cd rag_assistant
    ```

2.  **Create and Activate a Virtual Environment**:
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up OpenAI API Key**:
    Create a file named `.env` in the `rag_assistant` project root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY='your_actual_openai_api_key'
    ```

5.  **Prepare the Data Source**:
    Ensure the `project_1_publications.json` file is located in the directory from which `ingest.py` expects to load it (currently configured for `../project_1_publications.json` relative to the script.

6.  **Ingest Data and Build Vector Store**:
    Run the ingestion script to process the data and create the FAISS index. This only needs to be done once, or whenever the source data changes.
    ```bash
    python ingest.py
    ```
    This will create the `faiss_index` directory.

7.  **Run the RAG Assistant**:
    Execute the application script to start interacting with the assistant:
    ```bash
    python app.py
    ```
    The application will load the index and prompt you to ask a question.

## Sample Usage

Once `app.py` is running, you can ask questions like:

**User:**
```
Enter your question: What is the title of the publication with ID 6652f47f792e787411011179?
```

**Assistant (Example Output Structure):**
```
Thinking...
> Question: What is the title of the publication with ID 6652f47f792e787411011179?
> Context:
[Document(page_content='ID: 6652f47f792e787411011179\nTitle: The Role of Quantum Computing in Climate Change Mitigation\nPublication Description: This publication explores the potential applications of quantum computing in addressing climate change challenges, including complex climate modeling, materials science for renewable energy, and optimization of energy grids. It discusses current research, technological hurdles, and future prospects.', metadata={'id': '6652f47f792e787411011179', 'title': 'The Role of Quantum Computing in Climate Change Mitigation', ...})
... more documents if retrieved ...]

> Answer: The title of the publication with ID 6652f47f792e787411011179 is "The Role of Quantum Computing in Climate Change Mitigation".
```

*(Note: The exact answer and retrieved context will depend on the LLM and the contents of your vector store.)*

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
