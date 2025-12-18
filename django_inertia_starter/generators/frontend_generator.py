"""
Frontend generator for creating React/Vue frontend setup with Vite
"""

from pathlib import Path
from .base_generator import BaseGenerator
from ..utils.helpers import get_file_extension, get_config_extension


class FrontendGenerator(BaseGenerator):
    """Generator for frontend project structure and configuration"""

    def __init__(self, project_name, project_path, frontend, use_typescript):
        super().__init__(project_name, project_path, frontend, use_typescript)

    def get_context(self):
        """Get frontend-specific template context"""
        context = super().get_context()
        context.update(
            {
                "file_ext": get_file_extension(self.frontend, self.use_typescript),
                "config_ext": get_config_extension(self.use_typescript),
                "lang": "typescript" if self.use_typescript else "javascript",
                "is_vue": self.frontend == "vue3",
                "is_react": self.frontend == "react",
            }
        )
        return context

    def generate(self):
        """Generate frontend project structure"""
        # Create directory structure
        self.create_frontend_directories()

        # Generate package.json and build configuration
        self.generate_build_config()

        # Generate frontend source files
        self.generate_source_files()

        # Generate TypeScript configuration if needed
        if self.use_typescript:
            self.generate_typescript_config()

    def create_frontend_directories(self):
        """Create frontend directory structure"""
        directories = [
            # Frontend source files (inside static directory)
            "static",
            "static/components",
            "static/pages",
            "static/css",
            "static/lib",
        ]

        # Framework specific directories
        if self.frontend == "vue3":
            directories.extend(
                [
                    "static/pages/home",
                ]
            )
        elif self.frontend == "react":
            directories.extend(
                [
                    "static/pages/home",
                    "static/hooks",
                    "static/context",
                ]
            )

        self.create_directory_structure(directories)

    def generate_build_config(self):
        """Generate package.json and build configuration"""
        context = self.get_context()

        # Base configuration files
        config_files = [
            ("frontend/package.json.j2", "package.json"),
            (
                "frontend/vite.config.js.j2",
                f'vite.config.{context["config_ext"]}',
            ),
            ("frontend/index.html.j2", "index.html"),
            ("frontend/postcss.config.mjs.j2", "postcss.config.mjs"),
            (
                "frontend/tailwind.config.js.j2",
                f'tailwind.config.{context["config_ext"]}',
            ),
        ]

        for template_path, output_path in config_files:
            self.render_template(template_path, output_path, context)

    def generate_source_files(self):
        """Generate frontend source files based on framework choice"""
        context = self.get_context()

        if self.frontend == "react":
            self.generate_react_files(context)
        elif self.frontend == "vue3":
            self.generate_vue_files(context)

    def generate_react_files(self, context):
        """Generate React specific files"""
        file_ext = context["file_ext"]

        react_files = [
            ("frontend/react/main.tsx.j2", f"static/main.{file_ext}"),
            (
                "frontend/react/pages/home/page.tsx.j2",
                f"static/pages/home/page.{file_ext}",
            ),
            (
                "frontend/react/components/ThemeToggle.tsx.j2",
                f"static/components/ThemeToggle.{file_ext}",
            ),
            (
                "frontend/react/lib/inertia.ts.j2",
                f"static/lib/inertia.{get_config_extension(self.use_typescript)}",
            ),
        ]

        # CSS files
        css_files = [
            ("frontend/css/app.css.j2", "static/css/app.css"),
        ]

        all_files = react_files + css_files

        for template_path, output_path in all_files:
            self.render_template(template_path, output_path, context)

    def generate_vue_files(self, context):
        """Generate Vue3 specific files"""
        file_ext = context["file_ext"]
        config_ext = context["config_ext"]

        vue_files = [
            ("frontend/vue/main.ts.j2", f"static/main.{config_ext}"),
            ("frontend/vue/pages/home/page.vue.j2", f"static/pages/home/page.vue"),
            (
                "frontend/vue/components/ThemeToggle.vue.j2",
                f"static/components/ThemeToggle.vue",
            ),
            ("frontend/vue/lib/inertia.ts.j2", f"static/lib/inertia.{config_ext}"),
        ]

        # CSS files
        css_files = [
            ("frontend/css/app.css.j2", "static/css/app.css"),
        ]

        all_files = vue_files + css_files

        for template_path, output_path in all_files:
            self.render_template(template_path, output_path, context)

    def generate_typescript_config(self):
        """Generate TypeScript configuration files"""
        context = self.get_context()

        typescript_files = [
            ("frontend/typescript/tsconfig.json.j2", "tsconfig.json"),
            ("frontend/typescript/tsconfig.node.json.j2", "tsconfig.node.json"),
        ]

        # Framework specific TypeScript configs
        if self.frontend == "vue3":
            typescript_files.append(
                ("frontend/typescript/vue-env.d.ts.j2", "static/env.d.ts")
            )

        for template_path, output_path in typescript_files:
            self.render_template(template_path, output_path, context)
