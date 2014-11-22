import sqlite3
from flask import render_template
def show(dt,shopid):
	entry_con=sqlite3.connect('mxwg.db')
	entry_cur=entry_con.cursor()
	entry_cur.execute('select dt,time,use_goodsno,item_value from sale_j where dt=? and shopid=?',(dt,shopid))
	entries=[dict(dt=row[0],time=row[1],use_goodsno=row[2],item_value=row[3]) for row in entry_cur.fetchall()]
	entry_cur.close()
	entry_con.close()
	return entries

'''
       if len(entries) >= 2:
                remsg='slae_j record is over 2'
                return render_template('input.html',remsg=remsg,entries=entries)

'''
