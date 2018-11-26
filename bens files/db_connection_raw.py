
import psycopg2


class DBConnection:


	conn_string = "host='localhost' dbname='treeofknowledge' user='postgres' password='plop'"


	def __init__(self, conn_string=None):
		if conn_string is not None:
			self.conn_string = conn_string
		conn = psycopg2.connect(self.conn_string)
		self.cursor = conn.cursor()


	def get_all_data_points(self):
		cur = self.cursor
		cur.execute("SELECT * FROM data_points;")
		for row in cur:
			print(row)
