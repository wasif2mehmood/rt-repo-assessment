"""
Fact checking utilities for RAG Assistant.
"""

from typing import Dict, List, Tuple
import re
from langchain_community.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class FactChecker:
    """Validates answer factuality against context."""
    
    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize fact checker.
        
        Args:
            similarity_threshold: Minimum similarity score for validation
        """
        self.similarity_threshold = similarity_threshold
        self.embeddings = OpenAIEmbeddings()
    
    def validate_answer(
        self, 
        answer: str, 
        context: str,
        sources: List[Dict]
    ) -> Tuple[bool, float, List[str]]:
        """
        Validate answer factuality against context.
        
        Args:
            answer: Generated answer
            context: Context used for generation
            sources: Source documents metadata
            
        Returns:
            Tuple of (is_valid, confidence_score, warning_messages)
        """
        # Extract statements from answer
        statements = self._extract_statements(answer)
        validations = []
        
        for statement in statements:
            # Check factuality against context
            similarity = self._compute_similarity(statement, context)
            validations.append((similarity >= self.similarity_threshold))
        
        confidence = sum(validations) / len(validations) if validations else 0.0
        
        # Generate warning messages
        warnings = []
        if confidence < 0.8:
            warnings.append("The answer may contain information not directly supported by the documents")
        if not sources:
            warnings.append("No source documents were used to generate this answer")
        
        return all(validations), confidence, warnings
    
    def _extract_statements(self, text: str) -> List[str]:
        """
        Split text into statements.
        
        Args:
            text: Text to split
            
        Returns:
            List of statements
        """
        # Split on sentence boundaries
        statements = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
        return statements
    
    def _compute_similarity(self, statement: str, context: str) -> float:
        """
        Compute semantic similarity between statement and context.
        
        Args:
            statement: Statement to check
            context: Context to check against
            
        Returns:
            Similarity score between 0 and 1
        """
        # Get embeddings
        statement_embedding = self.embeddings.embed_query(statement)
        context_embedding = self.embeddings.embed_query(context)
        
        # Convert to numpy arrays
        statement_array = np.array(statement_embedding).reshape(1, -1)
        context_array = np.array(context_embedding).reshape(1, -1)
        
        # Compute cosine similarity
        similarity = cosine_similarity(statement_array, context_array)[0][0]
        
        return float(similarity)