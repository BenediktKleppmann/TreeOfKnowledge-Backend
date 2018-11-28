#!/bin/bash
gunicorn app:app --daemon
celery worker --app=worker.app
#celery -A worker worker --loglevel=debug