"""File system utilities."""

import os
from pathlib import Path
from typing import List, Optional


def ensure_directory_exists(path: str) -> None:
    """Ensure a directory exists, creating it if necessary."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def find_files_with_extension(directory: str, extension: str) -> List[str]:
    """Find all files with a specific extension in a directory."""
    path = Path(directory)
    if not path.exists():
        return []
    
    return [str(f) for f in path.rglob(f"*.{extension}")]


def validate_file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return Path(file_path).exists()


def get_file_size(file_path: str) -> Optional[int]:
    """Get file size in bytes."""
    try:
        return Path(file_path).stat().st_size
    except (OSError, FileNotFoundError):
        return None
