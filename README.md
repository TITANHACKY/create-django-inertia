# Django Inertia Starter

A powerful CLI tool to quickly scaffold Django + Inertia.js projects with React or Vue.js frontends.

## 🚀 Quick Start

### Installation

```bash
pip install create-django-inertia
```

### Create a New Project

```bash
# Basic project creation (interactive prompts)
create-django-inertia myproject

# Create with React and TypeScript
create-django-inertia myproject --react --typescript

# Create with Vue 3 and TypeScript  
create-django-inertia myproject --vue --typescript

# Create in current directory
create-django-inertia myproject . --react
```

### Run Your Project

```bash
cd myproject

# Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate

# Frontend setup  
npm install

# Run development servers
python manage.py runserver & npm run dev
```

Visit http://localhost:8000 to see your app!

## 📁 Project Structure

```
myproject/
├── manage.py
├── requirements.txt
├── package.json             # Frontend dependencies
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript config (if --typescript)
├── .gitignore
│
├── myproject/               # Django project settings
│   ├── settings.py          # Pre-configured with Inertia.js
│   ├── urls.py
│   ├── views.py             # Inertia.js views
│   ├── wsgi.py
│   └── asgi.py
│
├── home/                    # Django app
│   ├── views.py             # Sample Inertia views
│   ├── urls.py
│   ├── models.py
│   └── migrations/
│
├── templates/
│   └── base.html            # Inertia.js layout with Vite integration
│
├── static/                  # Frontend source files
│   ├── components/          # Reusable components
│   ├── pages/               # Inertia.js pages
│   │   └── home/
│   │       └── page.tsx     # Home page component
│   ├── css/
│   │   └── app.css          # Tailwind CSS with OKLCH colors
│   ├── lib/                 # Utilities and helpers
│   └── main.tsx             # Frontend entry point
│
└── media/                   # User uploads
```

## ⚙️ Features

### 🏗️ Full-Stack Integration
- **Django Backend**: Robust Python web framework with ORM, admin, and security
- **Inertia.js**: Seamless SPA experience without separate API
- **Modern Frontend**: React 18 or Vue 3 with Vite 6.0 for fast development

### 🎨 Frontend Options
- **React**: Modern React with hooks and TypeScript support  
- **Vue 3**: Composition API with `<script setup>` syntax
- **TypeScript**: Full TypeScript support for both frameworks
- **Vite 6.0**: Latest build tool with improved performance

### 🔧 Developer Experience  
- **Hot Module Replacement**: Instant updates during development
- **Pre-configured**: Ready-to-use setup with modern defaults
- **Modern Design**: Beautiful landing page with OKLCH color system
- **Tailwind CSS v4**: Latest CSS framework with inline theming
- **Geist Fonts**: Modern typography from Vercel

### 📦 Production Ready
- **Static Files**: Optimized Django static file handling with Vite
- **Modern Dependencies**: Latest stable versions of all packages  
- **Build Process**: Optimized production builds
- **Deployment**: Works with any Django hosting solution

## 🛠️ Command Options

### `create-django-inertia`

```bash
create-django-inertia PROJECT_NAME [DIRECTORY] [OPTIONS]
```

**Arguments:**
- `PROJECT_NAME`: Name of your project (required)
- `DIRECTORY`: Directory to create project in (optional, defaults to project name or use `.` for current directory)

**Options:**
- `--react`: Use React frontend framework
- `--vue`: Use Vue 3 frontend framework  
- `--typescript`: Use TypeScript instead of JavaScript
- `--force`: Overwrite existing directory  
- `--no-install`: Skip installation prompts
- `--help`: Show help message

**Examples:**

```bash
# Interactive setup (prompts for framework choice)
create-django-inertia myblog

# React with TypeScript
create-django-inertia myblog --react --typescript

# Vue 3 with TypeScript
create-django-inertia myblog --vue --typescript

# Create in current directory
create-django-inertia myblog . --react

# Force overwrite existing directory
create-django-inertia myblog --react --force

# Skip installation steps
create-django-inertia myblog --vue --no-install
```

## 🏃‍♂️ Development Workflow

### 1. Create and Setup Project
```bash
create-django-inertia myapp --react --typescript
cd myapp
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install
```

### 2. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin user
```

### 3. Development Servers
```bash
# Single command (runs both servers)
python manage.py runserver & npm run dev

# Or in separate terminals:
# Terminal 1: Django backend
python manage.py runserver

# Terminal 2: Vite frontend  
npm run dev
```

### 4. Create New Pages
1. Add Django view in `home/views.py`:
```python
def about(request):
    return inertia_render(request, 'home/about', {
        'message': 'About our company'
    })
```

2. Add URL route in `home/urls.py`:  
```python
path('about/', views.about, name='about'),
```

3. Create frontend component in `static/pages/home/about.tsx` (React) or `static/pages/home/about.vue` (Vue)

## 🎯 What's Included

### Backend (Django)
- ✅ Django 4.2+ with modern Python features
- ✅ Inertia.js middleware and configuration
- ✅ Home app with sample Inertia views  
- ✅ Admin interface ready
- ✅ Static files configuration for Vite
- ✅ CSRF protection integrated
- ✅ Modern Django project structure

### Frontend (React/Vue)  
- ✅ React 18 or Vue 3 with modern patterns
- ✅ TypeScript support (optional)
- ✅ Vite 6.0 for lightning-fast development
- ✅ Inertia.js client-side routing
- ✅ Tailwind CSS v4 with OKLCH colors
- ✅ Modern landing page with components
- ✅ Hot module replacement
- ✅ Geist fonts integration
- ✅ Production build optimization

## 📚 Learn More

- [Django Documentation](https://docs.djangoproject.com/)
- [Inertia.js Documentation](https://inertiajs.com/)
- [React Documentation](https://react.dev/) 
- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django team for the amazing web framework
- Inertia.js team for bridging frontend and backend
- React and Vue teams for excellent frontend frameworks  
- Vite team for the blazing fast build tool

---

**Happy coding!** 🚀