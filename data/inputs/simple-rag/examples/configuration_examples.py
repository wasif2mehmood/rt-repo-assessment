"""Configuration example showing how to customize the RAG Assistant.

This example demonstrates how to create different configurations
for various use cases and environments.
"""

from src.config.settings import (
    AppSettings, 
    OpenAISettings, 
    VectorStoreSettings, 
    DataSettings
)


def create_development_config():
    """Create a configuration for development environment."""
    return AppSettings(
        openai=OpenAISettings(
            api_key="your-api-key-here",
            model_name="gpt-3.5-turbo",
            embedding_model="text-embedding-ada-002"
        ),
        vector_store=VectorStoreSettings(
            index_path="faiss_index_dev",
            chunk_size=800,  # Smaller chunks for development
            chunk_overlap=150
        ),
        data=DataSettings(
            json_file_path="test_data/sample_publications.json"
        )
    )


def create_production_config():
    """Create a configuration for production environment."""
    return AppSettings(
        openai=OpenAISettings(
            api_key="your-production-api-key",
            model_name="gpt-4",  # More powerful model for production
            embedding_model="text-embedding-ada-002"
        ),
        vector_store=VectorStoreSettings(
            index_path="/data/faiss_index",
            chunk_size=1200,  # Larger chunks for better context
            chunk_overlap=250
        ),
        data=DataSettings(
            json_file_path="/data/production_publications.json"
        )
    )


def create_testing_config():
    """Create a configuration for testing environment."""
    return AppSettings(
        openai=OpenAISettings(
            api_key="test-api-key",
            model_name="gpt-3.5-turbo",
            embedding_model="text-embedding-ada-002"
        ),
        vector_store=VectorStoreSettings(
            index_path="test_faiss_index",
            chunk_size=500,  # Small chunks for faster testing
            chunk_overlap=100
        ),
        data=DataSettings(
            json_file_path="tests/fixtures/test_publications.json"
        )
    )


if __name__ == "__main__":
    print("Configuration Examples:")
    print("1. Development Config:", create_development_config())
    print("2. Production Config:", create_production_config())
    print("3. Testing Config:", create_testing_config())
