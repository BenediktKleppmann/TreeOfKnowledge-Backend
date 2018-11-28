#!/bin/bash
gunicorn app:app --daemon
worker: celery worker --app=worker.app
#celery -A worker worker --loglevel=debug