"""RAG Assistant - A modular Retrieval Augmented Generation system."""

__version__ = "1.0.0"
__author__ = "RAG Assistant Team"
__description__ = "A modular RAG system for querying custom knowledge bases"

from .config import AppSettings, load_settings
from .data import DocumentProcessor, PublicationLoader
from .models import Publication, QueryResult
from .rag import RAGChain, VectorStoreManager
from .utils import get_logger, setup_logging

__all__ = [
    "AppSettings",
    "load_settings",
    "DocumentProcessor",
    "PublicationLoader",
    "Publication",
    "QueryResult",
    "RAGChain",
    "VectorStoreManager",
    "get_logger",
    "setup_logging",
]
