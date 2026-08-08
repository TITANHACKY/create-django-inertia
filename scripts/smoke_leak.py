"""Assert the development server does not serve project files.

Usage: smoke_leak.py <project_name>

Run from inside the generated project, with DEBUG on. Guards the MEDIA_URL
regression that turned the media route into a catch-all file server.
"""
import logging
import os
import sys

import django

# Run from inside the generated project: put it on the path ahead of
# this script's own directory.
sys.path.insert(0, os.getcwd())

project = sys.argv[1]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project}.settings")
django.setup()
logging.disable(logging.CRITICAL)

from django.conf import settings  # noqa: E402
from django.test import Client  # noqa: E402

settings.DEBUG = True
settings.ALLOWED_HOSTS = ["testserver"]

client = Client()
failures = []
for path in (f"/{project}/settings.py", "/db.sqlite3", "/.env", "/manage.py"):
    status = client.get(path).status_code
    if status == 200:
        failures.append(f"{path} was served (HTTP 200)")

if failures:
    sys.exit("FAIL: the dev server exposed project files:\n  " + "\n  ".join(failures))

print("OK: project files are not reachable over HTTP")
