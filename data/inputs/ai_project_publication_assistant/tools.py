from langchain_core.tools import tool
import os
import git
from git import Repo, InvalidGitRepositoryError, GitCommandError

@tool
def git_clone_tool(repo_url: str, target_dir: str = "cloned_repo") -> dict:
    """Clones a GitHub repository into a local directory."""
    try:
        if not repo_url.startswith(("http://", "https://")):
            return {"status": "error", "message": "Invalid URL: must start with http:// or https://"}

        if os.path.exists(target_dir):
            os.system(f"rm -rf {target_dir}")

        print(f"📥 Cloning {repo_url}...")
        Repo.clone_from(repo_url, target_dir)
        return {"status": "success", "repo_path": target_dir}

    except InvalidGitRepositoryError:
        return {"status": "error", "message": "The URL is not a valid Git repository."}
    except GitCommandError as e:
        return {"status": "error", "message": f"Git command failed: {e.stderr.strip()}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@tool
def repo_reader_tool(repo_path: str) -> dict:
    """Reads README and other key files from a given repository path."""
    content = {}
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.lower() in ["readme.md", "readme", "description.md"]:
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content[file] = f.read()
    return {"repo_content": content}

@tool
def keyword_extractor_tool(text: str) -> list:
    """Extracts keywords from input text."""
    import nltk
    from nltk.corpus import stopwords
    from collections import Counter

    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download(['punkt', 'stopwords'])

    words = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    common_words = Counter(filtered_words).most_common(10)
    return [word for word, count in common_words]