"""
Data collection script for Wikipedia articles.
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag_assistant.data_collector import WikipediaDataCollector
from src.rag_assistant.utils import setup_logging

logger = setup_logging()


def main():
    """Main data collection function."""
    parser = argparse.ArgumentParser(description="Collect Wikipedia articles for RAG")
    parser.add_argument(
        "--topic", 
        choices=["machine_learning", "artificial_intelligence", "data_science"],
        required=True,
        help="Topic collection to gather"
    )
    parser.add_argument(
        "--max-articles", 
        type=int, 
        default=15,
        help="Maximum number of articles to collect"
    )
    parser.add_argument(
        "--output-dir", 
        default="data",
        help="Output directory for collected data"
    )
    
    args = parser.parse_args()
    
    # Topic collections
    topic_collections = {
        "machine_learning": [
            "Machine learning", "Deep learning", "Neural network",
            "Supervised learning", "Unsupervised learning", "Reinforcement learning",
            "Support vector machine", "Random forest", "Natural language processing",
            "Computer vision", "Convolutional neural network", "Transformer (machine learning model)",
            "BERT (language model)", "GPT-3", "Large language model"
        ],
        "artificial_intelligence": [
            "Artificial intelligence", "Machine learning", "Expert system",
            "Knowledge representation", "Automated reasoning", "Robotics",
            "Intelligent agent", "Artificial general intelligence", "AI alignment",
            "Explainable artificial intelligence", "Turing test", "Chinese room",
            "Symbolic artificial intelligence", "Connectionism", "Evolutionary computation"
        ],
        "data_science": [
            "Data science", "Big data", "Data mining", "Statistical inference",
            "Predictive analytics", "Data visualization", "Business intelligence",
            "Apache Spark", "Hadoop", "Python (programming language)",
            "R (programming language)", "Pandas (software)", "NumPy", "Scikit-learn"
        ]
    }
    
    # Initialize collector
    collector = WikipediaDataCollector(args.output_dir)
    
    # Get topic keywords
    keywords = topic_collections[args.topic]
    
    # Collect articles
    results = collector.collect_topic_articles(keywords, args.max_articles)
    
    # Print summary
    print(f"\n📊 Collection Summary:")
    print(f"✅ Successfully collected: {results['collected']} articles")
    print(f"❌ Failed: {results['failed']} articles")
    print(f"📁 Data saved to: {collector.output_dir}")
    print(f"📄 Processed files: {collector.processed_dir}")
    
    if results['errors']:
        print(f"\n⚠️ Errors encountered:")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")


if __name__ == "__main__":
    main()