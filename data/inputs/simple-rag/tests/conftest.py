"""Test configuration and fixtures for the RAG Assistant tests."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock

from src.config.settings import AppSettings, OpenAISettings, VectorStoreSettings, DataSettings


@pytest.fixture
def sample_json_data():
    """Sample publication data for testing."""
    return [
        {
            "id": "test123",
            "title": "Test Publication",
            "username": "test_user",
            "license": "MIT",
            "publication_description": "This is a test publication for unit testing."
        },
        {
            "id": "test456",
            "title": "Another Test Publication",
            "username": "another_user",
            "license": "Apache",
            "publication_description": "This is another test publication for testing purposes."
        }
    ]


@pytest.fixture
def temp_json_file(sample_json_data):
    """Create a temporary JSON file with sample data."""
    import json
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_json_data, f)
        yield f.name
    
    # Cleanup
    os.unlink(f.name)


@pytest.fixture
def test_settings(temp_json_file):
    """Create test settings configuration."""
    return AppSettings(
        openai=OpenAISettings(
            api_key="test-api-key",
            model_name="gpt-3.5-turbo",
            embedding_model="text-embedding-ada-002"
        ),
        vector_store=VectorStoreSettings(
            index_path="test_faiss_index",
            chunk_size=500,
            chunk_overlap=100
        ),
        data=DataSettings(
            json_file_path=temp_json_file
        )
    )


@pytest.fixture
def mock_openai_embeddings():
    """Mock OpenAI embeddings for testing."""
    mock = Mock()
    mock.embed_documents.return_value = [[0.1, 0.2, 0.3]] * 10
    mock.embed_query.return_value = [0.1, 0.2, 0.3]
    return mock


@pytest.fixture
def mock_openai_llm():
    """Mock OpenAI LLM for testing."""
    mock = Mock()
    mock.invoke.return_value = "This is a test response from the mocked LLM."
    return mock


@pytest.fixture
def temp_vector_store_path():
    """Create a temporary directory for vector store testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir
