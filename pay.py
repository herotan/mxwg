import sqlite3
import time

time1=time.strftime('%H:%M:%S')
reqtime=time.strftime('%H%M%S')
listno=1
sublistno=1
pos_id='P001'
cashier_id=1001

pay_reason='p'
pay_type='C'
curren_code='RMB'

flag3='0'
trainflag='1'

def sum(dt,shopid):
	db_name='mxwg.db'
	conn=sqlite3.connect(db_name)
	cur_pay=conn.cursor()
	cur_pay.execute('select sum(item_value) from sale_j where dt=? and shopid=?',(dt,shopid))
	pay_today=cur_pay.fetchone()
	pay_value=pay_today[0]
	cur_pay.close()
	conn.close()
	return pay_value

def pay_ins(dt,shopid,pay_amount):	
	pay_value=pay_amount
	
	reqtime=time.strftime('%H%M%S')
	shopid=str(shopid).upper()
	sheetid=shopid+str(dt)+str(reqtime)
	
	db_name='mxwg.db'
	conn=sqlite3.connect(db_name)
	cur_ins=conn.cursor()
	pay_reason='p'
	pay_type='C'
	curren_code='RMB'
	tranflag=1
	sql_str='Insert into pay_j(sheetid,shopid,dt,time,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,equiv_value,flag3,trainflag) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
	value_str=(sheetid,shopid,dt,time1,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,pay_value,flag3,trainflag)
#	r_pay=cur_ins.execute('Insert into pay_j(shopid,dt,time,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,equiv_value,flag3,trainflag) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(shopid,dt,time1,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,pay_value,flag3,trainflag))
	
	cur_ins.execute(sql_str,value_str)
	conn.commit()
	cur_ins.close()
	conn.close()
	r_pay=value_str
	return r_pay

