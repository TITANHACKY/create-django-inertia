"""
Django project generator for creating Django project structure and files
"""

from pathlib import Path
from .base_generator import BaseGenerator
from ..utils.helpers import generate_secret_key
from ..utils.file_utils import make_executable


class DjangoGenerator(BaseGenerator):
    """Generator for Django project structure and configuration"""

    def __init__(self, project_name, project_path, frontend, use_typescript):
        super().__init__(project_name, project_path, frontend, use_typescript)

    def get_context(self):
        """Get Django-specific template context"""
        context = super().get_context()
        context.update(
            {
                "secret_key": generate_secret_key(),
                "django_project_name": self.project_name,
                "allowed_hosts": "['localhost', '127.0.0.1']",
            }
        )
        return context

    def generate(self):
        """Generate Django project structure"""
        # Create directory structure
        self.create_django_directories()

        # Generate Django project files
        self.generate_django_files()

        # Generate configuration files
        self.generate_config_files()

        # Make manage.py executable
        manage_py = self.project_path / "manage.py"
        if manage_py.exists():
            make_executable(manage_py)

    def create_django_directories(self):
        """Create Django project directory structure"""
        directories = [
            # Main project directory
            self.project_name,
            # Templates directory
            "templates",
            # Static files
            "static",
            # Media files
            "media",
        ]

        self.create_directory_structure(directories)

    def generate_django_files(self):
        """Generate main Django project files"""
        context = self.get_context()

        # Main project files
        django_files = [
            ("django/manage.py.j2", "manage.py"),
            ("django/settings.py.j2", f"{self.project_name}/settings.py"),
            ("django/urls.py.j2", f"{self.project_name}/urls.py"),
            ("django/views.py.j2", f"{self.project_name}/views.py"),
            ("django/wsgi.py.j2", f"{self.project_name}/wsgi.py"),
            ("django/asgi.py.j2", f"{self.project_name}/asgi.py"),
            ("django/__init__.py.j2", f"{self.project_name}/__init__.py"),
        ]

        for template_path, output_path in django_files:
            self.render_template(template_path, output_path, context)

    def generate_config_files(self):
        """Generate configuration and requirements files"""
        context = self.get_context()

        config_files = [
            ("config/requirements.txt.j2", "requirements.txt"),
            ("config/.gitignore.j2", ".gitignore"),
            ("config/.env.example.j2", ".env.example"),
            ("templates/base.html.j2", "templates/base.html"),
        ]

        for template_path, output_path in config_files:
            self.render_template(template_path, output_path, context)
