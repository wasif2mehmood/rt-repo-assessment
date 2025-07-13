"""Data ingestion script for the RAG Assistant.

This script processes the publication data, creates embeddings,
and builds the FAISS vector store.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src import (
    DocumentProcessor,
    PublicationLoader,
    VectorStoreManager,
    get_logger,
    load_settings,
    setup_logging,
)


def main():
    """Main ingestion function."""
    # Setup logging
    logger = setup_logging(level="INFO")
    logger = get_logger("ingest")
    
    logger.info("Starting data ingestion process...")
    
    try:
        # Load configuration
        settings = load_settings()
        logger.info("Configuration loaded successfully")
        
        # Initialize components
        loader = PublicationLoader(settings.data.json_file_path)
        processor = DocumentProcessor(
            chunk_size=settings.vector_store.chunk_size,
            chunk_overlap=settings.vector_store.chunk_overlap
        )
        vector_store_manager = VectorStoreManager(settings)
        
        # Load and process documents
        logger.info(f"Loading documents from {settings.data.json_file_path}")
        documents = loader.load_documents()
        
        if not documents:
            logger.error("No documents were loaded. Exiting.")
            return
        
        logger.info(f"Loaded {len(documents)} documents")
        
        # Split documents into chunks
        logger.info("Processing documents...")
        chunks = processor.split_documents(documents)
        
        if not chunks:
            logger.error("No document chunks created. Exiting.")
            return
        
        logger.info(f"Created {len(chunks)} document chunks")
        
        # Create and save vector store
        logger.info("Creating vector store...")
        vector_store = vector_store_manager.create_vector_store(chunks)
        
        logger.info("Saving vector store...")
        vector_store_manager.save_vector_store()
        
        logger.info("✅ Data ingestion completed successfully!")
        logger.info(f"Vector store saved to: {settings.vector_store.index_path}")
        
    except Exception as e:
        logger.error(f"❌ Error during ingestion: {e}")
        raise


if __name__ == "__main__":
    main()
