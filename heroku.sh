#!/bin/bash
gunicorn app:app --daemon
celery -A worker worker --loglevel=debug