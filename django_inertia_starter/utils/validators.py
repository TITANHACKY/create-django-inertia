"""
Validation functions for project names, directories, and user inputs
"""

import re
import os
import keyword
from pathlib import Path


def validate_project_name(name):
    """
    Validate Django project name according to Django's rules.

    Args:
        name (str): Project name to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not name:
        return False

    # Check if it's a Python keyword
    if keyword.iskeyword(name):
        return False

    # Check if it's a valid Python identifier
    if not name.isidentifier():
        return False

    # Django specific checks
    if name.startswith("django"):
        return False

    # Check for common problematic names
    forbidden_names = {
        "test",
        "django",
        "site",
        "main",
        "manage",
        "settings",
        "urls",
        "wsgi",
        "asgi",
        "admin",
        "auth",
        "contenttypes",
        "sessions",
        "messages",
        "staticfiles",
    }

    if name.lower() in forbidden_names:
        return False

    return True


def validate_directory(project_path, force=False):
    """
    Validate that the target directory is suitable for project creation.

    Args:
        project_path (Path): Path where project will be created
        force (bool): Whether to overwrite existing directory

    Returns:
        bool: True if directory is valid/available, False otherwise
    """
    if not isinstance(project_path, Path):
        project_path = Path(project_path)

    # If directory doesn't exist, it's valid
    if not project_path.exists():
        return True

    # If force flag is set, allow overwriting
    if force:
        return True

    # If directory exists and has files, it's not valid without force
    if project_path.is_dir() and any(project_path.iterdir()):
        return False

    return True


def validate_frontend_choice(frontend):
    """
    Validate frontend framework choice.

    Args:
        frontend (str): Frontend framework name

    Returns:
        bool: True if valid choice, False otherwise
    """
    valid_choices = {"react", "vue3"}
    return frontend.lower() in valid_choices


def normalize_project_name(name):
    """
    Normalize project name to a valid Python identifier.

    Args:
        name (str): Original project name

    Returns:
        str: Normalized project name
    """
    # Convert to lowercase and replace invalid characters with underscores
    normalized = re.sub(r"[^a-zA-Z0-9_]", "_", name.lower())

    # Ensure it doesn't start with a number
    if normalized and normalized[0].isdigit():
        normalized = f"project_{normalized}"

    # Remove consecutive underscores
    normalized = re.sub(r"_+", "_", normalized)

    # Remove leading/trailing underscores
    normalized = normalized.strip("_")

    return normalized or "myproject"
