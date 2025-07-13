"""Data package for the RAG Assistant."""

from .loader import PublicationLoader
from .processor import DocumentProcessor

__all__ = ["PublicationLoader", "DocumentProcessor"]
