import os

from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from worker import integrate



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

# @app.route('test/', methods=['PUT'])
# def test():
#     return 'test'

# @app.route('/status/<task_id>')
# def taskstatus(task_id):
#     task = long_task.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         response = {
#             'state': task.state,
#             'current': 0,
#             'total': 1,
#             'status': 'Pending...'
#         }
#     elif task.state != 'FAILURE':
#         response = {
#             'state': task.state,
#             'current': task.info.get('current', 0),
#             'total': task.info.get('total', 1),
#             'status': task.info.get('status', '')
#         }
#         if 'result' in task.info:
#             response['result'] = task.info['result']
#     else:
#         # something went wrong in the background job
#         response = {
#             'state': task.state,
#             'current': 1,
#             'total': 1,
#             'status': str(task.info),  # this is the exception raised
#         }
#     return jsonify(response)



# @app.route('start_simulation/', methods=['GET'])
# def start_simulation(request):
#     task = run_simulations.apply_async()
#     return jsonify({}), 202, {'Location': url_for('taskstatus',
#                                                   task_id=task.id)}




if __name__ == '__main__':
    app.run(debug=True)
