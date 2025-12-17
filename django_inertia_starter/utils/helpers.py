"""
Helper functions for path handling, secret generation, and other utilities
"""

import os
import secrets
import string
from pathlib import Path


def get_project_path(project_name, directory):
    """
    Determine the full project path based on project name and directory.

    Examples:
        get_project_path("myproject", ".") -> "./myproject"
        get_project_path("myproject", "/path/to/parent") -> "/path/to/parent/myproject"

    Args:
        project_name (str): Name of the project
        directory (str): Target directory ("." for current directory)

    Returns:
        Path: Full path where project should be created
    """
    directory_path = Path(directory).resolve()

    # If directory is "." (current directory) or doesn't end with project name,
    # create project folder inside it
    if directory == "." or directory_path.name != project_name:
        return directory_path / project_name
    else:
        # If the directory already has the project name, use it directly
        return directory_path


def generate_secret_key(length=50):
    """
    Generate a Django secret key.

    Args:
        length (int): Length of the secret key

    Returns:
        str: Generated secret key
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def get_relative_path_for_display(project_path):
    """
    Get a user-friendly relative path for display purposes.

    Args:
        project_path (Path): Full project path

    Returns:
        str: Relative path or absolute path if relative path calculation fails
    """
    try:
        rel_path = os.path.relpath(project_path)
        if rel_path == ".":
            return "# Already in project directory"
        else:
            return f"cd {rel_path}"
    except (ValueError, OSError):
        return f"cd {project_path}"


def ensure_directory_exists(path):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        path (Path): Directory path to ensure exists
    """
    if not isinstance(path, Path):
        path = Path(path)

    path.mkdir(parents=True, exist_ok=True)


def get_file_extension(frontend, use_typescript):
    """
    Get the appropriate file extension based on frontend and TypeScript choice.

    Args:
        frontend (str): Frontend framework ('react', 'vue3')
        use_typescript (bool): Whether to use TypeScript

    Returns:
        str: File extension ('js', 'ts', 'jsx', 'tsx', 'vue')
    """
    if frontend == "vue3":
        return "vue"

    # For React
    if use_typescript:
        return "tsx"
    else:
        return "jsx"


def get_config_extension(use_typescript):
    """
    Get the appropriate config file extension.

    Args:
        use_typescript (bool): Whether to use TypeScript

    Returns:
        str: Config file extension ('js', 'ts')
    """
    return "ts" if use_typescript else "js"
