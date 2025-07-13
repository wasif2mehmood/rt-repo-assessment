"""Vector store management for the RAG system."""

import os
from typing import List, Optional

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from ..config import AppSettings


class VectorStoreManager:
    """Manages FAISS vector store operations."""
    
    def __init__(self, settings: AppSettings):
        """Initialize the vector store manager."""
        self.settings = settings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai.api_key,
            model=settings.openai.embedding_model
        )
        self._vector_store: Optional[FAISS] = None
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """Create a new vector store from documents."""
        if not documents:
            raise ValueError("No documents provided for vector store creation.")
        
        print(f"Creating vector store from {len(documents)} documents...")
        self._vector_store = FAISS.from_documents(documents, self.embeddings)
        return self._vector_store
    
    def save_vector_store(self, path: Optional[str] = None) -> None:
        """Save the vector store to disk."""
        if self._vector_store is None:
            raise ValueError("No vector store to save. Create one first.")
        
        save_path = path or self.settings.vector_store.index_path
        self._vector_store.save_local(save_path)
        print(f"Vector store saved to {save_path}")
    
    def load_vector_store(self, path: Optional[str] = None) -> FAISS:
        """Load a vector store from disk."""
        load_path = path or self.settings.vector_store.index_path
        
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"Vector store not found at {load_path}")
        
        try:
            self._vector_store = FAISS.load_local(
                load_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            print(f"Vector store loaded from {load_path}")
            return self._vector_store
        except Exception as e:
            raise RuntimeError(f"Error loading vector store: {e}")
    
    def get_retriever(self, search_kwargs: Optional[dict] = None):
        """Get a retriever from the vector store."""
        if self._vector_store is None:
            raise ValueError("No vector store available. Load or create one first.")
        
        search_kwargs = search_kwargs or {"k": 4}
        return self._vector_store.as_retriever(search_kwargs=search_kwargs)
    
    @property
    def vector_store(self) -> Optional[FAISS]:
        """Get the current vector store."""
        return self._vector_store
