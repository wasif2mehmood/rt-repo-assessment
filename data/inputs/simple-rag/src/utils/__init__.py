"""Utilities package for the RAG Assistant."""

from .file_utils import (
    ensure_directory_exists,
    find_files_with_extension,
    get_file_size,
    get_project_root,
    validate_file_exists,
)
from .logging import get_logger, setup_logging

__all__ = [
    "ensure_directory_exists",
    "find_files_with_extension",
    "get_file_size",
    "get_project_root",
    "validate_file_exists",
    "get_logger",
    "setup_logging",
]
