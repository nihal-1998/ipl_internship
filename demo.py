from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import json
import numpy as np 
from flask_jsonpify import jsonpify
import pandas as pd 
#import matplotlib.pyplot as plt
#from sklearn import preprocessing,cross_validation
#from sklearn import linear_model
#from subprocess import check_output


app = Flask(__name__)

import mysql.connector
database=mysql.connector.connect(host='localhost',user='root',passwd='hari1998',database='ipl-ball-by-ball')
cursor=database.cursor()



query2 = "select * from iplmatch"
#cursor.execute(query2)
#table_ = cursor.fetchall()
match_data = pd.read_sql(query2,database)

query="select * from ball"
#cursor.execute(query)
#table_rows = cursor.fetchall()
delivery_data = pd.read_sql(query,database)

database.commit()

#delivery_data=pd.read_csv("deliveries_till_2019.csv")
#match_data=pd.read_csv("matches_till_2019.csv")

@app.route('/batVsBall')
def my_form():
		
		return render_template('batvsball.html')




@app.route('/batVsBall', methods=['POST'])		
def home():
   #         print(delivery_data)
				name = request.form['batsman']
				name2 = request.form['bowler']
				batsman_data_1=delivery_data[(delivery_data.batsman==name)&(delivery_data.bowler==name2)]
				balls=len(batsman_data_1[(batsman_data_1.wide_runs==0)&(batsman_data_1.noball_runs==0)])
		#	out = len(batsman_data_1[batsman_data_1.player_dismissed==name].index)
				runs = batsman_data_1.batsman_runs.sum()
				outss=0
				for outs in batsman_data_1.player_dismissed:
						if outs!="\r":
								outss = outss + 1
					    
			#out = batsman_data_1[batsman_data_1.player_dismissed==name]
			#out_ = len(out.index)
			#notnull().astype('int').sum()
			#	out = batsman_data_1.player_dismissed.notnull().astype('int').sum()
				run1 = np.asarray(runs)
				df_list = run1.tolist()
				JSONP_data = jsonpify(df_list)
			
				balls1 = np.asarray(balls)
				df_list1 = balls1.tolist()
				JSONP_data1 = jsonpify(df_list1)
			
				out1 = np.asarray(outss)
				df_list2 = out1.tolist()
				JSONP_data2 = jsonpify(df_list2)
			
				str1 = (run1/balls1)*100
				df_list3 = str1.tolist()
				JSONP_data3 = jsonpify(df_list3)
				print(JSONP_data)
#			 answer = [JSONP_data,JSONP_data1,JSONP_data2]
				answer = {'runs':df_list,'balls':df_list1,'out':df_list2,'strike rate':df_list3}
			
#			d = json.dumps(d)
				ds = np.asarray(delivery_data)
				dds = ds.tolist()
				return jsonpify(answer)
				#jsonpify(answer)
			
			
@app.route('/batVsVenue')
def my_form_1():
		return render_template('batvsvenue.html')
			
@app.route('/batVsVenue', methods=['POST'])		
def home_1():

			batting_first = list()
			name = request.form['batsman']
			name2 = request.form['venue']
			batsman_data = delivery_data[(delivery_data.batsman==name)]
			for venue in match_data.venue.unique():
					matches=match_data[(match_data.venue==venue)].id
# 			        print(matches)
					runs=0
					balls=0
					for match in matches:
							runs = 0
							balls = 0
							t=batsman_data[batsman_data.match_id==match].batsman_runs.sum()
							runs=runs+t
#           				print(runs)
							balls=balls+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.wide_runs==0)&(batsman_data.noball_runs==0)])
							batting_first=batting_first+[[venue,1,balls,t]]
			batvs_venue = pd.DataFrame(batting_first,columns=['venue','batting first','balls','runs'])
			batsman_venue = batvs_venue[batvs_venue.balls != 0]
			abc = batsman_venue[batsman_venue.venue==name2]
#			venue_runs = pd.DataFrame(datatoss[(datatoss.venue==name3)])
			total_runs = abc.runs.sum()
			h_cen = 0
			cen = 0
			num_inni = len(abc.index)
			for fif in abc.runs:
					if((fif>49) & (fif<100)):
							h_cen = h_cen+1
					elif(fif>99):
							cen = cen+1
        
			sti = (total_runs/abc.balls.sum())*100 
			sti1 = np.asarray(sti)
			df_list2 = sti1.tolist()
			
			
			h_cen1 = np.asarray(h_cen)
			df_list1 = h_cen1.tolist()
			
			
			cen1 = np.asarray(cen)
			df_list = cen1.tolist()
			
			total_runs1 = np.asarray(total_runs)
			df_list3 = total_runs1.tolist()
			
			num_inni1 = np.asarray(num_inni)
			df_list4 = num_inni1.tolist()
		  
		     
			answer = {'centuries':df_list,'half-centuries':df_list1,'strike rate':df_list2,'total run':df_list3 ,'innings':df_list4}
			
			bat_vs_venue = abc.drop(columns=['batting first'])
#			bat_array = bat_vs_venue.reset_index().values
			bat_answer = bat_vs_venue.values.tolist()
			return jsonpify(answer)
		
			
if __name__=='__main__':
	app.run	(debug=True)