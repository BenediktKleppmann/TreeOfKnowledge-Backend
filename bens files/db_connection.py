from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import text


def get_all_data_points(self):
	sql = text('SELECT * FROM data_points;')
	result = db.engine.execute(sql)
	result_string = ""
	for row in result:
	    result_string += "||" + str(row)
	return result_string
