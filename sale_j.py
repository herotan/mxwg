import sqlite3
def ins(sql_value):
	 
	conn=sqlite3.connect('mxwg.db')
	cursor=conn.cursor()
	sql_ins='Insert into sale_j(shopid,serialid,dt,time,reqtime,listno,sublistno,pos_id,cashier_id,vgno,goodsno,placeno,groupno,deptno,amount,item_value,disc_value,vipdisc_value,item_type,v_type,disc_type,x,flag1,flag2,flag3,trainflag,price,use_goodsno,sheetid) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
	cursor.execute(sql_ins,sql_value)
	conn.commit()
	cursor.close()

