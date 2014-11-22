import sqlite3
class myclass:
	db_name='mxwg.db'
	conn_str=''
	def conn(self):
		conn_str=sqlite3.connect(self.db_name)
		return conn_str
	def close(self):
		conn_str.close()

	

