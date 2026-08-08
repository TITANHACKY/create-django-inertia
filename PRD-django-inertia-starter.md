# PRD — create-django-inertia (v1.0.2)

**Status:** Retroactive — documents what shipped, not what is planned
**Version covered:** 1.0.2 (published to PyPI as `create-django-inertia`)
**Last updated:** 2026-08-08

> **How to read this.** This PRD describes a product that already exists. It was written after the fact, by reading the code, to give contributors and evaluators one place to understand what the tool does, who it is for, and where the edges are. Anything not yet proven is marked as an assumption in section 7.4.

---

## 1. Summary

`create-django-inertia` is a command-line tool that creates a working Django + Inertia.js project in one command. It writes out a full Django backend, a React or Vue 3 frontend, and all the config that glues them together, so a developer can start writing features instead of wiring a build system. Version 1.0.2 is a Beta release on PyPI.

---

## 2. Contacts

| Name | Role | Comment |
|---|---|---|
| poonkawin (GitHub: TITANHACKY) | Maintainer / author | Owns the repo, the PyPI package, and all releases to date |
| *TBD* | Contributors | No outside contributors yet. `README.md` invites pull requests |
| Django + Inertia developers | Users | Reached through PyPI and GitHub. No formal user research has been run |

*This is a solo-maintained open-source project. The table is kept so the document stays usable if that changes.*

---

## 3. Background

### What this is about

Django is a strong backend framework. React and Vue are strong frontend frameworks. Putting them together used to mean building and maintaining a separate API — Django serves JSON, the frontend fetches it, and you now own two apps, two routers, and an authentication story that spans both.

Inertia.js removes that split. Django views return page components directly, and the frontend renders them like a single-page app. No API layer in the middle.

The catch is setup. Getting Django, Inertia, Vite, and Tailwind to agree takes a lot of small, easy-to-get-wrong steps: Vite's dev server has to be reachable from Django templates, static file paths have to line up in both dev and production, CSRF tokens have to survive the round trip, and the frontend entry point has to resolve page components by name. A developer trying this for the first time spends hours on plumbing before writing a line of product code.

This tool does that setup for you.

### Why now

Three things came together:

- **Inertia.js has a maintained Django adapter.** `inertia-django` (0.6+) makes the server side straightforward.
- **`django-vite` (3.0+) solved the asset problem.** It handles the dev-server-vs-manifest switch that used to be hand-rolled.
- **The frontend tooling settled.** Vite 6 and Tailwind CSS v4 are stable enough to template against without the output going stale in a month.

There is also a gap in the ecosystem. Laravel ships this experience in the box through its official starter kits. Django has no equivalent. Templates exist, but they are mostly `git clone` repos that go out of date, not an installable CLI.

---

## 4. Objective

### What we are trying to do

Cut the time between "I want to build a Django app with a modern frontend" and "I am writing my first feature" from hours to under five minutes — without asking the developer to learn a new framework or accept a black box they cannot edit.

### Why it matters

- **For developers:** they skip the worst part of the job and get a project they fully own. Everything generated is ordinary Django and ordinary Vite. There is no runtime dependency on this tool after generation — it writes files and exits.
- **For the Django ecosystem:** it lowers the cost of choosing Django for a project that needs a rich frontend, a decision that today often goes to Laravel or Next.js purely on setup friction.
- **For the project:** a well-scoped CLI with a clear job is something people can find, use, and contribute to.

### Key Results

These were not tracked during v1.0.2 development. They are stated here as the measures the project should be judged on going forward.

