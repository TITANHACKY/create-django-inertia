"""
Base generator class providing common functionality for all generators
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..utils.file_utils import create_file, create_directory


class BaseGenerator:
    """Base class for all project generators"""

    def __init__(self, project_name, project_path, frontend, use_typescript):
        self.project_name = project_name
        self.project_path = Path(project_path)
        self.frontend = frontend
        self.use_typescript = use_typescript

        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def get_context(self):
        """
        Get the base template context.
        Subclasses can override this to add more context variables.
        """
        return {
            "project_name": self.project_name,
            "frontend": self.frontend,
            "use_typescript": self.use_typescript,
        }

    def render_template(self, template_path, output_path, context=None):
        """
        Render a Jinja2 template to a file.

        Args:
            template_path (str): Path to the template file relative to templates directory
            output_path (str): Output path relative to project directory
            context (dict): Additional context variables for template rendering
        """
        if context is None:
            context = {}

        # Merge with base context
        full_context = {**self.get_context(), **context}

        try:
            template = self.env.get_template(template_path)
            content = template.render(**full_context)

            output_file = self.project_path / output_path
            create_file(output_file, content, overwrite=True)

        except Exception as e:
            raise Exception(f"Failed to render template {template_path}: {str(e)}")

    def create_directory_structure(self, directories):
        """
        Create multiple directories.

        Args:
            directories (list): List of directory paths relative to project root
        """
        for directory in directories:
            full_path = self.project_path / directory
            create_directory(full_path)

    def generate(self):
        """
        Generate the project structure.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the generate method")
