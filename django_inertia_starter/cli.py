"""
Main CLI entry point for django-inertia-starter
"""

import click
from . import __version__


@click.command()
@click.argument("project_name")
@click.argument("directory", required=False, default=None)
@click.option("--react", is_flag=True, help="Use React frontend")
@click.option("--vue", "--vue3", is_flag=True, help="Use Vue3 frontend")
@click.option("--typescript", is_flag=True, help="Use TypeScript instead of JavaScript")
@click.option("--force", is_flag=True, help="Overwrite existing directory")
@click.option("--no-install", is_flag=True, help="Skip package installation prompts")
@click.version_option(version=__version__, prog_name="create-django-inertia")
@click.pass_context
def main(ctx, project_name, directory, react, vue, typescript, force, no_install):
    """
    Create a new Django + Inertia.js project.

    PROJECT_NAME: Name of the project to create
    DIRECTORY: Directory to create project in (optional, defaults to project name)

    Examples:

        \b
        # Create project with interactive prompts
        create-django-inertia myproject

        \b
        # Create React project with TypeScript
        create-django-inertia myproject --react --typescript

        \b
        # Create Vue3 project
        create-django-inertia myproject --vue

        \b
        # Create in current directory with React
        create-django-inertia myproject . --react

        \b
        # Create in specific directory with Vue
        create-django-inertia myproject ./my-custom-dir --vue --typescript
    """
    from .commands.startproject import startproject_logic

    # Convert flags to frontend choice
    frontend = None
    if react:
        frontend = "react"
    elif vue:
        frontend = "vue3"

    return startproject_logic(
        ctx, project_name, frontend, directory, typescript, force, no_install
    )


if __name__ == "__main__":
    main()
