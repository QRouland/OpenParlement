#!/bin/sh

# Start cron in background
crond

# Run migrations and db update
cd /app
pwd
export FLASK_APP=app
alembic upgrade head
flask db update

# Start Gunicorn
cd /app
exec gunicorn -w 4 -b 0.0.0.0:8000 main:app