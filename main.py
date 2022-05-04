from flask.wrappers import Response
import pymysql
from app import app
from config import mysql
from flask import flash, request, render_template, redirect, url_for
import string
import random


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/admin')
def adminpage():
	return render_template('admin.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
				error = 'Invalid Credentials. Please try again.'
		else:
				return redirect(url_for('adminpage'))
	return render_template('adminlogin.html', error=error)

@app.route('/add-patient', methods=['GET', 'POST'])
def add_patient():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		if request.method == "POST":
			_json = request.form.to_dict(flat=False)
			name = _json['name']
			house_number = _json['house_number']
			street = _json['street']
			city = _json['city']
			zipcode = _json['zipcode']
			birthdate = _json['birthdate']
			phone_number = _json['phone_number']
			race = _json['race']
			gender = _json['gender']
			marital_status = _json['marital_status']
			blood_group = _json['blood_group']
			insurance_name = _json['insurance_name']
			insurance_number = _json['insurance_number']
			patient_id = [randStr()]

			query = "INSERT INTO patient(patient_id,name,house_number,street,city,zipcode,birthdate,phone_number,race,gender,marital_status,blood_group,insurance_name,insurance_number,TBL_LAST_DATE)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,null)"
			b_data = (patient_id, name, house_number, street, city, zipcode, birthdate, phone_number, race, gender, marital_status, blood_group, insurance_name, insurance_number)
			
			cursor.execute(query, b_data)
			conn.commit()

			return redirect(url_for('get_all_patients'))
			
		elif request.method == "GET":
			return render_template('add_patient.html')

	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit-patient', methods=['GET', 'POST'])
@app.route('/edit-patient/<patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			if request.method == "POST":
				_json = request.form.to_dict(flat=False)
				name = _json['name']
				house_number = _json['house_number']
				street = _json['street']
				city = _json['city']
				zipcode = _json['zipcode']
				birthdate = _json['birthdate']
				phone_number = _json['phone_number']
				race = _json['race']
				gender = _json['gender']
				marital_status = _json['marital_status']
				blood_group = _json['blood_group']
				insurance_name = _json['insurance_name']
				insurance_number = _json['insurance_number']

				print("hqsw")
				query = "UPDATE patient set name=%s,house_number=%s,street=%s,city=%s,zipcode=%s,birthdate=%s,phone_number=%s,race=%s,gender=%s,marital_status=%s,blood_group=%s,insurance_name=%s,insurance_number=%s where patient_id=%s"
				b_data = (name, house_number, street, city, zipcode, birthdate, phone_number, race, gender, marital_status, blood_group, insurance_name, insurance_number, patient_id)
				
				cursor.execute(query, b_data)
				conn.commit()

				return redirect(url_for('get_all_patients'))
			elif request.method == "GET":
				query ="SELECT * from patient where patient_id = %s"
				b_data = (patient_id)
				cursor.execute(query, b_data)
				rows = cursor.fetchall()
				return render_template('edit_patient.html', patient=rows)
		except Exception as e:
			print(e)
			return None
		finally:
			cursor.close() 
			conn.close()

@app.route('/patients', methods=['GET', 'POST'])
@app.route('/patients/<action>/<patient_id>', methods=['GET', 'POST'])
def get_all_patients(action=None,patient_id=None):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

		if request.method == "POST":
			if action == 'delete':
				query = "DELETE from patient where patient_id = %s"
				b_data = (patient_id)
				cursor.execute(query,b_data)
				conn.commit()
				return redirect(url_for('get_all_patients'))
			elif action == 'edit':
				return redirect(url_for('edit_patient',patient_id=patient_id))
			elif action == 'add':
				return redirect(url_for('add_patient'))
		elif request.method == "GET":
			query ="SELECT * from patient"
			cursor.execute(query)
			rows = cursor.fetchall()
			return render_template('patient_table.html', title='Patients', patients=rows)
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

@app.route('/add-doctor', methods=['GET', 'POST'])
def add_doctor():
	print("add")
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		if request.method == "POST":
			_json = request.form.to_dict(flat=False)
			name = _json['name']
			dtype = _json['type']
			speciality = _json['speciality']
			ophone = _json['ophone']
			pphone = _json['pphone']
			doc_id = [randStr()]

			query = "INSERT INTO doctor(doc_id,type,name,speciality,offic_phone,personal_phone,TBL_LAST_DATE) VALUES (%s,%s,%s,%s,%s,%s,null)"
			b_data = (doc_id, dtype, name, speciality, ophone, pphone)
			
			cursor.execute(query, b_data)
			conn.commit()

			return redirect(url_for('get_all_doctors'))
			
		elif request.method == "GET":
			return render_template('add_doctor.html')

	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()


@app.route('/edit-doctor', methods=['GET', 'POST'])
@app.route('/edit-doctor/<doc_id>', methods=['GET', 'POST'])
def edit_doctor(doc_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		if request.method == "POST":
			_json = request.form.to_dict(flat=False)
			name = _json['name']
			dtype = _json['type']
			speciality = _json['speciality']
			ophone = _json['ophone']
			pphone = _json['pphone']

			query = "UPDATE doctor set name = %s,type= %s,speciality=%s,offic_phone=%s,personal_phone=%s where doc_id = %s"
			b_data = (name, dtype, speciality, ophone, pphone, doc_id)
			
			cursor.execute(query, b_data)
			conn.commit()

			return redirect(url_for('get_all_doctors'))
			
		elif request.method == "GET":
			query ="SELECT * from doctor where doc_id = %s"
			b_data = (doc_id)
			cursor.execute(query, b_data)
			rows = cursor.fetchall()
			return render_template('edit_doctor.html', doctor=rows)

	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/doctors', methods=['GET', 'POST'])
@app.route('/doctors/<action>/<doc_id>', methods=['GET', 'POST'])
def get_all_doctors(action=None, doc_id=None):

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

		if request.method == "POST":
			if action == 'delete':
				query = "DELETE from doctor where doc_id = %s"
				b_data = (doc_id)
				cursor.execute(query,b_data)
				conn.commit()
				return redirect(url_for('get_all_doctors'))
			elif action == 'edit':
				return redirect(url_for('edit_doctor',doc_id=doc_id))
			elif action == 'add':
				return redirect(url_for('add_doctor'))

		elif request.method == "GET":
			cursor.execute("SELECT * from doctor")
			rows = cursor.fetchall()
			return render_template('doctor_table.html', title='Doctors', doctors=rows)
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/most-common-disease') 
def get_most_common_dis():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from disease, registration where disease.ICD = registration.ICD group by disease.desc order by count(disease.ICD) desc limit 1;")
		rows = cursor.fetchall()
		return render_template('most_common_dis.html', title='Most Common Disease', diseases=rows)
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/most-popular-doctor') 
def get_most_pop_doc():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from doctor, doctor_registration where doctor.doc_id = doctor_registration.doc_id group by name order by count(doctor.doc_id) desc limit 1;")
		rows = cursor.fetchall()
		return render_template('most_pop_doc.html', title='Most Popular Doctor', doctors=rows)
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

@app.route('/most-popular-hospital') 
def get_most_pop_hos():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * from hospital, doctor_hospital where hospital.hospital_id = doctor_hospital.hospital_id group by name order by count(hospital.hospital_id) desc limit 1;")
		rows = cursor.fetchall()
		return render_template('most_pop_hos.html', title='Most Popular Hospital', hospitals=rows)
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close() 
		conn.close()

if __name__ == "__main__":
    app.run()


