import sqlite3

def show(dt,shopid):
	entry_con=sqlite3.connect('mxwg.db')
	entry_cur=entry_con.cursor()
	entry_cur.execute('select groupno,deptno,shopid,mwid,mwname,goodsno,goodsname from shopinfo where shopid=?',(shopid,))
	entries=[dict(groupno=row[0],deptno=row[1],shopid=row[2],mwid=row[3],mwname=row[4],goodsno=row[5],goodsname=row[6]) for row in entry_cur.fetchall()]
	entry_cur.close()
	entry_con.close()
	return entries

