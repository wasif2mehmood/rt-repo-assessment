"""
Vector store building script.
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag_assistant.main import RAGAssistant
from src.rag_assistant.utils import setup_logging

logger = setup_logging()


def main():
    """Main vector store building function."""
    parser = argparse.ArgumentParser(description="Build vector store from documents")
    parser.add_argument(
        "--input", 
        required=True,
        help="Input directory containing documents"
    )
    parser.add_argument(
        "--output",
        default="vectorstore", 
        help="Output directory for vector store"
    )
    
    args = parser.parse_args()
    
    # Initialize RAG assistant
    assistant = RAGAssistant()
    
    # Ingest documents and build vector store
    logger.info(f"Building vector store from: {args.input}")
    assistant.ingest_documents(args.input)
    
    print(f"\n✅ Vector store built successfully!")
    print(f"📁 Saved to: {args.output}")
    print(f"🔍 Ready for queries!")


if __name__ == "__main__":
    main()