from flask import Flask
import config
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# import config
# app.config.from_ob(config.DevelopmentConfig)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)


import models 

@app.route('/')
def hello():
    return "Hello World!"



@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()