| # | Key result | Target | How to measure | Status |
|---|---|---|---|---|
| KR1 | A generated project runs with no manual fixes | 100% of the four option combinations (React/Vue × TS/JS) | Run each combination end to end; confirm the home page loads and HMR works | **Not measured** — no automated tests exist |
| KR2 | Time from install to running app | Under 5 minutes on a clean machine | Time a fresh run, including `pip install` and `npm install` | **Not measured** |
| KR3 | Adoption | 500 PyPI downloads in the first 90 days after a public announcement | PyPI download stats | **Not measured** — no announcement has been made |
| KR4 | Generated code stays current | Zero deprecated or end-of-life dependencies in the templates at each release | Check `requirements.txt.j2` and `package.json.j2` before publishing | Currently met |

*Honest note: v1.0.2 shipped without instrumentation or a test suite. Section 7.4 treats that as the top risk.*

---

## 5. Market segment(s)

Segments here are defined by the problem people have, not by company size or job title.

### Primary — the developer who knows Django and wants a real frontend

They are comfortable with Django views, models, and the ORM. They want React or Vue for the interface. They do not want to build and maintain a REST or GraphQL API just to render a page, and they do not want to hand-configure Vite.

**What this segment needs:** the wiring done, and the result readable enough to change.

### Secondary — the developer evaluating Inertia.js on Django

They have read the Inertia docs and want to see it working before committing. Their alternative is following a tutorial for an hour and hoping the versions still match.

**What this segment needs:** a working reference project in one command.

### Tertiary — teams starting new internal tools

Small teams who start several Django projects a year and want them to look the same. Consistent structure matters more to them than any single feature.

**What this segment needs:** a repeatable starting point, not a framework to adopt.

### Constraints

- **Python 3.8+** and **Node.js** must both be installed. The tool does not check for or install either.
- **Generated projects target Django 4.2.x** (`Django>=4.2.0,<5.0`). Django 5.x is listed in the package classifiers but is not what the generated project pins — a known inconsistency.
- **Everything is generated once.** There is no upgrade path. A project created with v1.0.2 stays on v1.0.2's layout unless the developer updates it themselves.
- **SQLite is the default database.** PostgreSQL is available via the included `psycopg2-binary` dependency but is not configured.
- **English only**, no localization in the generated project.

---

## 6. Value proposition(s)

### The job customers are hiring this for

> *"Give me a Django project with a modern frontend that already works, so I can start on the actual product today."*

### What they gain

| Gain | What it looks like in practice |
|---|---|
| **A running app in minutes** | One command produces a project that starts and serves a styled home page |
| **No API to build or maintain** | Django views pass props straight to React or Vue components through Inertia |
| **Modern defaults, already chosen** | Vite 6, Tailwind CSS v4, TypeScript, Geist fonts, an OKLCH color system, and a working light/dark theme toggle |
| **Code they own** | Plain Django and plain Vite files. No wrapper layer, no dependency on this CLI after generation |
| **A choice of frontend** | React 18 or Vue 3, JavaScript or TypeScript — picked by flag or by interactive prompt |

### The pains it avoids

- Hours lost to Vite ↔ Django static file configuration, in dev and again in production.
- Version mismatches from following a blog post written against older packages.
- CSRF failures on the first form submission.
- Deciding, alone and up front, how to lay out pages, components, and shared utilities.
- The "clone the template repo" problem, where the template was last updated two years ago.

### Where it beats the alternatives

| Alternative | Its weakness | How this compares |
|---|---|---|
| **Hand-rolled setup** | Hours of work, easy to get subtly wrong | One command, a configuration known to work |
| **`git clone` a starter repo** | Goes stale; carries the original author's git history and project name | Installed from PyPI, versioned, generates a clean project under your own name |
| **Django + separate SPA + DRF** | Two apps, two routers, duplicated auth | One app, one router, one auth story |
| **Laravel starter kits** | Requires leaving Python | Brings the same experience to the Django stack |
| **`django-admin startproject`** | Backend only — no frontend, no build tooling | Full stack, wired end to end |

**The value curve, in one line:** compete on *setup speed* and *the quality of the defaults*, not on feature count. Deliberately do less than a framework, so the output stays readable.

---

## 7. Solution

### 7.1 UX

