#!/usr/bin/env python3
from celery import Celery, current_task
from algorithm import approx
import os

# run with:
# $ redis-server
# $ celery -A worker worker --loglevel=debug
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
app = Celery(__name__, backend='rpc://', broker=redis_url)
app.conf.update(BROKER_URL=redis_url, CELERY_RESULT_BACKEND=redis_url)

## easier, if you don't care about exceptions:
# integrate = app.task(approx)


@app.task
def integrate(*args, **kwargs):
    try:
        return approx(*args, **kwargs)
    except Exception:
    	return
        # return {"error": "couldn't execute algorithm.approx()"}