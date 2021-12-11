import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import random

@app.route('/customers')
def customer():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from smjl_customer")
		rows = cursor.fetchall()
		respone = jsonify(rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

@app.route('/addcustomer', methods=['POST'])
def add_cust():
	try:
		_json = request.json
		_nationality = _json['nationality']
		_email = _json['email']
		_phone = _json['phone']
		_passengers_alongside = _json['passengers_alongside']	
		_emergency_fname=_json['emergency_fname']
		_emergency_lname=_json['emergency_lname']	
		_emergency_phone=_json['emergency_phone']	
		_password = _json['password']
		print(_nationality, _phone, _passengers_alongside)
		_fname = _json['fname']
		_lname = _json['lname']
		_dob = _json['dob']
		_gender = _json['gender']
		_passport_number = _json['passport_number']
		_passport_expiry = _json['passport_expiry']

		if request.method == 'POST':	
			p_id = random.randint(1, 10000)		

			sqlQuery1 = "INSERT INTO smjl_passenger VALUES(%s, %s, %s, STR_TO_DATE(%s, '%M %d %Y'), %s, %s, %s, STR_TO_DATE(%s, '%M %d %Y'))"
			bindData1 = (p_id, _fname, _lname, _dob, _nationality, _gender, _passport_number, _passport_expiry)
			print(p_id)
			sqlQuery = "INSERT INTO smjl_customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			bindData = (p_id, _email, _phone, _nationality, _passengers_alongside, _emergency_fname, _emergency_lname, _emergency_phone, _password)
		
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery1, bindData1)
			cursor.execute(sqlQuery, bindData)
			conn.commit()

			respone = jsonify('Customer and Passenger added successfully!')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



if __name__ == "__main__":
    app.run()