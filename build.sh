#!/usr/bin/env bash
# Render build script for NotesBridge Django app

set -o errexit  # Exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Auto-create superuser from environment variables (only if DJANGO_SUPERUSER_USERNAME is set)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --no-input || true
fi
