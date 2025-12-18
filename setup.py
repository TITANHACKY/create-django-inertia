from setuptools import setup, find_packages
import os


# Read the README file
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "A CLI tool to quickly scaffold Django + Inertia.js projects"


setup(
    name="create-django-inertia",
    version="1.0.2",
    author="Django Inertia Starter Team",
    author_email="contact@create-django-inertia.com",
    description="A CLI tool to quickly scaffold Django + Inertia.js projects",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/TITANHACKY/create-django-inertia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "jinja2>=3.0.0",
        "colorama>=0.4.4",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "create-django-inertia=django_inertia_starter.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "django_inertia_starter": [
            "templates/**/*",
        ],
    },
    keywords="django, inertia, inertiajs, react, vue, typescript, javascript, scaffolding, cli",
    project_urls={
        "Bug Reports": "https://github.com/TITANHACKY/create-django-inertia/issues",
        "Source": "https://github.com/TITANHACKY/create-django-inertia",
        "Documentation": "https://github.com/TITANHACKY/create-django-inertia#readme",
    },
)
