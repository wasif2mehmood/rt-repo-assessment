"""
Basic usage example for RAG Assistant.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag_assistant import RAGAssistant


def main():
    """Basic usage demonstration."""
    
    # Initialize the assistant
    print("🤖 Initializing RAG Assistant...")
    assistant = RAGAssistant()
    
    # Load pre-built vector store
    print("📚 Loading vector store...")
    vectorstore_path = os.path.join(os.path.dirname(__file__), "..", "data", "vectorstore")
    assistant.load_vectorstore(vectorstore_path)
    
    # Test questions
    questions = [
        # Normal questions about data science
        "What is data science and what are its main components?",
        "How is Python used in data science?",
        "What is the difference between data mining and business intelligence?",
        
        # Questions about information not in the documents
        "Who is the CEO of Google?",
        "What will be the weather tomorrow?",
        
        # Questions with low relevance to the context
        "How do I make a pizza?",
        "Tell me about ancient Egyptian pyramids"
    ]
    
    print("\n🔍 Asking questions...")
    for question in questions:
        print(f"\n❓ Question: {question}")
        
        try:
            result = assistant.query(question)
            print(f"💡 Answer: {result['answer']}")
            
            if result['warnings']:
                print("\n⚠️ Warnings:")
                for warning in result['warnings']:
                    print(f"  - {warning}")
            
            print(f"\n🎯 Confidence: {result['confidence']:.2f}")
            
            print("\n📄 Context used:")
            if result['context']:
                print(result['context'][:1000] + "..." if len(result['context']) > 1000 else result['context'])
            else:
                print("No relevant context found")
            
            if result['sources']:
                print("\n📚 Sources:")
                for source in result['sources']:
                    print(f"  - {source['source']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()