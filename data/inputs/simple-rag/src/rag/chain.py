"""RAG chain implementation for question answering."""

from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from ..config import AppSettings
from ..models import QueryResult
from .vector_store import VectorStoreManager


class RAGChain:
    """Implements the RAG (Retrieval Augmented Generation) chain."""
    
    def __init__(self, settings: AppSettings, vector_store_manager: VectorStoreManager):
        """Initialize the RAG chain."""
        self.settings = settings
        self.vector_store_manager = vector_store_manager
        self.llm = ChatOpenAI(
            openai_api_key=settings.openai.api_key,
            model_name=settings.openai.model_name
        )
        self.prompt_template = self._create_prompt_template()
        self._chain = None
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Create the prompt template for the RAG chain."""
        template = """Answer the question based only on the following context.
If the context is empty or doesn't contain the answer, say you don't have enough information.

Context:
{context}

Question: {question}
"""
        return ChatPromptTemplate.from_template(template)
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format retrieved documents for the prompt."""
        page_contents = []
        for doc in docs:
            # Extract metadata for debugging (optional)
            source_id = doc.metadata.get("id", "N/A")
            title = doc.metadata.get("title", "N/A")
            
            # The document content already has ID and Title prepended
            page_contents.append(doc.page_content)
        
        return "\n\n---\n\n".join(page_contents)
    
    def build_chain(self):
        """Build the RAG chain."""
        retriever = self.vector_store_manager.get_retriever()
        
        self._chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        
        return self._chain
    
    def query(self, question: str) -> QueryResult:
        """Execute a query against the RAG system."""
        if self._chain is None:
            self.build_chain()
        
        try:
            # Get the answer
            answer = self._chain.invoke(question)
            
            # Get source documents for reference
            retriever = self.vector_store_manager.get_retriever()
            source_docs = retriever.invoke(question)
            
            # Format source documents for the result
            formatted_sources = []
            for doc in source_docs:
                formatted_sources.append({
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                })
            
            return QueryResult(
                question=question,
                answer=answer,
                source_documents=formatted_sources
            )
            
        except Exception as e:
            return QueryResult(
                question=question,
                answer=f"Error processing query: {e}",
                source_documents=[]
            )
