# Audit — create-django-inertia v1.0.2

**Date:** 2026-08-08
**Method:** every template read, then all four option combinations generated, installed, built, and run.
**Original verdict:** the happy path works in development. **Production is broken, and the dev server leaks `settings.py`.**
**Current status:** **every finding in this document is fixed and re-verified** — see [§0](#0-fixes-applied). A CI smoke matrix now guards against regressions.

---

## 0. Fixes applied

Applied to the templates and re-verified by regenerating all four combinations from scratch.

| # | Fix | Where | Verification |
|---|---|---|---|
| B2 | Define `MEDIA_URL` / `MEDIA_ROOT` | `templates/django/settings.py.j2` | `GET /<project>/settings.py` → **404** (was 200 + SECRET_KEY); `GET /db.sqlite3` → **404**; `GET /` → 200 |
| B1 | `STATICFILES_DIRS` narrowed to `static/dist` (see note below) | `templates/django/settings.py.j2` | `DEBUG=False` render → **200**, assets at `/static/main-*.js` (was `DjangoViteAssetNotFoundError`) |
| B4 | Uncomment `InertiaMiddleware` | `templates/django/settings.py.j2` | DELETE-then-redirect → **303** (was 302); stale asset version → **409** (was 200) |
| B7 | `lib/` → `/lib/` | `templates/config/.gitignore.j2` | `git check-ignore static/lib/inertia.ts` → **not ignored** |
| B3 | `--typescript/--javascript` tri-state flag | `cli.py`, `commands/startproject.py` | All four combinations generate with **stdin closed**, exit 0 (JS variants were exit 1) |
| B8 | `strictPort: true` | `templates/frontend/vite.config.js.j2` | Present in generated config; Vite now fails loudly instead of drifting to another port |

Two notes on B1. `STATIC_ROOT` also moved from the relative string `'staticfiles/'` to `BASE_DIR / 'staticfiles'` (small issue #9) — `django-vite` derives the manifest path from `STATIC_ROOT`, so leaving it relative would have made the fix depend on the working directory.

And the first attempt at B1 was wrong. Setting `DJANGO_VITE_STATIC_URL_PREFIX = 'dist'` fixed production but broke development: django-vite applies the prefix to dev-server URLs too, so the page started requesting `http://localhost:3000/static/dist/main.tsx`, which Vite does not serve. The Django response was still HTTP 200, so a status-code check missed it. Pointing `STATICFILES_DIRS` at `static/dist` instead fixes production **and** B9 while leaving dev URLs correct. `scripts/smoke_render.py` now asserts on the asset URLs, not just the status code.

### Second pass — everything else

| # | Fix | Verification |
|---|---|---|
| B5 | The `home` app is now generated and wired: `INSTALLED_APPS`, `include('home.urls')`, `name = 'home'`, component `'home'`. The duplicate project-level `views.py` is gone | `manage.py test` → **2 tests pass**, including one asserting the Inertia JSON component is `home` |
| B6 | `tsconfig` `paths`/`include` repointed at `static/`, `types: ["vite/client"]` added, Vue switched to `vue-tsc` | `tsc --listFiles` → **4 real files** (was 0); a planted type error now **fails** the check |
| B9 | `STATICFILES_DIRS` narrowed to `static/dist` | `collectstatic` publishes **3 build artifacts**, no `.tsx` source (was 5 source files) |
| B10 | **Both** clients aligned on `^2.3.27` (Vue was v1, React v2.2). React stays on 18 | Both render in a real browser against `inertia-django` 1.2, props live, no console errors. **Not v3 — see below** |
| B11 | Upper bounds on all server deps; `Framework :: Django :: 5.0` classifier dropped to match the `<5.0` pin | `pip install -r requirements.txt` resolves clean |
| Version | `__init__.py` is the single source (`1.1.0`); `pyproject.toml` reads it via `dynamic`; `setup.py` deleted | `--version` → **1.1.0** |
| §4 | `requests` and `get_project_path()` removed; `tailwind.config` and `index.html` no longer generated; `.env` generated with the `SECRET_KEY` and loaded via dotenv; WhiteNoise and django-extensions wired up; `psycopg2-binary` commented out; project `README.md` generated; `--force` clears the target; theme handling reworked (see below); React entry no longer wrapped in `DOMContentLoaded`; the Vue "static/views/" message corrected | All four combinations regenerated and re-run end to end |

**Theme switching — broken, then fixed.**

The `.dark`/`.light` handling had two mechanisms fighting each other. `app.css` carried a
`@media (prefers-color-scheme: dark) { :root:not(.light) { ... } }` block, so the stylesheet
depended on a `.light` class to opt *out* of system dark mode, while `ThemeToggle` drove a
`.dark` class. Removing the redundant-looking `.light` toggle broke light mode outright on any
machine set to dark: `:root:not(.light)` always matched, so the toggle changed the icon and
nothing else.

Fixed by deleting the media-query block entirely and keeping one mechanism: the pre-paint script
in `base.html` resolves `localStorage` → system preference into a single `.dark` class before
first paint, and `ThemeToggle` initialises its state by reading that class back rather than
re-deriving it. Verified in a browser for React and Vue: dark → light → dark, and the choice
survives a reload with the correct icon and no flash.

**Found while fixing, and also fixed:**

- **The landing page ignored every prop Django sent it.** Both page components destructured `message`, `project_name`, `frontend`, `typescript` and then rendered hardcoded text, with the values baked in by Jinja at generation time. The starter never demonstrated the one thing Inertia exists for. Surfaced by the now-working type-check (`TS6198: All destructured elements are unused`); both pages now render the real props.
- **`.gitignore` excluded `package-lock.json`.** The lockfile is what makes installs reproducible, and excluding it compounded B11. Now committed.
- **`--force` would have deleted `.git`.** The new clearing logic preserves `.git`, `node_modules`, and virtualenvs.
- **The error path would delete a pre-existing directory.** `create-django-inertia app . --force` failing midway called `rmtree` on the whole working directory. It now only removes a directory this run created.

### Known limitation, deliberately accepted

The Vite dev-server port is hardcoded to 3000 in two places (`vite.config`, `DJANGO_VITE_DEV_SERVER_PORT`). With `strictPort: true` (B8), a developer whose port 3000 is busy now gets a hard failure and must edit both files. That is strictly better than the old silent drift, but a `--port` option would be better still. Not done.

### Regression guard

`.github/workflows/smoke.yml` runs the four-combination matrix on every push: generate non-interactively, install both dependency sets, `check`, `migrate`, `test`, type-check, build, render with `DEBUG=True` and `DEBUG=False`, and assert the dev server serves no project files.

**What it does not cover:** the matrix asserts on server-rendered HTML, so it would not have caught the Inertia v3 mount failure, and it cannot see a theme toggle that changes an icon but no colours. Both needed a real browser. A headless browser step — assert the page has visible text, click the toggle, assert the computed background colour changed — would close both gaps. Not done.

The two assertion scripts (`scripts/smoke_render.py`, `scripts/smoke_leak.py`) were tested against the original bugs by reintroducing them:

```
FAIL: dev asset URLs include /dist/, which Vite does not serve
FAIL: the dev server exposed project files:
  /reactts/settings.py was served (HTTP 200)
  /db.sqlite3 was served (HTTP 200)
```

**Nothing from this audit remains open.**

---

## 1. What was actually run

*Results below are from the **pre-fix** run against v1.0.2 as published. See §0 for the post-fix results.*

| Step | Result |
|---|---|
| Generate React + TS | ✅ exit 0 |
| Generate Vue + TS | ✅ exit 0 |
| Generate React (JS) | ❌ **exit 1** non-interactively — see B3 |
| Generate Vue (JS) | ❌ **exit 1** non-interactively — see B3 |
| `pip install -r requirements.txt` | ✅ all four |
| `python manage.py check` | ✅ "no issues" (misleading — see B2) |
| `python manage.py migrate` | ✅ |
| `runserver` → `GET /` | ✅ HTTP 200, Inertia page data correct |
| `npm install` + `npm run build` | ✅ all four |
| Vite dev server + module graph | ✅ entry and page glob resolve |
| `npm run type-check` | ⚠️ **passes while checking zero files** — see B6 |
| **`DEBUG=False` render** | ❌ **`DjangoViteAssetNotFoundError`** — see B1 |
| **`GET /<project>/settings.py`** | ❌ **HTTP 200, SECRET_KEY returned** — see B2 |

---

## 2. Blockers

### B1 — Production rendering fails completely — ✅ FIXED

Nothing renders once `DEBUG=False`. Verified:

```
DjangoViteAssetNotFoundError: Cannot find main.tsx for app=default
in Vite manifest at staticfiles/manifest.json
```

**Cause.** Vite writes the manifest to `static/dist/manifest.json`. `collectstatic` copies it to `staticfiles/dist/manifest.json`. `django-vite` looks in `STATIC_ROOT / static_url_prefix / manifest.json` — with no prefix set, that is `staticfiles/manifest.json`. The paths never meet. Asset URLs are wrong the same way: django-vite would emit `/static/main-*.js` while the file sits at `/static/dist/main-*.js`.

Every project generated by v1.0.2 fails on its first deploy.

**Fix (verified).** Point `STATICFILES_DIRS` at the build output rather than the source tree:

```python
STATICFILES_DIRS = [BASE_DIR / "static" / "dist"]
```

`collectstatic` then copies `static/dist/*` to `staticfiles/*`, which is exactly where django-vite looks with no prefix configured — and it fixes B9 at the same time. After the change:

```
status 200
<link rel="stylesheet" href="/static/main-B1XY8Yar.css" />
<script type="module" src="/static/main-BnvXiDDR.js"></script>
```

Do **not** solve this with `DJANGO_VITE_STATIC_URL_PREFIX = "dist"` — see the note in §0.

---

### B2 — The dev server serves your entire project directory — ✅ FIXED

```
$ curl http://127.0.0.1:8000/reactts/settings.py
SECRET_KEY = 'vy*IDOx7v1uh6TC33tAqx*@uX9)*uVfh^uAV2FAMHCB*!!%COf'
status=200
```

`db.sqlite3` and `.env` are reachable the same way.

**Cause.** `urls.py` ends with:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

but `settings.py` **never defines `MEDIA_URL` or `MEDIA_ROOT`**. Django's defaults are `MEDIA_URL = '/'` and `MEDIA_ROOT = ''`, so this registers the catch-all route `^(?P<path>.*)$` serving files from the working directory. Every unmatched URL becomes a file read.

`manage.py check` reports no issues, so nothing warns you.

**Fix.** Add to `settings.py.j2`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

The generator already creates the `media/` directory — only the settings are missing. Severity is limited to `DEBUG=True`, but that is the mode every user starts in, and dev servers do get bound to `0.0.0.0` on shared networks.

---

### B3 — JavaScript projects cannot be generated non-interactively — ✅ FIXED

```
$ create-django-inertia myapp --react < /dev/null
📝 Choose language for React:
Use TypeScript? [True]: Aborted!          # exit 1
```

There is no `--javascript` or `--no-typescript` flag, and the guard meant to skip the prompt is a no-op:

```python
if not typescript and not ctx.params.get("typescript"):   # both are the same value
```

`ctx.params["typescript"]` *is* `typescript`, so the prompt fires whenever `--typescript` is absent. Any scripted or CI use of the JS path fails.

**Fix.** Replace the flag pair with a tri-state option:

```python
@click.option("--typescript/--javascript", "typescript", default=None,
              help="Use TypeScript or JavaScript (prompts if omitted)")
...
if typescript is None:
    typescript = click.confirm("Use TypeScript?", default=True)
```

---

## 3. Correctness and completeness

### B4 — `InertiaMiddleware` is commented out — ✅ FIXED

You asked specifically what this does. It is commented out in `settings.py.j2`:

```python
    # 'inertia.middleware.InertiaMiddleware',
```

It has four jobs. Measured on a generated project, with and without it:

```
AS SHIPPED (commented) | DELETE that redirects -> HTTP 302   browser repeats DELETE on the target -> 405
AS SHIPPED (commented) | stale asset version   -> HTTP 200   client keeps stale JS after a deploy

WITH middleware        | DELETE that redirects -> HTTP 303   browser retries as GET (correct)
WITH middleware        | stale asset version   -> HTTP 409   client reloads fresh assets
```

1. **303 on redirects after `PUT`/`PATCH`/`DELETE`.** A `302` tells the browser to repeat the *same method* on the redirect target, so a delete-then-redirect ends in `405 Method Not Allowed`. This is the single most common Inertia bug, and the middleware exists mainly to prevent it.
2. **Asset versioning.** When the client's `X-Inertia-Version` no longer matches the server's, the middleware answers `409` with a location header so the browser does a hard reload and picks up the new bundle. Without it, users keep running the JavaScript from before your deploy until they manually refresh.
3. **CSRF token refresh.** Inertia requests are XHR and never render a template, so `{{ csrf_token }}` never runs and the `XSRF-TOKEN` cookie never updates. The middleware calls `get_token(request)` on every request. Without it, anything that rotates the token — `login()` does — leaves the SPA holding a stale token, and the next `POST` gets `403`.
4. **Flash messages** survive the forced refresh (`messages.get_messages(request).used = False`).

The first page load works without it, which is exactly why this is easy to ship and painful to debug later.

**Fix.** Uncomment it. It belongs after `AuthenticationMiddleware` and `MessageMiddleware`.

---

### B5 — The `home` app documented in the README does not exist — ✅ FIXED

`README.md` shows this structure:

```
home/                    # Django app
├── views.py
├── urls.py
├── models.py
└── migrations/
```

The generated project has no `home/` directory. Templates for it exist under `templates/django/apps/home/`, but **`DjangoGenerator` never renders them**, and `INSTALLED_APPS` has no entry for the app. They are dead files.

They would not have worked as written either:

- `apps.py` declares `name = 'apps.home'`, a package the generator never creates.
- `apps/home/views.py.j2` renders the component `'Home'`, while the frontend resolves `./pages/${name}/page.tsx` and the only page is `pages/home/`. Capital `H` would not resolve.

The home view actually in use is the project-level `views.py`, which renders `'home'` — correct.

**Fix.** Either wire the app up properly (render the templates, fix `name` to `home`, fix the component to `home`, add it to `INSTALLED_APPS` and include its URLs) or delete the dead templates and correct the README. Wiring it up is the better answer — a sample app is the natural place for users to add their second page.

---

### B6 — `npm run type-check` checks nothing — ✅ FIXED

```
$ npx tsc --noEmit --listFiles | grep -v node_modules | wc -l
0
$ echo 'const x: number = "not a number"' > static/typebomb.ts
$ npx tsc --noEmit ; echo $?
0                                   # passes
```

`tsconfig.json` has `"include": ["src/**/*.ts", ...]` and `"paths": {"@/*": ["./src/*"]}`, but the source lives in `static/`, not `src/`. Zero files are checked, and the `@/` alias resolves only in Vite — editors will flag every `@/components/...` import as missing.

Vue is worse: `vue-tsc` is installed but the script runs plain `tsc`, which cannot read `.vue` files at all. `env.d.ts` is written to `static/`, which the config also excludes.

**Fix.**

```jsonc
"paths": { "@/*": ["./static/*"] },
"include": ["static/**/*.ts", "static/**/*.d.ts", "static/**/*.tsx"]  // + "static/**/*.vue" for Vue
```

and for Vue, `"type-check": "vue-tsc --noEmit"`.

---

### B7 — `.gitignore` swallows `static/lib/` — ✅ FIXED

```
$ git check-ignore -v static/lib/inertia.ts
.gitignore:17:lib/    static/lib/inertia.ts
```

The `.gitignore` is the standard Python one, whose `lib/` rule (meant for build artifacts) matches the generated `static/lib/` directory. `inertia.ts` — a source file the tool just wrote — would never be committed, and the project would break for the next person who clones it.

**Fix.** Narrow the rule to `/lib/` or add `!static/lib/`.

---

### B8 — Vite port collisions fail silently — ✅ FIXED

This happened live during the audit: port 3000 was held by another project, so Vite printed

```
Port 3000 is in use, trying another one...
➜  Local: http://localhost:3001/static/
```

and moved on. Django, meanwhile, keeps emitting `http://localhost:3000/static/main.tsx`, because `DJANGO_VITE_DEV_SERVER_PORT = 3000` is hardcoded. The page then loads assets from *whatever else* is on port 3000 — in this case an unrelated portfolio site — or nothing at all. There is no error, just a blank page.

**Fix.** `strictPort: true` in `vite.config`, so a collision fails loudly instead of drifting.

---

### B9 — `collectstatic` publishes your frontend source — ✅ FIXED

```
staticfiles/main.tsx
staticfiles/pages/home/page.tsx
staticfiles/components/ThemeToggle.tsx
staticfiles/lib/inertia.ts
staticfiles/css/app.css
```

`STATICFILES_DIRS = [BASE_DIR / "static"]` points at the *source* directory, so every `.tsx`/`.ts` file is copied into the deployed static root alongside the built bundle. Frontend source is public anyway, but this bloats deploys and means anything a developer drops into `static/` is served to the internet.

**Fix.** Point `STATICFILES_DIRS` at `static/dist`, or add `--ignore` patterns to the documented deploy step.

---

### B10 — React and Vue are on different Inertia major versions — ✅ FIXED

| | Client | Protocol |
|---|---|---|
| React | `@inertiajs/react` `^2.2.0` | v2 |
| Vue | `@inertiajs/vue3` `^1.2.0` | v1 |
| Server | `inertia-django` 1.2.0 | v2 (emits `encryptHistory`, `clearHistory`) |

Vue users get an older client against a v2-capable server: no deferred props, no prefetching, no polling. The server side supports all of it — `inertia-django` exports `defer`, `merge`, `optional`, and `lazy`.

**npm latest for both clients is `3.6.1`, but v3 does not work with this server.** Verified in a browser, not just at build time:

| Client | Builds | Type-checks | Runs |
|---|---|---|---|
| `@inertiajs/react@3.6.1` | ✅ | ✅ | ❌ **blank page** |
| `@inertiajs/react@2.3.27` | ✅ | ✅ | ✅ |
| `@inertiajs/vue3@2.3.27` | ✅ | ✅ | ✅ |

The v3 client throws on mount against `inertia-django` 1.2:

```
TypeError: Cannot read properties of null (reading 'component')
    at createInertiaApp (@inertiajs_react.js)
```

The server renders `<div id="app" data-page="...">` — the v1/v2 convention — and the v3 client no longer reads it. **A v3 upgrade is blocked on `inertia-django`, not on the frontend.**

This is the sharpest lesson in this audit: the v3 client installed cleanly, built cleanly, and type-checked cleanly. Only loading the page in a browser caught it.

**Fix applied:** both clients on `^2.3.27` — same major, matching the server's protocol. React stays on 18; the only reason to move to 19 was to unblock the v3 client, and that reason is gone.

---

### B11 — Server dependencies have no upper bounds — ✅ FIXED

`inertia-django>=0.6.0` resolved to **1.2.0** in this audit — a major version the templates were never tested against. It happens to work; next time it may not.

Relatedly, `requirements.txt` pins `Django>=4.2.0,<5.0` while `pyproject.toml` advertises `Framework :: Django :: 5.0` in its classifiers. Pick one.

---

## 4. Smaller issues

| # | Issue | Fix |
|---|---|---|
| 1 | `__init__.py` says `1.0.0`; `pyproject.toml`/`setup.py` say `1.0.2`. `--version` prints **1.0.0** | Single source of truth |
| 2 | `requests` declared as a dependency, imported nowhere | Remove |
| 3 | `get_project_path()` written and imported, never called (path logic is inlined in `startproject_logic`) | Remove or use |
| 4 | `tailwind.config.{js,ts}` generated, but Tailwind v4 is CSS-first and ignores it. Its `content` globs point at `./src/**` regardless | Delete, or add `@config` to `app.css` |
| 5 | `index.html` generated at project root referencing `/src/main.tsx`, a path that does not exist | Delete — Django serves the HTML |
| 6 | `.env.example` generated and `python-dotenv` installed, but settings never load `.env`. `SECRET_KEY` is written into `settings.py` and committed | Load `.env`, read `SECRET_KEY` from it |
| 7 | `whitenoise` installed but absent from `MIDDLEWARE`; `django-extensions` installed but absent from `INSTALLED_APPS` | Wire up or drop |
| 8 | `psycopg2-binary` always installed despite the "(optional)" comment | Move to an extras file |
| 9 | `STATIC_ROOT = 'staticfiles/'` is a relative string — resolves against the working directory | `BASE_DIR / 'staticfiles'` |
| 10 | `--force` overwrites files but never clears the directory; stale files from a previous project survive | Clear the target first |
| 11 | No `README.md` is generated in the new project | Add one with the run commands |
| 12 | `ThemeToggle` toggles both `dark` and `light` classes; only `.dark` exists in `app.css`. Theme also flashes before hydration | Drop the `light` class; add a pre-paint inline script |
| 13 | React entry wraps in `DOMContentLoaded`, Vue does not | Make them consistent |
| 14 | No tests and no CI in this repo | See below |

---

## 5. Fix order

**Before the next release** — ✅ **all done**, see §0:

1. ~~B2 — define `MEDIA_URL` / `MEDIA_ROOT`~~
2. ~~B1 — add `DJANGO_VITE_STATIC_URL_PREFIX = "dist"`~~
3. ~~B4 — uncomment `InertiaMiddleware`~~
4. ~~B7 — fix the `lib/` gitignore rule~~
5. ~~B3 — add `--javascript` / fix the prompt guard~~
6. ~~B8 — `strictPort: true`~~

**Next, still open** — B5 (home app), B6 (TypeScript config), B10 (Vue Inertia v2), B9, B11.

Version numbers should also be reconciled before publishing: `__init__.py` still says `1.0.0` while `pyproject.toml` says `1.0.2`, and these fixes warrant a bump.

**Then, the thing that would have caught all of this:** a CI job that, for each of the four combinations, generates a project, installs both dependency sets, runs `migrate`, builds the frontend, renders `/` with `DEBUG=True` **and** `DEBUG=False`, and asserts HTTP 200. Every blocker in this document would have been caught by that job on the first run.

---

## 6. So — does the scaffold look like the README?

Not quite. Actual output versus the documented structure:

| README says | Reality |
|---|---|
| `home/` app with `views.py`, `urls.py`, `models.py`, `migrations/` | **Absent.** Never generated |
| `static/pages/home/page.tsx` | ✅ Correct |
| `templates/base.html` | ✅ Correct |
| `media/` | ✅ Directory created — but unusable, see B2 |
| *(not mentioned)* | `index.html`, `postcss.config.mjs`, `tailwind.config.ts`, `.env.example`, `static/hooks/`, `static/context/` all appear |
| "Add pages in `static/views/`" *(success message, Vue)* | Wrong — the generator writes `static/pages/` |

The core claim of the README — Django, Inertia, Vite, Tailwind, React or Vue, wired together and running — **is true in development**. The gaps are the home app, production, and the docs describing a structure the code does not produce.
