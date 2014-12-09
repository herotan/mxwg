import sqlite3

def showgoods(shopid):
	entry_con=sqlite3.connect('mxwg.db')
	entry_cur=entry_con.cursor()
	entry_cur.execute('select groupno,deptno,shopid,mwid,mwname,vgno,goodsname from shopinfo where shopid=?',(shopid,))
	entries=[dict(groupno=row[0],deptno=row[1],shopid=row[2],mwid=row[3],mwname=row[4],vgno=row[5],goodsname=row[6]) for row in entry_cur.fetchall()]
	entry_cur.close()
	entry_con.close()
	return entries

def showshop():
	entry_con=sqlite3.connect('mxwg.db')
	entry_cur=entry_con.cursor()
	entry_cur.execute('select distinct shopid,mwid,mwname from shopinfo')
	entries=[dict(shopid=row[0],mwid=row[1],mwname=row[2]) for row in entry_cur.fetchall()]
	entry_cur.close()
	entry_con.close()
	return entries


def showgoodscata(shopid,goodsid):
	entry_con=sqlite3.connect('mxwg.db')
	entry_cur=entry_con.cursor()
	entry_cur.execute('select groupno,deptno,goodsno from shopinfo where shopid=? and vgno=?',(shopid,goodsid))
	entries=entry_cur.fetchone()
#	entries=[dict(groupno=row[0],deptno=row[1])for row in entry_cur.fetchone()]
	entry_cur.close()
	entry_con.close()
	return entries
