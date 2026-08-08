"""Render the home page of a generated project and assert it is wired correctly.

Usage: smoke_render.py <project_name> <dev|prod>

Run from inside the generated project. Fails loudly if the page errors, if the
asset URLs point somewhere Vite does not serve, or if Inertia did not mount.
"""
import logging
import os
import sys

import django

# Run from inside the generated project: put it on the path ahead of
# this script's own directory.
sys.path.insert(0, os.getcwd())

project, mode = sys.argv[1], sys.argv[2]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project}.settings")
django.setup()
logging.disable(logging.CRITICAL)

from django.conf import settings  # noqa: E402
from django.test import Client  # noqa: E402

settings.ALLOWED_HOSTS = ["testserver"]

response = Client().get("/")
if response.status_code != 200:
    sys.exit(f"FAIL: GET / returned {response.status_code}, expected 200")

html = response.content.decode()

if 'id="app"' not in html or "data-page" not in html:
    sys.exit("FAIL: Inertia root element missing - the page did not mount")

if mode == "dev":
    # django-vite must point at the paths the Vite dev server actually serves.
    if "localhost:3000/static/dist/" in html:
        sys.exit("FAIL: dev asset URLs include /dist/, which Vite does not serve")
    if "localhost:3000/static/main." not in html:
        sys.exit("FAIL: dev entry script URL missing from the page")
else:
    if "localhost:3000" in html:
        sys.exit("FAIL: production page still references the Vite dev server")
    if "/static/main-" not in html:
        sys.exit("FAIL: hashed production bundle missing from the page")

print(f"OK: {mode} render is correctly wired")
