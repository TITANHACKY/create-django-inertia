"""
StartProject command implementation for django-inertia-starter
"""

import click
import os
from pathlib import Path
from ..utils.validators import (
    validate_project_name,
    validate_directory,
    normalize_project_name,
)
from ..utils.helpers import get_project_path, get_relative_path_for_display
from ..generators.django_generator import DjangoGenerator
from ..generators.frontend_generator import FrontendGenerator


def startproject_logic(
    ctx, project_name, frontend, directory, typescript, force, no_install
):
    """
    Create a new Django + Inertia.js project.

    PROJECT_NAME: Name of the project to create
    FRONTEND: Frontend framework (react, vue3) - optional
    DIRECTORY: Directory to create project in (optional, defaults to PROJECT_NAME)

    Examples:

        \b
        # Create project with interactive prompts
        django-inertia startproject myproject

        \b
        # Create React project with TypeScript
        django-inertia startproject myproject react --typescript

        \b
        # Create Vue3 project with JavaScript
        django-inertia startproject myproject vue3

        \b
        # Create in current directory
        django-inertia startproject myproject . react

        \b
        # Create in specific directory
        django-inertia startproject myproject ./my-app react
    """

    # Handle directory argument
    if directory is None:
        # No directory specified - create in subdirectory with project name
        project_path = Path.cwd() / project_name
    elif directory == ".":
        # Create in current directory
        project_path = Path.cwd()
    else:
        # Create in specified directory
        if os.path.isabs(directory):
            project_path = Path(directory)
        else:
            project_path = Path.cwd() / directory

    # Validate project name
    if not validate_project_name(project_name):
        suggested_name = normalize_project_name(project_name)
        click.echo(click.style("❌ Invalid project name.", fg="red"))
        click.echo(
            f"   Project name must be a valid Python identifier and not conflict with Django."
        )
        if suggested_name != project_name:
            click.echo(f"   Suggested name: {click.style(suggested_name, fg='yellow')}")
        return 1

    # Validate directory
    if not validate_directory(project_path, force):
        click.echo(
            click.style(
                f"❌ Directory '{project_path}' already exists and is not empty.",
                fg="red",
            )
        )
        click.echo(
            f"   Use {click.style('--force', fg='yellow')} to overwrite existing files."
        )
        return 1

    # Interactive prompts for missing options
    if not frontend:
        click.echo(
            f"\n🎨 Choose your frontend framework for {click.style(project_name, fg='cyan')}:"
        )
        frontend = click.prompt(
            click.style("Frontend framework", fg="blue"),
            type=click.Choice(["react", "vue3"]),
            show_choices=True,
            default="react",
        )

    if not typescript and not ctx.params.get("typescript"):
        click.echo(
            f"\n📝 Choose language for {click.style(frontend.title(), fg='cyan')}:"
        )
        use_typescript = click.prompt(
            click.style("Use TypeScript?", fg="blue"),
            type=bool,
            default=True,
            show_default=True,
        )
        typescript = use_typescript

    # Display project creation info
    click.echo(f"\n🚀 Creating Django + Inertia.js project...")
    click.echo(f"   📁 Project: {click.style(project_name, fg='green', bold=True)}")
    click.echo(f"   📍 Location: {click.style(str(project_path), fg='yellow')}")
    click.echo(
        f"   ⚛️  Frontend: {click.style(frontend.title(), fg='cyan')} ({click.style('TypeScript' if typescript else 'JavaScript', fg='magenta')})"
    )

    try:
        # Create generators
        django_gen = DjangoGenerator(project_name, project_path, frontend, typescript)
        frontend_gen = FrontendGenerator(
            project_name, project_path, frontend, typescript
        )

        # Generate Django project structure
        click.echo(f"\n📦 Generating Django project structure...")
        django_gen.generate()

        # Generate frontend setup
        click.echo(f"🎨 Setting up {frontend.title()} frontend...")
        frontend_gen.generate()

        # Show success message
        show_success_message(
            project_name, project_path, frontend, typescript, no_install
        )

        return 0

    except Exception as e:
        click.echo(click.style(f"\n❌ Error creating project: {str(e)}", fg="red"))
        # Clean up partial project on error
        if project_path.exists():
            import shutil

            try:
                shutil.rmtree(project_path)
                click.echo(f"🧹 Cleaned up partial project files.")
            except Exception:
                pass
        return 1


def show_success_message(project_name, project_path, frontend, typescript, no_install):
    """Display success message with next steps"""

    click.echo(
        click.style(
            f"\n🎉 Project '{project_name}' created successfully!",
            fg="green",
            bold=True,
        )
    )

    # Determine relative path for user-friendly display
    cd_command = get_relative_path_for_display(project_path)

    click.echo(click.style(f"\n📋 Next steps:", fg="blue", bold=True))

    step = 1
    if cd_command != "# Already in project directory":
        click.echo(click.style(f"{step}. {cd_command}", fg="yellow"))
        step += 1

    # Python environment setup
    click.echo(click.style(f"{step}. python -m venv venv", fg="yellow"))
    step += 1

    # Activation command (platform specific)
    if os.name == "nt":  # Windows
        activate_cmd = "venv\\Scripts\\activate"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"

    click.echo(click.style(f"{step}. {activate_cmd}", fg="yellow"))
    step += 1

    if not no_install:
        # Installation steps
        click.echo(click.style(f"{step}. pip install -r requirements.txt", fg="yellow"))
        step += 1
        click.echo(click.style(f"{step}. npm install", fg="yellow"))
        step += 1

        # Database setup
        click.echo(click.style(f"{step}. python manage.py migrate", fg="yellow"))
        step += 1
    else:
        click.echo(
            click.style(
                f"{step}. # Install dependencies manually (--no-install was used)",
                fg="yellow",
            )
        )
        step += 1

    # Development servers
    click.echo(click.style(f"\n🔥 Development servers:", fg="blue", bold=True))
    click.echo(click.style(f"   Terminal 1: python manage.py runserver", fg="green"))
    click.echo(click.style(f"   Terminal 2: npm run dev", fg="green"))

    # Final info
    click.echo(
        click.style(
            f"\n🌐 Your app will be available at: http://localhost:8000",
            fg="green",
            bold=True,
        )
    )

    # Additional tips
    click.echo(click.style(f"\n💡 Useful commands:", fg="cyan"))
    click.echo("   • python manage.py createsuperuser    # Create admin user")
    click.echo("   • python manage.py startapp <name>    # Create new Django app")
    click.echo("   • npm run build                       # Build for production")

    # Framework specific tips
    if frontend == "react":
        click.echo("   • Add components in static/components/")
        click.echo("   • Add pages in static/pages/")
    else:  # vue3
        click.echo("   • Add components in static/components/")
        click.echo("   • Add pages in static/views/")

    if typescript:
        click.echo("   • TypeScript config: tsconfig.json")

    click.echo(click.style(f"\n🚀 Happy coding!", fg="magenta", bold=True))
