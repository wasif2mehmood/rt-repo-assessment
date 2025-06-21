# Enhanced RAG Document Assistant

A production-ready implementation of a Retrieval-Augmented Generation (RAG) system with fact verification and conversation management capabilities.

## Features

- 🔍 Advanced document retrieval with ChromaDB
- ✅ Fact verification system
- 💬 Conversation history management
- 📊 Confidence scoring
- ⚠️ Warning system for out-of-context queries
- 📝 Source attribution

## Project Structure

```
rag-document-assistant/
├── src/
│   └── rag_assistant/
│       ├── __init__.py
│       ├── config.py
│       ├── main.py
│       ├── data_collector.py
│       ├── utils.py
│       ├── memory/
│       │   └── conversation.py
│       └── validation/
│           └── fact_checker.py
├── scripts/
│   ├── collect_data.py
│   └── build_vectorstore.py
├── examples/
│   └── basic_usage.py
├── data/
│   ├── processed/
│   └── vectorstore/
├── requirements.txt
├── .env.example
├── README.md
└── publication.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/daishir0/rag-document-assistant
cd rag-document-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Usage

### Data Collection

```bash
python scripts/collect_data.py --topic your_topic --max-articles 15
```

### Build Vector Store

```bash
python scripts/build_vectorstore.py --input data/processed --output data/vectorstore
```

### Basic Usage

```python
from rag_assistant import RAGAssistant

# Initialize assistant
assistant = RAGAssistant()

# Load vector store
assistant.load_vectorstore("data/vectorstore")

# Query
result = assistant.query("What is data science?")
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
```

## Configuration

Key configuration options in `.env`:

```env
# Model Settings
RAG_MODEL_NAME=gpt-4o-mini
RAG_EMBEDDING_MODEL=text-embedding-3-large
RAG_TEMPERATURE=0.0

# Retrieval Settings
RAG_RETRIEVAL_K=4
RAG_SIMILARITY_THRESHOLD=0.3
```

## Documentation

See [publication.md](publication.md) for detailed technical information and implementation details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this work in your research, please cite:

```bibtex
@software{rag_assistant,
  title = {Enhanced RAG Document Assistant},
  author = {daishir0},
  year = {2025},
  url = {https://github.com/daishir0/rag-document-assistant}
}
```

## Acknowledgments

- OpenAI for providing the language models
- LangChain for the RAG framework
- ChromaDB for vector storage