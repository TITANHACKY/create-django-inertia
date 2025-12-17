"""
File operation utilities for creating and managing project files
"""

import os
import shutil
from pathlib import Path


def create_file(filepath, content, overwrite=False):
    """
    Create a file with specified content.

    Args:
        filepath (Path): Path to the file to create
        content (str): Content to write to the file
        overwrite (bool): Whether to overwrite existing files
    """
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    # Ensure parent directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Check if file exists and we're not overwriting
    if filepath.exists() and not overwrite:
        return False

    # Write the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def copy_file(src, dest, overwrite=False):
    """
    Copy a file from source to destination.

    Args:
        src (Path): Source file path
        dest (Path): Destination file path
        overwrite (bool): Whether to overwrite existing files
    """
    if not isinstance(src, Path):
        src = Path(src)
    if not isinstance(dest, Path):
        dest = Path(dest)

    # Ensure destination parent directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Check if destination exists and we're not overwriting
    if dest.exists() and not overwrite:
        return False

    # Copy the file
    shutil.copy2(src, dest)
    return True


def create_directory(dirpath):
    """
    Create a directory and all necessary parent directories.

    Args:
        dirpath (Path): Directory path to create
    """
    if not isinstance(dirpath, Path):
        dirpath = Path(dirpath)

    dirpath.mkdir(parents=True, exist_ok=True)


def remove_directory(dirpath):
    """
    Remove a directory and all its contents.

    Args:
        dirpath (Path): Directory path to remove
    """
    if not isinstance(dirpath, Path):
        dirpath = Path(dirpath)

    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)


def make_executable(filepath):
    """
    Make a file executable (mainly for manage.py).

    Args:
        filepath (Path): Path to the file to make executable
    """
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    if filepath.exists():
        # Add execute permission for owner
        current_mode = filepath.stat().st_mode
        filepath.chmod(current_mode | 0o100)
