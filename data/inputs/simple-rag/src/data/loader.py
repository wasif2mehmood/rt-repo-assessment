"""Data loading and processing utilities."""

import json
import os
from typing import Dict, List

from langchain_community.document_loaders import JSONLoader
from langchain_core.documents import Document

from ..models import Publication


class PublicationLoader:
    """Handles loading and processing of publication data."""
    
    def __init__(self, json_file_path: str):
        """Initialize the loader with the path to the JSON file."""
        self.json_file_path = json_file_path
    
    def extract_publication_metadata(self, record: Dict, metadata: Dict) -> Dict:
        """Extract specific metadata fields from a JSON record."""
        metadata["id"] = record.get("id")
        metadata["title"] = record.get("title")
        metadata["username"] = record.get("username")
        metadata["license"] = record.get("license")
        return metadata
    
    def load_documents(self) -> List[Document]:
        """Load and process documents from the JSON file."""
        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"JSON file not found: {self.json_file_path}")
        
        json_loader = JSONLoader(
            self.json_file_path,
            jq_schema=".[]",
            content_key="publication_description",
            text_content=True,
            metadata_func=self.extract_publication_metadata,
        )
        
        try:
            documents = json_loader.load()
            
            if documents:
                print("--- Debug: Metadata of the first document loaded by JSONLoader ---")
                print(documents[0].metadata)
                print("--- Debug: Page content of the first document (first 200 chars) ---")
                print(f"{documents[0].page_content[:200]}...")
                print("--- End Debug ---")
                
                # Enhance documents with formatted content
                self._enhance_documents(documents)
                
                print("--- Debug: Page content after enhancement (first 400 chars) ---")
                print(f"{documents[0].page_content[:400]}...")
                print("--- End Debug ---")
            
            return documents
            
        except ValueError as e:
            print(f"Error loading JSON file: {e}")
            print(
                "Please ensure the JSON file is correctly formatted and contains "
                "the 'publication_description' key."
            )
            return []
    
    def _enhance_documents(self, documents: List[Document]) -> None:
        """Enhance documents by prepending metadata to content."""
        for doc in documents:
            publication = Publication(
                id=doc.metadata.get("id", "N/A"),
                title=doc.metadata.get("title", "N/A"),
                username=doc.metadata.get("username"),
                license=doc.metadata.get("license"),
                publication_description=doc.page_content
            )
            doc.page_content = publication.to_formatted_content()
    
    def load_publications_as_objects(self) -> List[Publication]:
        """Load publications as Publication objects."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            publications = []
            for item in data:
                publications.append(Publication.from_dict(item))
            
            return publications
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading publications: {e}")
            return []
