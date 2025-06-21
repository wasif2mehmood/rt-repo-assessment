"""
Wikipedia data collection utilities.
"""

import os
from typing import Dict, List
from pathlib import Path
import wikipediaapi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from .utils import setup_logging, clean_filename, ensure_directory

logger = setup_logging()

class WikipediaDataCollector:
    """Collect and process Wikipedia articles."""
    
    def __init__(self, output_dir: str = "data"):
        """
        Initialize data collector.
        
        Args:
            output_dir: Output directory for collected data
        """
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='RAGAssistant/1.0'
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Setup directories
        self.output_dir = ensure_directory(Path(output_dir))
        self.processed_dir = ensure_directory(self.output_dir / "processed")
        self.raw_dir = ensure_directory(self.output_dir / "raw")

    def collect_topic_articles(self, keywords: List[str], max_articles: int) -> Dict[str, int]:
        """
        Collect Wikipedia articles for given keywords.
        
        Args:
            keywords: List of topics to collect
            max_articles: Maximum number of articles per keyword
            
        Returns:
            Collection statistics
        """
        stats = {
            "collected": 0,
            "failed": 0,
            "errors": []
        }
        
        for keyword in keywords[:max_articles]:
            try:
                logger.info(f"Processing article: {keyword}")
                
                # Get Wikipedia page
                page = self.wiki.page(keyword)
                if not page.exists():
                    raise ValueError(f"No Wikipedia page found for: {keyword}")
                
                # Save raw content
                raw_path = self.raw_dir / f"{clean_filename(keyword)}.txt"
                with open(raw_path, "w", encoding="utf-8") as f:
                    f.write(page.text)
                
                # Process into chunks
                chunks = self.text_splitter.split_text(page.text)
                
                # Save processed chunks
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": page.title,
                            "chunk_id": i,
                            "url": page.fullurl
                        }
                    )
                    
                    chunk_path = self.processed_dir / f"{clean_filename(keyword)}_{i}.txt"
                    with open(chunk_path, "w", encoding="utf-8") as f:
                        f.write(f"Source: {doc.metadata['source']}\n")
                        f.write(f"URL: {doc.metadata['url']}\n")
                        f.write(f"Chunk: {i}\n\n")
                        f.write(doc.page_content)
                
                stats["collected"] += 1
                
            except Exception as e:
                logger.error(f"Error processing {keyword}: {str(e)}")
                stats["failed"] += 1
                stats["errors"].append(f"{keyword}: {str(e)}")
                
        return stats