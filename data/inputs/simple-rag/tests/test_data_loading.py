"""Tests for data loading functionality."""

import pytest
import json
import tempfile
import os

from src.data.loader import PublicationLoader
from src.models.publication import Publication


class TestPublicationLoader:
    """Test cases for PublicationLoader class."""
    
    def test_extract_publication_metadata(self):
        """Test metadata extraction from publication record."""
        loader = PublicationLoader("dummy_path.json")
        
        record = {
            "id": "test123",
            "title": "Test Publication",
            "username": "test_user",
            "license": "MIT",
            "other_field": "ignored"
        }
        
        metadata = {"source": "test_source"}
        result = loader.extract_publication_metadata(record, metadata)
        
        assert result["id"] == "test123"
        assert result["title"] == "Test Publication"
        assert result["username"] == "test_user"
        assert result["license"] == "MIT"
        assert result["source"] == "test_source"  # Original metadata preserved
    
    def test_load_documents_success(self, temp_json_file):
        """Test successful document loading."""
        loader = PublicationLoader(temp_json_file)
        documents = loader.load_documents()
        
        assert len(documents) == 2
        assert "This is a test publication" in documents[0].page_content
        assert documents[0].metadata["id"] == "test123"
        assert documents[1].metadata["title"] == "Another Test Publication"
    
    def test_load_documents_file_not_found(self):
        """Test handling of missing JSON file."""
        loader = PublicationLoader("nonexistent_file.json")
        
        with pytest.raises(FileNotFoundError):
            loader.load_documents()
    
    def test_load_documents_invalid_json(self):
        """Test handling of invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            invalid_json_path = f.name
        
        try:
            loader = PublicationLoader(invalid_json_path)
            documents = loader.load_documents()
            assert documents == []  # Should return empty list on error
        finally:
            os.unlink(invalid_json_path)
    
    def test_enhance_documents(self, temp_json_file):
        """Test document enhancement with formatted content."""
        loader = PublicationLoader(temp_json_file)
        documents = loader.load_documents()
        
        # Check that documents are enhanced with formatted content
        first_doc = documents[0]
        assert "Publication ID is test123" in first_doc.page_content
        assert 'Title is "Test Publication"' in first_doc.page_content
        assert "This is a test publication" in first_doc.page_content
    
    def test_load_publications_as_objects(self, temp_json_file):
        """Test loading publications as Publication objects."""
        loader = PublicationLoader(temp_json_file)
        publications = loader.load_publications_as_objects()
        
        assert len(publications) == 2
        assert isinstance(publications[0], Publication)
        assert publications[0].id == "test123"
        assert publications[0].title == "Test Publication"
        assert publications[1].username == "another_user"
