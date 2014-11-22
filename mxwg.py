from flask import Flask,render_template,url_for,request,redirect,make_response,url_for,make_response
import os,string
import sqlite3
import time
import entry,pay,sale_j,shopinfo

app=Flask(__name__)


@app.route('/input/',methods=['GET','POST'])
def input():
	username=request.cookies.get('username')
	password=request.cookies.get('password')
	shopid=request.cookies.get('shopid')
	ip=request.cookies.get('ip')
	if not username:
		return redirect('/')

	posdb_name=str(request.cookies.get('posdb_name'))
	instance_name=str(request.cookies.get('instance_name'))

	dt=time.strftime('%Y%m%d')

	if request.method=='POST':
		
		dt=time.strftime('%Y%m%d')
		time1=time.strftime('%H:%M:%S')
		reqtime=time.strftime('%H%M%S')
		listno=1
		sublistno=1
		pos_id='P001'
		cashier_id=1001
		placeno=000000
		amount=1
		disc_value=0
		vipdisc_value=0
		item_type='a'
		v_type='8'
		disc_type='n'
		x=1
		flag1='0'
		flag2='0'
		flag3='0'
		trainflag='1'
		
		goodsid=request.form.get('goodsid')
		vgno=goodsid
		use_goodsno=goodsid
		if goodsid=='7107710':
			goodsno='2171077100011'
			groupno=56
		else:
			goodsno='2171077000014'
			groupno=58
	    	sales_amount_input=request.form.get('sales_amount')

		if sales_amount_input=='':
			return render_template('input.html')

		sales_amount=float(sales_amount_input)/100
        	
		item_value=sales_amount
		price=item_value
				
		if groupno==56:
			deptno='561302'
		else:
			deptno='580108'
		
		sheetid=str(shopid)+str(dt)+str(reqtime)
		
		sql_value=(shopid,1001,dt,time1,reqtime,listno,sublistno,pos_id,cashier_id,vgno,goodsno,placeno,groupno,deptno,amount,item_value,disc_value,vipdisc_value,item_type,v_type,disc_type,x,flag1,flag2,flag3,trainflag,price,use_goodsno,sheetid)
		sale_j.ins(sql_value)
	
		pay_value=pay.sum(dt,shopid)
		entries=entry.show(dt,shopid)
		
		remsg=os.popen('sh upload_sale.sh '+sheetid+' '+posdb_name+' '+instance_name).read()
		return render_template("input.html",username=username,shopid=shopid,goodsid=goodsid,sales_amount=sales_amount,remsg=remsg,time1=time1,dt=dt,pay_value=pay_value,ip=ip,entries=entries)
		cursor.close()
		conn.close()
	else:	
		entries=entry.show(dt,shopid)
		pay_value=pay.sum(dt,shopid)
		
		goodsinfo=shopinfo.show(shopid)
		
		return render_template("input.html",goodsinfo=goodsinfo,username=username,shopid=shopid,pay_value=pay_value,entries=entries)

@app.route('/payfor/',methods=['GET','POST'])
def payfor():
	username=request.cookies.get('username')
	password=request.cookies.get('password')
	shopid=request.cookies.get('shopid')
	ip=request.cookies.get('ip')
	if not username:
		return redirect('/')
	username=request.cookies.get('username')
	password=request.cookies.get('password')
	shopid=request.cookies.get('shopid')
	ip=request.cookies.get('ip')
	posdb_name=str(request.cookies.get('posdb_name'))
	instance_name=str(request.cookies.get('instance_name'))

	dt=time.strftime('%Y%m%d')
	reqtime=time.strftime('%H%M%S')
	sheetid=str(shopid)+str(dt)+str(reqtime)

	if request.method=='POST':
		pay_amount=request.form.get('pay_amount')
		if pay_amount=='':
			remsg='pay_amount is not null.'
			return render_template('pay_input.html',username=username,shopid=shopid,pay_amount=pay_amount,dt=dt,ip=ip,remsg=remsg)

		pay_amount=float(pay_amount)/100
	
		pay_value=pay.sum(dt,shopid)
		entries=entry.show(dt,shopid)

		r_pay=pay.pay_ins(dt,shopid,pay_amount)
			
		remsg=os.popen('sh upload_pay.sh '+sheetid+' '+posdb_name+' '+instance_name).read()
		return render_template("pay_input.html",username=username,shopid=shopid,pay_amount=pay_amount,dt=dt,pay_value=pay_value,ip=ip,entries=entries,r_pay=r_pay,remsg=remsg)
	else:	
		entries=entry.show(dt,shopid)
		pay_value=pay.sum(dt,shopid)
		return render_template("pay_input.html",username=username,shopid=shopid,pay_value=pay_value,entries=entries)



@app.route('/',methods=['GET','POST'])
def login():
	if request.method=='POST':
		ip=request.headers.get('X-Real-Ip', request.remote_addr)
		ipmask=ip[0:7]	
#		hdip='10.228.'
		hdip='158.143'
		username=request.form.get('username')
		password=request.form.get('password')
		shopid=request.form.get('shopid')
		conn=sqlite3.connect('mxwg.db')
		cur_login=conn.cursor()
		sql_login='select username,password,shopid,ip,posdb_name,instance_name from user where username=? and password=? and shopid=? and (substr(ip,1,7)=? or ?=?)'
		login_value=(username,password,shopid,ipmask,ipmask,hdip)
		cur_login.execute(sql_login,login_value)
		row=cur_login.fetchone()
#		posdb_name=str(row[4])
#		instance_name=str(row[5])

		cur_login.close()
		conn.close()
		if row==None:
			msg='Login Failed!'
			return render_template("login.html",username=username,shopid=shopid,msg=msg,ip=ip)
		else:
			redirect_to_index = redirect('/input/')
			response = make_response(redirect_to_index)    
			response.set_cookie('username',value=username,max_age=600)
			response.set_cookie('password',value=password,max_age=600)
			response.set_cookie('shopid',value=shopid,max_age=600)
			response.set_cookie('ip',value=ip,max_age=600)
#			response.set_cookie('posdb_name',value=posdb_name,max_age=600)
#			response.set_cookie('instance_name',value=instance_name,max_age=600)
			return response
	else:	
		return render_template('login.html')

#@app.loginout('/loginout/',methods=['POST'])
#def loginout():
#	response = make_response(redirect('/loginout/')
#	response.delete_cookie('username')
#	response.delete_cookie('password')
#	response.delete_cookie('shopid')
#	response.delete_cookie('posdb_name')
#	response.delete_cookie('instance_name')



if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0')