The whole product is one command. There is no GUI and no config file.

**Flow A — flags supplied (no prompts):**

```
$ create-django-inertia myblog --react --typescript

🚀 Creating Django + Inertia.js project...
   📁 Project: myblog
   📍 Location: /Users/you/myblog
   ⚛️  Frontend: React (TypeScript)

📦 Generating Django project structure...
🎨 Setting up React frontend...

🎉 Project 'myblog' created successfully!

📋 Next steps:
1. cd myblog
2. python -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. npm install
6. python manage.py migrate

🔥 Development servers:
   Terminal 1: python manage.py runserver
   Terminal 2: npm run dev

🌐 Your app will be available at: http://localhost:8000
```

**Flow B — no flags (interactive):** the tool asks for the frontend framework (React or Vue 3, defaulting to React) and whether to use TypeScript (defaulting to yes), then continues as above.

**Failure paths:**

- *Bad project name* → rejected with a suggested valid name. Names are rejected if they are not valid Python identifiers, are Python keywords, start with `django`, or collide with reserved names like `test`, `admin`, `settings`, `urls`, `auth`, `sessions`, `staticfiles`.
- *Directory exists and is not empty* → rejected, with a pointer to `--force`.
- *Generation fails partway* → the partial project directory is deleted so the developer is not left with half a project.

**Command surface:**

```
create-django-inertia PROJECT_NAME [DIRECTORY] [OPTIONS]

  --react         Use React
  --vue, --vue3   Use Vue 3
  --typescript    Use TypeScript instead of JavaScript
  --force         Overwrite an existing directory
  --no-install    Skip the dependency steps in the printed instructions
  --version       Print the version
  --help          Print help
```

`DIRECTORY` accepts `.` for the current directory, a relative path, or an absolute path. Omitted, it creates a folder named after the project.

### 7.2 Key features

**F1 — Django project generation.** Writes `manage.py`, settings, root URLs and views, WSGI and ASGI entry points, plus a `home` app with models, views, URLs, admin, apps config, tests stub, and a migrations package. Settings arrive pre-wired for Inertia and `django-vite`.

**F2 — Frontend generation.** Writes the Vite config, `package.json`, PostCSS and Tailwind config, an entry point (`main.tsx` / `main.ts`), an Inertia setup helper under `lib/`, a home page component, and a `ThemeToggle` component. React and Vue have separate template sets; the correct one is chosen from the flag.

**F3 — TypeScript as a switch.** When enabled, adds `tsconfig.json`, `tsconfig.node.json`, a `vue-env.d.ts` shim for Vue, the matching `@types/*` packages, and a `type-check` npm script. When disabled, the same project is generated in JavaScript.

**F4 — Inertia + Vite integration.** A `base.html` template ties Django's rendering to Vite's dev server in development and to the build manifest in production, so the same project works both ways without edits.

**F5 — Styling defaults.** Tailwind CSS v4 with inline theming, an OKLCH color system, Geist fonts, and a light/dark theme toggle that works out of the box in both React and Vue.

**F6 — Input validation and safe failure.** Name and directory checks run *before* anything is written, and a failed run cleans up after itself.

**F7 — Guided next steps.** The success message prints exactly what to run next, adjusted for the platform (`venv\Scripts\activate` on Windows, `source venv/bin/activate` elsewhere) and for the chosen framework.

#### What v1.0.2 deliberately does not do

- **It does not install anything.** `--no-install` only shortens the printed instructions; the tool never runs `pip install` or `npm install` in any mode. The flag name over-promises.
- **No authentication scaffolding.** No login, signup, or password reset.
- **No database configuration.** SQLite defaults; PostgreSQL is a dependency, not a setup.
- **No Docker, CI, or deployment files.**
- **No SSR.** Client-side rendering only.
- **No update or eject command.** Generation is one-way.

### 7.3 Technology

