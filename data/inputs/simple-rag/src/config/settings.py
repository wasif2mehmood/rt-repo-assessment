"""Configuration settings for the RAG Assistant."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class OpenAISettings:
    """OpenAI API configuration."""
    api_key: str
    model_name: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-ada-002"


@dataclass
class VectorStoreSettings:
    """Vector store configuration."""
    index_path: str = "faiss_index"
    chunk_size: int = 1000
    chunk_overlap: int = 200


@dataclass
class DataSettings:
    """Data source configuration."""
    json_file_path: str


@dataclass
class AppSettings:
    """Main application settings."""
    openai: OpenAISettings
    vector_store: VectorStoreSettings
    data: DataSettings


def load_settings() -> AppSettings:
    """Load and validate application settings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    # Construct the JSON file path
    json_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "project_1_publications.json")
    )
    
    return AppSettings(
        openai=OpenAISettings(api_key=api_key),
        vector_store=VectorStoreSettings(),
        data=DataSettings(json_file_path=json_file_path)
    )
