"""Data models for the RAG Assistant."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Publication:
    """Represents a publication from the knowledge base."""
    id: str
    title: str
    username: Optional[str] = None
    license: Optional[str] = None
    publication_description: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Publication":
        """Create a Publication instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            username=data.get("username"),
            license=data.get("license"),
            publication_description=data.get("publication_description", "")
        )
    
    def to_formatted_content(self) -> str:
        """Convert publication to formatted content for embedding."""
        prepend_text = (
            f'This document is about a publication. '
            f'The Publication ID is {self.id}. '
            f'The Title is "{self.title}". '
            f'The main content follows:\n\n'
        )
        return prepend_text + self.publication_description


@dataclass
class QueryResult:
    """Represents the result of a RAG query."""
    question: str
    answer: str
    source_documents: List[Dict]
    confidence_score: Optional[float] = None
