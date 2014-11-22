sqlite3 mxwg.db "select time,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,equiv_value,flag3,trainflag from pay_j where sheetid='"$1"'" > receive_pay/$1.plt

echo "load from receive_pay/$1.plt delimiter '|'
insert into pay_j(time,reqtime,listno,sublistno,pos_id,cashier_id,pay_reason,pay_type,curren_code,pay_value,equiv_value,flag3,trainflag);"|dbaccess $2@$3

