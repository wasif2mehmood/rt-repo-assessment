# A Wikipedia-based RAG System with Fact Verification and Conversation Management

## Abstract

This paper presents an improved implementation of a Retrieval-Augmented Generation (RAG) system that addresses two critical challenges in question-answering systems: factual accuracy and contextual awareness. Using Wikipedia articles as the knowledge source, we introduce a fact verification mechanism and conversation management system that significantly improve the reliability and user experience of RAG-based applications. Our implementation demonstrates enhanced accuracy in information retrieval and response generation while maintaining strict adherence to source document content.

## 1. Introduction

### 1.1 Background

RAG systems have emerged as a powerful approach for grounding large language model outputs in factual information. However, existing implementations often face challenges with:
- Hallucination and factual accuracy
- Context relevance and retrieval
- Conversation continuity
- Source traceability

### 1.2 Objectives

Our implementation aims to:
1. Enhance factual accuracy through systematic verification
2. Improve context relevance through advanced similarity metrics
3. Maintain conversation history for contextual responses
4. Provide transparent source attribution

## 2. System Architecture

### 2.1 Core Components

```python
class RAGAssistant:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.vectorstore = None
        self.llm = OpenAI(
            model_name=self.config.model_name,
            temperature=self.config.temperature
        )
        self.embeddings = OpenAIEmbeddings(
            model=self.config.embedding_model
        )
```

The system consists of four main components:
1. Document Processing Pipeline
2. Vector Store Management
3. Fact Verification System
4. Conversation Memory Manager

### 2.2 Fact Verification

```python
class FactChecker:
    def validate_answer(
        self, 
        answer: str, 
        context: str,
        sources: List[Dict]
    ) -> Tuple[bool, float, List[str]]:
        statements = self._extract_statements(answer)
        validations = []
        for statement in statements:
            similarity = self._compute_similarity(statement, context)
            validations.append((similarity >= self.similarity_threshold))
```

### 2.3 Conversation Management

```python
class ConversationMemory:
    def add_turn(self, question: str, answer: str, context: str):
        turn = ConversationTurn(
            question=question,
            answer=answer,
            context=context,
            timestamp=datetime.now()
        )
        self.turns.append(turn)
```

## 3. Implementation Details

### 3.1 Data Processing

- Data source: Wikipedia articles via Wikipedia API
- Topic-based article collection
- Chunk size: 1000 tokens
- Overlap: 200 tokens
- Embedding model: text-embedding-3-large
- Vector store: ChromaDB

### 3.2 Data Collection

The system includes a Wikipedia data collector that:
- Fetches articles based on specified topics
- Processes and cleans article content
- Splits content into manageable chunks
- Maintains source attribution

```python
class WikipediaDataCollector:
    def collect_topic_articles(
        self, 
        keywords: List[str], 
        max_articles: int
    ) -> Dict[str, int]:
        for keyword in keywords[:max_articles]:
            page = self.wiki.page(keyword)
            if not page.exists():
                continue
            self._process_article(page)
```

### 3.3 Query Processing

1. Context retrieval with similarity threshold
2. Fact verification against source documents
3. Response generation with source attribution
4. Conversation history integration

### 3.4 Configuration Management

```python
@dataclass
class Config:
    model_name: str = "gpt-4-turbo-preview"
    temperature: float = 0.0
    chunk_size: int = 1000
    chunk_overlap: int = 200
    similarity_threshold: float = 0.3
```

## 4. Evaluation

### 4.1 Test Scenarios

We evaluated our system using three types of queries:

1. In-context queries
   - Example: "What is data science and what are its main components?"
   - Result: Successfully retrieved relevant context and provided accurate answers
   - Source attribution: Properly cited source documents

2. Out-of-context queries
   - Example: "Who is the CEO of Google?"
   - Result: Correctly identified as out-of-scope
   - Response: "That information is not available in the documents"
   - Warning messages: Appropriately generated

3. Irrelevant queries
   - Example: "How do I make a pizza?"
   - Result: Correctly identified as irrelevant
   - Response: Clear indication of information not being in the document scope

### 4.2 Results Analysis

Our system demonstrated:
- Accurate identification of in-context vs out-of-context queries
- Clear warning messages for out-of-scope information
- Proper source attribution for valid responses
- Consistent refusal to hallucinate or speculate

### 4.3 Key Findings

1. Context Relevance
   - Successfully maintained factual accuracy
   - Avoided speculation on unknown information
   - Provided clear indications when information was not available

2. Source Attribution
   - All responses linked to source documents
   - Clear confidence scoring
   - Transparent warning system

## 5. Usage and Reproduction

### 5.1 Installation

```bash
git clone https://github.com/daishir0/rag-document-assistant
cd rag-document-assistant
pip install -r requirements.txt
```

### 5.2 Configuration

```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 5.3 Basic Usage

```python
from rag_assistant import RAGAssistant

assistant = RAGAssistant()
assistant.load_vectorstore("data/vectorstore")
result = assistant.query("What is data science?")
```

## 6. Future Work

1. Multi-modal support
2. Real-time fact verification
3. Enhanced conversation understanding
4. Performance optimization

## 7. Conclusion

Our implementation demonstrates significant improvements in RAG system reliability through fact verification and conversation management. The system shows robust performance in maintaining factual accuracy while providing transparent source attribution.

## References

1. LangChain Documentation
2. ChromaDB Documentation
3. OpenAI API Documentation
4. Vector Similarity Search: Theory and Implementation

## Code Availability

The complete implementation is available at:
https://github.com/daishir0/rag-document-assistant

## License

MIT License

## Appendix A: Experimental Results

### A.1 Data Collection Results

```bash
$ python scripts/collect_data.py --topic data_science --max-articles 15

📊 Collection Summary:
✅ Successfully collected: 14 articles
❌ Failed: 0 articles
📁 Data saved to: data
📄 Processed files: data/processed

Collected articles:
- Data science
- Big data
- Data mining
- Statistical inference
- Predictive analytics
- Data visualization
- Business intelligence
- Apache Spark
- Hadoop
- Python
- R
- Pandas
- NumPy
- Scikit-learn
```

### A.2 Vector Store Creation

```bash
$ python scripts/build_vectorstore.py --input data/processed --output data/vectorstore

2025-05-22 15:53:07,993 - INFO - Building vector store from: data/processed
2025-05-22 15:53:13,520 - INFO - Created vector store with 474 documents

✅ Vector store built successfully!
📁 Saved to: data/vectorstore
🔍 Ready for queries!
```

### A.3 Query Results

Example query responses:

1. In-context query:
```
❓ Question: What is data science and what are its main components?
💡 Answer: Data science is a concept that unifies statistics, data analysis, informatics, and their related methods to understand and analyze actual phenomena with data. Its main components include techniques and theories from mathematics, statistics, computer science, information science, and domain knowledge.
🎯 Confidence: 1.00
📚 Sources: data_science_1.txt
```

2. Out-of-context query:
```
❓ Question: Who is the CEO of Google?
💡 Answer: That information is not available in the documents.
⚠️ Warnings: No relevant documents found for this query
🎯 Confidence: 0.00
```

3. Irrelevant query:
```
❓ Question: How do I make a pizza?
💡 Answer: That information is not available in the documents.
⚠️ Warnings: No relevant documents found for this query
🎯 Confidence: 0.00
```