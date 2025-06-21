"""
RAG Document Assistant

A production-ready RAG assistant for question-answering based on custom documents.
"""

__version__ = "1.0.0"
__author__ = "Daishiro Hirashima"

from .main import RAGAssistant
from .data_collector import WikipediaDataCollector
from .config import Config
from .memory.conversation import ConversationMemory
from .validation.fact_checker import FactChecker

__all__ = [
    "RAGAssistant",
    "WikipediaDataCollector",
    "Config",
    "ConversationMemory",
    "FactChecker"
]