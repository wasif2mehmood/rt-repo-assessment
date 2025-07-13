"""Sample queries to demonstrate the RAG Assistant capabilities.

This module provides example queries that users can run to test
the RAG Assistant and understand its capabilities.
"""

from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src import RAGChain, VectorStoreManager, load_settings, setup_logging


def run_sample_queries():
    """Run a series of sample queries against the RAG system."""
    # Setup
    setup_logging(level="INFO")
    settings = load_settings()
    
    # Initialize the system
    vector_store_manager = VectorStoreManager(settings)
    
    try:
        vector_store_manager.load_vector_store()
        rag_chain = RAGChain(settings, vector_store_manager)
        rag_chain.build_chain()
        
        # Sample queries
        sample_queries = [
            "What types of publications are available in the knowledge base?",
            "Can you summarize the publication with the highest ID?",
            "What are the main topics covered in the publications?",
            "Which publications discuss artificial intelligence or machine learning?",
            "What is the total number of publications available?"
        ]
        
        print("🚀 Running Sample Queries")
        print("=" * 50)
        
        for i, query in enumerate(sample_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            print("-" * 30)
            
            result = rag_chain.query(query)
            print(f"🤖 Answer: {result.answer}")
            
            if result.source_documents:
                print(f"📚 Found {len(result.source_documents)} relevant sources")
        
        print("\n✅ Sample queries completed!")
        
    except FileNotFoundError:
        print("❌ Vector store not found. Please run 'python ingest.py' first.")
    except Exception as e:
        print(f"❌ Error running sample queries: {e}")


if __name__ == "__main__":
    run_sample_queries()
