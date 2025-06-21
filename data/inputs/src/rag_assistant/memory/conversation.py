"""
Conversation memory management for RAG Assistant.
"""

from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation."""
    question: str
    answer: str
    context: str
    timestamp: datetime


class ConversationMemory:
    """Manages conversation history."""
    
    def __init__(self, max_turns: int = 5):
        """
        Initialize conversation memory.
        
        Args:
            max_turns: Maximum number of conversation turns to keep
        """
        self.max_turns = max_turns
        self.turns: List[ConversationTurn] = []
    
    def add_turn(self, question: str, answer: str, context: str) -> None:
        """
        Add a new conversation turn.
        
        Args:
            question: User's question
            answer: System's answer
            context: Context used for the answer
        """
        turn = ConversationTurn(
            question=question,
            answer=answer,
            context=context,
            timestamp=datetime.now()
        )
        self.turns.append(turn)
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)
    
    def get_context(self) -> str:
        """
        Get conversation history formatted as context.
        
        Returns:
            Formatted conversation history
        """
        return "\n\n".join([
            f"Q: {turn.question}\nA: {turn.answer}"
            for turn in self.turns
        ])
    
    def clear(self) -> None:
        """Clear conversation history."""
        self.turns = []
    
    @property
    def is_empty(self) -> bool:
        """Check if conversation history is empty."""
        return len(self.turns) == 0