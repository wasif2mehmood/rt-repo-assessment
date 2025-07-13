"""Tests for RAG chain functionality."""

import pytest
from unittest.mock import Mock, patch

from src.rag.chain import RAGChain
from src.rag.vector_store import VectorStoreManager
from src.models.publication import QueryResult


class TestRAGChain:
    """Test cases for RAGChain class."""
    
    def test_chain_initialization(self, test_settings):
        """Test RAG chain initialization."""
        mock_vector_store_manager = Mock(spec=VectorStoreManager)
        
        rag_chain = RAGChain(test_settings, mock_vector_store_manager)
        
        assert rag_chain.settings == test_settings
        assert rag_chain.vector_store_manager == mock_vector_store_manager
        assert rag_chain._chain is None
    
    def test_format_docs(self, test_settings):
        """Test document formatting for prompts."""
        mock_vector_store_manager = Mock(spec=VectorStoreManager)
        rag_chain = RAGChain(test_settings, mock_vector_store_manager)
        
        # Create mock documents
        mock_docs = [
            Mock(
                page_content="First document content",
                metadata={"id": "doc1", "title": "First Doc"}
            ),
            Mock(
                page_content="Second document content",
                metadata={"id": "doc2", "title": "Second Doc"}
            )
        ]
        
        formatted = rag_chain._format_docs(mock_docs)
        
        assert "First document content" in formatted
        assert "Second document content" in formatted
        assert "---" in formatted  # Separator between docs
    
    @patch('src.rag.chain.ChatOpenAI')
    def test_build_chain(self, mock_openai, test_settings):
        """Test RAG chain building."""
        mock_vector_store_manager = Mock(spec=VectorStoreManager)
        mock_retriever = Mock()
        mock_vector_store_manager.get_retriever.return_value = mock_retriever
        
        rag_chain = RAGChain(test_settings, mock_vector_store_manager)
        chain = rag_chain.build_chain()
        
        assert chain is not None
        assert rag_chain._chain is not None
        mock_vector_store_manager.get_retriever.assert_called_once()
    
    @patch('src.rag.chain.ChatOpenAI')
    def test_query_success(self, mock_openai, test_settings):
        """Test successful query execution."""
        # Setup mocks
        mock_vector_store_manager = Mock(spec=VectorStoreManager)
        mock_retriever = Mock()
        mock_vector_store_manager.get_retriever.return_value = mock_retriever
        
        # Mock retriever response
        mock_docs = [
            Mock(
                page_content="Test document content",
                metadata={"id": "test1", "title": "Test Document"}
            )
        ]
        mock_retriever.invoke.return_value = mock_docs
        
        # Mock LLM response
        mock_llm_instance = Mock()
        mock_llm_instance.invoke.return_value = "Test answer"
        mock_openai.return_value = mock_llm_instance
        
        rag_chain = RAGChain(test_settings, mock_vector_store_manager)
        
        # Mock the chain invoke method
        with patch.object(rag_chain, '_chain') as mock_chain:
            mock_chain.invoke.return_value = "Test answer"
            
            result = rag_chain.query("What is a test?")
        
        assert isinstance(result, QueryResult)
        assert result.question == "What is a test?"
        assert result.answer == "Test answer"
        assert len(result.source_documents) == 1
    
    @patch('src.rag.chain.ChatOpenAI')
    def test_query_error_handling(self, mock_openai, test_settings):
        """Test query error handling."""
        mock_vector_store_manager = Mock(spec=VectorStoreManager)
        mock_retriever = Mock()
        mock_vector_store_manager.get_retriever.return_value = mock_retriever
        
        rag_chain = RAGChain(test_settings, mock_vector_store_manager)
        
        # Mock chain to raise an exception
        with patch.object(rag_chain, '_chain') as mock_chain:
            mock_chain.invoke.side_effect = Exception("Test error")
            
            result = rag_chain.query("What is a test?")
        
        assert isinstance(result, QueryResult)
        assert result.question == "What is a test?"
        assert "Error processing query: Test error" in result.answer
        assert result.source_documents == []
