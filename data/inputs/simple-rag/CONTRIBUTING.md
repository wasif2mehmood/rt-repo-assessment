# Contributing to RAG Assistant

Thank you for your interest in contributing to the RAG Assistant project! This guide will help you get started with contributing to our codebase.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- Git installed and configured
- A GitHub account
- Basic knowledge of Python and RAG concepts

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   # Fork the repo on GitHub, then clone your fork
   git clone https://github.com/your-username/rag_assistant-w1.git
   cd rag_assistant-w1
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set Up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 📝 Development Guidelines

### Code Style

We follow PEP 8 guidelines with some modifications:
- Maximum line length: 88 characters
- Use type hints for all function parameters and return values
- Write descriptive docstrings for all classes and functions
- Use meaningful variable and function names

Example:
```python
def process_documents(documents: List[Document], chunk_size: int = 1000) -> List[Document]:
    """Process documents by splitting them into chunks.
    
    Args:
        documents: List of documents to process
        chunk_size: Maximum size of each chunk
        
    Returns:
        List of processed document chunks
    """
    # Implementation here
    pass
```

### Testing

- Write tests for all new features and bug fixes
- Maintain test coverage above 80%
- Use pytest for testing
- Place tests in the `tests/` directory

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src tests/
```

### Documentation

- Update README.md for significant changes
- Add docstrings to all public functions and classes
- Include examples in docstrings where helpful
- Update type hints as needed

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Clear Title**: Describe the issue briefly
2. **Environment Details**: Python version, OS, package versions
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Expected Behavior**: What you expected to happen
5. **Actual Behavior**: What actually happened
6. **Error Messages**: Include full error messages and stack traces
7. **Additional Context**: Screenshots, logs, or other relevant information

## 💡 Submitting Changes

### Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow the coding guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **Push Changes**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to GitHub and create a pull request
   - Fill out the pull request template
   - Link any related issues

### Commit Message Format

We use conventional commits for clear change history:

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding or updating tests
- `chore:` maintenance tasks

Examples:
```
feat: add support for PDF document loading
fix: resolve vector store loading issue
docs: update installation instructions
refactor: improve error handling in RAG chain
```

## 🎯 Types of Contributions

### Code Contributions

- **Bug Fixes**: Fix existing bugs or issues
- **New Features**: Add new functionality
- **Performance Improvements**: Optimize existing code
- **Code Refactoring**: Improve code structure and readability

### Non-Code Contributions

- **Documentation**: Improve README, add examples, write tutorials
- **Testing**: Add or improve test coverage
- **Issue Triage**: Help organize and prioritize issues
- **Community Support**: Help other users in discussions

## 🔍 Review Process

All contributions go through a review process:

1. **Automated Checks**: CI/CD runs tests and code quality checks
2. **Code Review**: Maintainers review the code for quality and correctness
3. **Testing**: Changes are tested in different environments
4. **Documentation Review**: Ensure documentation is updated appropriately
5. **Approval**: Once everything passes, the change is approved and merged

### Review Criteria

- Code follows project guidelines
- All tests pass
- Documentation is updated
- Changes are backwards compatible (when possible)
- No security vulnerabilities introduced

## 📚 Resources

### Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://faiss.ai/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Project-Specific Resources

- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api.md)
- [Example Implementations](examples/)

## ❓ Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Open a new issue with the "question" label
3. Join our community discussions
4. Contact the maintainers directly

Thank you for contributing to the RAG Assistant project! 🎉
