#!/usr/bin/env python3
from celery import Celery
from algorithm import approx
import os
import time

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


@app.task(bind=True)
def run_simulations(self):
	total=50
	for i in range(total):
		message = "just did step %s !" % (str(i))
		self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(0.1)
    return {'current': 50, 'total': 50, 'status': 'Task completed!',
            'result': 42}