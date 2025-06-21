"""
Main RAG Assistant implementation.
"""

import os
from typing import Dict, Optional, List, Any
from pathlib import Path
from langchain_openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import Config
from .memory.conversation import ConversationMemory
from .validation.fact_checker import FactChecker
from .utils import setup_logging

logger = setup_logging()

class RAGAssistant:
    """RAG-based question answering assistant."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize RAG Assistant.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config()
        self.vectorstore = None
        self.llm = OpenAI(
            model_name=self.config.model_name,
            temperature=self.config.temperature
        )
        self.embeddings = OpenAIEmbeddings(
            model=self.config.embedding_model
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap
        )
        self.conversation = ConversationMemory(
            max_turns=self.config.max_conversation_turns
        ) if self.config.enable_conversation else None
        self.fact_checker = FactChecker(
            similarity_threshold=self.config.similarity_threshold
        )

    def load_vectorstore(self, path: str) -> None:
        """
        Load vector store from disk.
        
        Args:
            path: Path to vector store
        """
        self.vectorstore = Chroma(
            persist_directory=path,
            embedding_function=self.embeddings
        )

    def query(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using RAG.
        
        Args:
            question: Question to answer
            
        Returns:
            Dictionary containing question, answer, context, and metadata
        """
        if not self.vectorstore:
            raise ValueError("Vector store not loaded. Call load_vectorstore first.")

        # Get conversation context if enabled
        conversation_context = ""
        if self.conversation and not self.conversation.is_empty:
            conversation_context = f"Previous conversation:\n{self.conversation.get_context()}\n\n"

        # Retrieve relevant documents
        docs = self.vectorstore.similarity_search_with_score(
            question,
            k=self.config.retrieval_k
        )
        
        # Filter by relevance score
        relevant_docs = []
        for doc, score in docs:
            if score >= self.config.similarity_threshold:
                relevant_docs.append(doc)
        
        if not relevant_docs:
            return {
                "question": question,
                "answer": "I apologize, but I couldn't find any relevant information in the documents to answer your question.",
                "context": None,
                "confidence": 0.0,
                "sources": [],
                "warnings": ["No relevant documents found for this query"],
                "is_valid": False
            }
        
        # Format context
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Generate answer
        prompt = f"""Please answer the question following these constraints:
1. Use ONLY information provided in the context
2. If information is not present in the context, respond with "That information is not available in the documents"
3. Do not include any uncertain or speculative information

{conversation_context}Context:
{context}

Question: {question}

Answer:"""

        response = self.llm.invoke(prompt)
        
        # Validate answer
        is_valid, confidence, warnings = self.fact_checker.validate_answer(
            str(response),
            context,
            [doc.metadata for doc in relevant_docs]
        )
        
        # Store conversation turn if enabled
        if self.conversation:
            self.conversation.add_turn(question, str(response), context)
        
        return {
            "question": question,
            "answer": str(response),
            "context": context,
            "confidence": confidence,
            "sources": [doc.metadata for doc in relevant_docs],
            "warnings": warnings,
            "is_valid": is_valid
        }

    def ingest_documents(self, input_dir: str) -> None:
        """
        Process documents and create vector store.
        
        Args:
            input_dir: Directory containing documents
        """
        logger.info(f"Building vector store from: {input_dir}")
        
        # Load documents
        documents = []
        input_path = Path(input_dir)
        
        for file_path in input_path.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                # Skip metadata lines
                for _ in range(4):
                    next(f)
                content = f.read().strip()
                
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": file_path.name
                    }
                )
                documents.append(doc)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=os.path.join(os.path.dirname(input_dir), "vectorstore")
        )
        
        logger.info(f"Created vector store with {len(documents)} documents")