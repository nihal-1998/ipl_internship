from flask import Flask,render_template,request,make_response,flash
from flask_mysqldb import MySQL
import json
import numpy as np 
from flask_jsonpify import jsonpify
import pandas as pd 
import mysql.connector


app = Flask(__name__)



@app.route('/deleteball')
def deleteball():
	return render_template('deleteball.html')

@app.route('/delete')
def delete():
	return render_template('delete.html')

@app.route('/match')
def add_matches():
	return render_template('add.html')
	

@app.route('/delivery')
def add_delivery():
	return render_template('add_ball.html')	
	

		
@app.route('/add', methods=['POST'])
def add_user():
	database = None
	cursor = None
	try:		
		_id = request.form['inputID']
		_venue = request.form['inputVENUE']
		_date = request.form['inputDATE']
		# validate the received values
		if _id and _venue and _date and request.method == 'POST':
			#do not save password as a plain text
			# save edits
			sql = "INSERT INTO iplmatch(id,date,venue) VALUES(%s, %s, %s)"
			data = (_id, _date, _venue,)
			database=mysql.connector.connect(host='localhost',user='root',passwd='hari1998',database='ipl-ball-by-ball')
			cursor=database.cursor()
			cursor.execute(sql, data)
			database.commit()
			#flash('inserted successfully..')
			return render_template('add.html')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		database.close()
	
		
@app.route('/add_ball', methods=['POST'])
def add_delivery_set():
	database = None
	cursor = None
	try:
		_id = request.form['inputID']
		_batting_team = request.form['inputBATTING_TEAM']
		_bowling_team = request.form['inputBOWLING_TEAM']
		_batsman = request.form['inputBATSMAN']
		_bowler = request.form['inputBOWLER']
		_wide = request.form['inputWIDE_RUNS']
		_noball = request.form['inputNOBALL_RUNS']
		_batsman_runs = request.form['inputBATSMAN_RUNS']
		_total_runs = request.form['inputTOTAL_RUNS']
		_player_diss = request.form['inputPLAYER_DISS']
		_kind = request.form['inputKIND']
		# validate the received values
		if _batting_team and _bowling_team and _batsman and _bowler and _wide and _noball and _batsman_runs and _total_runs and _player_diss and _kind and request.method == 'POST':
			#do not save password as a plain text
			# save edits
			sql = "INSERT INTO ball(match_id,batting_team,bowling_team,batsman,bowler,wide_runs,noball_runs,batsman_runs,total_runs,player_dismissed,dismissal_kind) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			data = (_id, _batting_team,_bowling_team,_batsman,_bowler,_wide,_noball,_batsman_runs,_total_runs,_player_diss,_kind,)
			database=mysql.connector.connect(host='localhost',user='root',passwd='hari1998',database='ipl-ball-by-ball')
			cursor=database.cursor()
			cursor.execute(sql, data)
			database.commit()
			#flash('inserted successfully..')
			return render_template('add_ball.html')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		database.close()
	
@app.route('/delete', methods=['POST'])
def delete_user():
	database = None
	cursor = None
	try:
		_id = request.form['inputID']
		database=mysql.connector.connect(host='localhost',user='root',passwd='hari1998',database='ipl-ball-by-ball')
		cursor=database.cursor()
		sql = "DELETE FROM iplmatch WHERE id=%s"
		data = (_id,)
		cursor.execute(sql,data)
		database.commit()
		#flash('delete successfully..')
		return render_template('delete.html')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		database.close()	
		
	
@app.route('/deleteball', methods=['POST'])
def delete_ball():
	database = None
	cursor = None
	try:
		_id = request.form['inputID']
		database=mysql.connector.connect(host='localhost',user='root',passwd='hari1998',database='ipl-ball-by-ball')
		cursor=database.cursor()
		sql = "DELETE FROM ball WHERE unique_id=%s"
		data = (_id,)
		cursor.execute(sql,data)
		database.commit()
		#flash('delete successfully..')
		return render_template('deleteball.html')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		database.close()		
		
	
		
if __name__ == "__main__":
    app.run(debug=True,threaded=True)	