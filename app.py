import os

from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from worker import integrate, run_simulation
from celery.result import AsyncResult
from celery import task, current_task
from simulations import simulation



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# SQLAlchemy
db = SQLAlchemy(app)
# import models 
# try:
# 	result = models.Result(
# 	    url="www.bla.com",
# 	    result_all={'word1':2, 'word2':3},
# 	    result_no_stop_words={'word1':2, 'word2':3}
# 	)
# 	db.session.add(result)
# 	db.session.commit()
# 	return result.id
# except:
# 	return {"error":"Unable to add item to database."}
# # retrieve
# result = models.Result.query.filter_by(id=result.id).first()



TASKS = {}


@app.route('/', methods=['GET'])
def list_tasks():
    tasks = {task_id: {'ready': task.ready()}
             for task_id, task in TASKS.items()}
    return jsonify(tasks)

@app.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    response = {'task_id': task_id}

    task = TASKS[task_id]
    if task.ready():
        response['result'] = task.get()
    return jsonify(response)



@app.route('/', methods=['PUT'])
def put_task():
    f = request.json['f']
    a = request.json['a']
    b = request.json['b']
    c = request.json['c']
    d = request.json['d']
    size = request.json.get('size', 100)

    task_id = len(TASKS)
    TASKS[task_id] = integrate.delay(f, a, b, c, d, size)
    response = {'result': task_id}
    return jsonify(response)

# ===============================================================
# ===============================================================
# ===============================================================

@task
def run_simulation():
	for i in range(40):
		simulation.run_simulation()
		current_task.update_state(state='PROGRESS',
            meta={'current': i, 'total': 40})


@app.route('poll_simulation/<int:task_id>', methods=['GET'])
def poll_task(task_id):
    response = {'task_id': task_id}
    job = AsyncResult(task_id)
    data = job.result or job.state
    response['data'] = data
    return jsonify(response)


@app.route('init_simulation/', methods=['GET'])
def init_simulation(request):
    """ A view to start a background job and redirect to the status page """
    job = run_simulation.delay()
    return jsonify({"job_id":job.id})








if __name__ == '__main__':
    app.run(debug=True)
