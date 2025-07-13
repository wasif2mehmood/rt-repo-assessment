"""RAG Assistant CLI Application.

This script provides a command-line interface for querying
the knowledge base using the RAG system.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src import (
    RAGChain,
    VectorStoreManager,
    get_logger,
    load_settings,
    setup_logging,
)


class RAGAssistantCLI:
    """Command-line interface for the RAG Assistant."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.logger = get_logger("app")
        self.settings = None
        self.rag_chain = None
        
    def initialize(self):
        """Initialize the RAG system."""
        try:
            # Load settings
            self.settings = load_settings()
            self.logger.info("Configuration loaded successfully")
            
            # Initialize vector store manager
            vector_store_manager = VectorStoreManager(self.settings)
            
            # Load the vector store
            self.logger.info("Loading vector store...")
            vector_store_manager.load_vector_store()
            
            # Initialize RAG chain
            self.rag_chain = RAGChain(self.settings, vector_store_manager)
            self.rag_chain.build_chain()
            
            self.logger.info("✅ RAG Assistant initialized successfully")
            return True
            
        except FileNotFoundError:
            print("❌ Error: Vector store not found.")
            print("Please run 'python ingest_new.py' first to create the index.")
            return False
        except Exception as e:
            print(f"❌ Error initializing RAG Assistant: {e}")
            return False
    
    def run_interactive_session(self):
        """Run the interactive question-answering session."""
        print("\n" + "="*60)
        print("🤖 RAG Assistant is ready!")
        print("Ask questions about the publications in the knowledge base.")
        print("Type 'exit', 'quit', or 'q' to quit.")
        print("Type 'help' for more information.")
        print("="*60)
        
        while True:
            try:
                user_question = input("\n💬 You: ").strip()
                
                if not user_question:
                    continue
                
                if user_question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_question.lower() == 'help':
                    self.show_help()
                    continue
                
                # Process the question
                print("\n🤔 Thinking...")
                result = self.rag_chain.query(user_question)
                
                # Display the response
                print(f"\n🤖 Assistant: {result.answer}")
                
                # Optionally show sources (for debugging)
                if result.source_documents and input("\nShow sources? (y/n): ").lower() == 'y':
                    self.show_sources(result.source_documents)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error processing question: {e}")
    
    def show_help(self):
        """Display help information."""
        help_text = """
📚 RAG Assistant Help

This assistant can answer questions about the publications in the knowledge base.

Examples of questions you can ask:
• "What is the title of publication with ID 123?"
• "Tell me about quantum computing publications"
• "What publications are written by [author name]?"
• "Summarize the publication about [topic]"

Commands:
• 'help' - Show this help message
• 'exit', 'quit', 'q' - Exit the application

Tips:
• Be specific in your questions for better results
• The assistant will only answer based on the knowledge base
• If information isn't available, the assistant will tell you
        """
        print(help_text)
    
    def show_sources(self, sources):
        """Display source documents."""
        print("\n📖 Sources:")
        print("-" * 40)
        for i, source in enumerate(sources, 1):
            metadata = source.get('metadata', {})
            print(f"{i}. ID: {metadata.get('id', 'N/A')}")
            print(f"   Title: {metadata.get('title', 'N/A')}")
            print(f"   Content: {source.get('content', 'N/A')}")
            print()


def main():
    """Main application function."""
    # Setup logging
    setup_logging(level="INFO")
    
    # Create and initialize the CLI
    cli = RAGAssistantCLI()
    
    if cli.initialize():
        cli.run_interactive_session()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