- **CLI:** Python 3.8+, built on `click` for argument parsing and prompts, `colorama` for cross-platform colored output.
- **Templating:** Jinja2. Every generated file is a `.j2` template rendered with a context of `project_name`, `frontend`, and `use_typescript`. Templates ship inside the wheel as package data.
- **Structure:** a `BaseGenerator` holds shared rendering and directory logic; `DjangoGenerator` and `FrontendGenerator` subclass it. Adding a third frontend means adding a template set and a branch, not rewriting the tool.
- **Generated stack:** Django ≥4.2 <5.0, `inertia-django` ≥0.6, `django-vite` ≥3.0, WhiteNoise, Gunicorn, `python-dotenv`, `django-extensions`; on the frontend, Vite 6, Tailwind v4, and either React 18 with `@inertiajs/react` 2.x or Vue 3.5 with `@inertiajs/vue3` 1.x.
- **Distribution:** setuptools build, published to PyPI, installed with `pip install create-django-inertia`.

*Note: `requests` is declared as a dependency in `pyproject.toml` but is not imported anywhere in the package.*

### 7.4 Assumptions

Each of these is believed but not proven. They are listed worst-first by what it would cost to be wrong.

| # | Assumption | Risk if wrong | Cheapest way to check |
|---|---|---|---|
| A1 | All four option combinations generate a project that actually runs | **Highest.** A broken combination means a first-run failure — the one moment where a starter tool cannot afford to fail. There is no test suite, so this rests on manual testing during development | Add a CI job that generates all four combinations, installs dependencies, runs `migrate`, builds the frontend, and loads the home page |
| A2 | Developers want the setup done for them rather than done by hand | The whole product | PyPI download counts after a public announcement; GitHub stars and issues |
| A3 | The chosen defaults (Tailwind, Vite, TypeScript-by-default, this folder layout) match what users would pick themselves | Users fight the output instead of building on it; adoption stalls quietly | Ask in issues and in the Django community what people change first |
| A4 | Generation-only, with no upgrade path, is acceptable | Projects rot and the tool gets blamed for it | Watch for "how do I upgrade?" issues |
| A5 | Pinning Django 4.2 while advertising Django 5.0 support in the classifiers will not confuse anyone | Users on Django 5 hit an unexpected constraint | Test against Django 5.x and make the pin and the classifiers agree |
| A6 | The docs match the code | Small trust erosion at exactly the wrong moment. Two known mismatches today: the success message tells Vue users to put pages in `static/views/` when the generator writes them to `static/pages/`, and `--no-install` implies installation the tool never performs | Re-read the README and the success message against the generator; fix both |
| A7 | React and Vue are enough; nobody needs Svelte or Alpine | A whole segment stays out of reach | Wait for requests before building |

---

## 8. Release

### What shipped

| Version | Timing | Contents |
|---|---|---|
| 1.0.0 | Mid-December 2025 | Initial release: CLI, Django and frontend generators, React and Vue templates, TypeScript support |
| 1.0.1 | Same week | Repository URL corrections |
| 1.0.2 | Same week | Theme toggle component for React and Vue, style and configuration updates. Current PyPI release |

All three shipped inside about a week. The package is marked **Development Status :: 4 - Beta**, which is accurate: the feature set is real, the verification is not there yet.

### What is not in v1.x

Recorded here as scope that was consciously left out, not as a commitment:

- **Nearest term:** automated tests across all four combinations; fixing the two doc/code mismatches in A6; deciding whether `--no-install` should install or be renamed.
- **After that:** authentication scaffolding, database configuration, SSR support, Docker and CI templates.
- **Longer term:** more frontend frameworks, an upgrade path for existing projects.

No dates. This is a solo-maintained project and dates would be fiction.

### What "ready to leave Beta" should mean

1. Every option combination is verified by CI on every commit.
2. The README, the success message, and the code agree.
3. At least a handful of real users have generated projects and reported back.

Until then, Beta is the honest label.
