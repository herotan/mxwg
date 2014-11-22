from flask import Flask,render_template,url_for,request,redirect,make_response,url_for,session,make_response
import os,string
import sqlite3
import datetime,time

app=Flask(__name__)

shopid='j10b'
instance_name='onspj10b2'
posdb_name='sppos1'


@app.route('/input/',methods=['GET','POST'])
def input():

	username=request.cookies.get('username')
	password=request.cookies.get('password')
	shopid=request.cookies.get('shopid')
	ip=request.cookies.get('ip')
	if not username:
		return redirect('/')	
	if request.method=='POST':
		username=request.cookies.get('username')
		password=request.cookies.get('password')
		shopid=request.cookies.get('shopid')
		ip=request.cookies.get('ip')
		if not username:
			return redirect('/login/')	
						
#		shopid='j10b'
		instance_name='onspj10b2'
		posdb_name='sppos1'
		
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

		sales_amount=float(sales_amount_input)*100
        	
		item_value=sales_amount
		price=item_value
				
		if groupno==56:
			deptno='561302'
		else:
			deptno='580108'
		
		sheetid=shopid+dt+reqtime
				
		conn=sqlite3.connect('mxwg.db')
		cursor=conn.cursor()
        	sql_ins='Insert into sale_j(shopid,serialid,dt,time,reqtime,listno,sublistno,pos_id,cashier_id,vgno,goodsno,placeno,groupno,deptno,amount,item_value,disc_value,vipdisc_value,item_type,v_type,disc_type,x,flag1,flag2,flag3,trainflag,price,use_goodsno,sheetid) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
		sql_value=(shopid,1001,dt,time1,reqtime,listno,sublistno,pos_id,cashier_id,vgno,goodsno,placeno,groupno,deptno,amount,item_value,disc_value,vipdisc_value,item_type,v_type,disc_type,x,flag1,flag2,flag3,trainflag,price,use_goodsno,sheetid)
        	cursor.execute(sql_ins,sql_value)
		conn.commit()
		cursor.close()
		
		cur_pay=conn.cursor()
		cur_pay.execute('select sum(item_value) from sale_j where dt=?',(dt,))
		pay_today=cur_pay.fetchone()
		pay_value=pay_today[0]
		cur_pay.close()
		
#		cur_ins=conn.cursor()
#		pay_reason='p'
#		pay_type='C'
#		curren_code='RMB'
		
#		cur_ins.execute('Insert into pay_j(dt,time,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,equiv_value,flag3,trainflag) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(dt,time,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,pay_value,flag3,trainflag))
#		cur_ins.close()
		
		remsg=os.popen('sh upload.sh '+sheetid+' '+posdb_name+' '+instance_name).read()
		return render_template("input.html",username=username,shopid=shopid,goodsid=goodsid,sales_amount=sales_amount,remsg=remsg,time1=time1,dt=dt,pay_value=pay_value,ip=ip)
		cursor.close()
		conn.close()
	else:
		return render_template("input.html",username=username,shopid=shopid)

app.secret_key= 'c\xe5\xcc#\xd9\xd1\xaf*b$\x0b\xdd=\x0bQ\\Y608D`\x9dQ'
@app.route('/',methods=['GET','POST'])
def login():
        if request.method=='POST':
               
		ip=request.headers.get('X-Real-Ip', request.remote_addr)
		
		username=request.form.get('username')
		password=request.form.get('password')
		shopid=request.form.get('shopid')
		conn=sqlite3.connect('mxwg.db')
		cur_login=conn.cursor()
		sql_login='select username,password,shopid from user where username=? and password=? and shopid=?'
		login_value=(username,password,shopid)
		cur_login.execute(sql_login,login_value)
		row=cur_login.fetchone()
	        
		if row==None:
			msg='Login Failed!'
                	return render_template("login.html",username=username,password=password,shopid=shopid,msg=msg)
                else:
			redirect_to_index = redirect('/input/')
			response = make_response(redirect_to_index)    
			response.set_cookie('username',value=username,max_age=600)
			response.set_cookie('password',value=password,max_age=600)
			response.set_cookie('shopid',value=shopid,max_age=600)
			response.set_cookie('ip',value=ip,max_age=600)
			return response
	
#			return redirect('/set_cookie')
#                       session['username']=username
#			session['shopid']=shopid
#			session['password']=password
			
			msg='Login OK'
#                       return redirect('/input/')
		
		cur_login.close()
		conn.close()

        else:
                return render_template("login.html")




if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0')

