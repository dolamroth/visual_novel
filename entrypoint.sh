#!/bin/bash

cd /usr/app
git pull

cd /usr/app/visual_novel

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn visual_novel.wsgi --preload -w 2 --bind 0.0.0.0:8000


