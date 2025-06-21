"""
Configuration for the RAG Assistant.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class for RAG Assistant."""
    
    # Model settings
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.0
    embedding_model: str = "text-embedding-3-large"
    
    # Document processing
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Retrieval settings
    retrieval_k: int = 4
    similarity_threshold: float = 0.3  # Lowered from 0.7 to allow more matches
    max_context_tokens: int = 2000    # Maximum tokens for context
    
    # Conversation settings
    enable_conversation: bool = True   # Enable conversation history
    max_conversation_turns: int = 5    # Maximum conversation turns to keep
    
    # Paths
    data_dir: str = "data"
    vectorstore_dir: str = "vectorstore"