class Consqlite:
	db_name='mxwg.db'
	conn=''
	cur=''
	def conn(self):
		self.conn=sqlite3.connect(self.db_name)
		cur=self.conn.cursor()
		return conn,cur
	def close(self):
		conn_str.close()
	
