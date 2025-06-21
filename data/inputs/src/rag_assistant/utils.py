"""
Utility functions for the RAG Assistant.
"""

import logging
import re
import time
from typing import List, Dict, Any
from pathlib import Path


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level
        
    Returns:
        Configured logger
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def clean_filename(filename: str) -> str:
    """
    Clean filename for safe file system usage.
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    # Remove invalid characters
    filename = re.sub(r'[^\w\s-]', '', filename)
    # Replace spaces with underscores
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename.lower().strip('_')


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text.
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    # Rough estimation: 1 token ≈ 4 characters
    return len(text) // 4


def retry_with_backoff(func, max_retries: int = 3, backoff_factor: float = 1.0):
    """
    Retry function with exponential backoff.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        backoff_factor: Backoff multiplier
        
    Returns:
        Function result
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise e
            
            wait_time = backoff_factor * (2 ** attempt)
            time.sleep(wait_time)


def ensure_directory(path: Path) -> Path:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path