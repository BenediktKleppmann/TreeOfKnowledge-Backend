import app
from sqlalchemy.dialects.postgresql import JSON

db = app.db


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


# from app import db
# from sqlalchemy.dialects import postgresql 


# class Result(db.Model):
# 	__tablename__ = 'results'

# 	 = db.Column(db.String, primary_key=True)
# 	possible_attributes = db.Column(postgresql.ARRAY(db.String), server_default='[]')

# 	def __init__(self, object_type, possible_attributes):
# 		self.object_type = object_type
# 		self.possible_attributes = possible_attributes

# 	def __repr__(self):
# 		return '<object_type {}>'.format(self.id)