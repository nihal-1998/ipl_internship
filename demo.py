from flask import Flask,render_template,request,make_response
from flask_mysqldb import MySQL
import json
import numpy as np 
from flask_jsonpify import jsonpify
import pandas as pd 
from gevent.pywsgi import WSGIServer
from gevent import monkey
#import matplotlib.pyplot as plt
#from sklearn import preprocessing,cross_validation
#from sklearn import linear_model
#from subprocess import check_output

#monkey.patch_all()

app = Flask(__name__)

#import mysql.connector
#database=mysql.connector.connect(host='localhost',user='root',passwd='hari1998',database='ipl-ball-by-ball')
#cursor=database.cursor()



#query2 = "select * from iplmatch"
#cursor.execute(query2)
#table_ = cursor.fetchall()
#match_data = pd.read_sql(query2,database)

#query="select * from ball"
#cursor.execute(query)
#table_rows = cursor.fetchall()
#delivery_data = pd.read_sql(query,database)

#database.commit()

delivery_data=pd.read_csv("deliveries_till_2019.csv")
delivery_data = delivery_data.replace(np.nan, '', regex=True)
match_data=pd.read_csv("matches_till_2019.csv")


@app.route('/')
def website_home():
		return render_template('tem.html')

@app.route('/batVsBall')
def my_form():
		
		return render_template('imagebat.html')




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
				for outs in batsman_data_1.dismissal_kind:
						if ((outs!="")&(outs!="run out")):
							
								outss = outss + 1
					    
			#out = batsman_data_1[batsman_data_1.player_dismissed==name]
			#out_ = len(out.index)
			#notnull().astype('int').sum()
			#	out = batsman_data_1.player_dismissed.notnull().astype('int').sum()
				run1 = np.asarray(runs)
				df_list = run1.tolist()
				#JSONP_data = jsonpify(df_list)
			
				balls1 = np.asarray(balls)
				df_list1 = balls1.tolist()
		#		JSONP_data1 = jsonpify(df_list1)
			
				out1 = np.asarray(outss)
				df_list2 = out1.tolist()
		#		JSONP_data2 = jsonpify(df_list2)
			
				str1 = (run1/balls1)*100
				df_list3 = str1.tolist()
		#		JSONP_data3 = jsonpify(df_list3)
		#		print(JSONP_data)
#			 answer = [JSONP_data,JSONP_data1,JSONP_data2]
				answer = {'runs':df_list,'balls':df_list1,'out':df_list2,'strike rate':df_list3}
			
#			d = json.dumps(d)
		#		ds = np.asarray(delivery_data)
		#		dds = ds.tolist()
		#		response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
		#		an=response
				df = pd.DataFrame(answer,index=['stats'])
				return render_template('imagebat.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,bowler=name2,vs="Vs")
				#jsonpify(answer)


@app.route('/ballVsVenue')
def my_form_2():
		return render_template('imageball.html')

@app.route('/ballVsVenue', methods=['POST'])		
def home_2():
			bowling_first = list()
			name = request.form['bowler']
			name2 = request.form['venue']
			bowler_data = delivery_data[(delivery_data.bowler==name)]
			match_data1 = match_data[(match_data.venue==name2)]
			for venue in match_data1.venue.unique():
					matches=match_data1[(match_data1.venue==venue)].id
					wk=0
					runs=0
					balls = 0
					for match in matches:
							wk=0
							runs=0
							balls = 0
#							ta=bowler_data[(bowler_data.match_id==match)&(bowler_data.dismissal_kind!='run out\r')&(bowler_data.dismissal_kind!='\r')].player_dismissed.sum()
							for wks in bowler_data[(bowler_data.match_id==match)&(bowler_data.dismissal_kind!='run out')&(bowler_data.dismissal_kind!='')].player_dismissed:
								if wks!='':
									wk = wk+1
							t=bowler_data[bowler_data.match_id==match].total_runs.sum()
							balls=balls+len(bowler_data[(bowler_data.match_id==match)&(bowler_data.wide_runs==0)&(bowler_data.noball_runs==0)])
							bowling_first=bowling_first+[[venue,t,wk,balls]]
			bowvs_venue = pd.DataFrame(bowling_first,columns=['venue','runs','wickets','balls'])
			bowler_venue = bowvs_venue[bowvs_venue.balls != 0]
			abc = bowler_venue[bowler_venue.venue==name2]
			
			
			inning = len(abc.index)
			wick = abc.wickets.sum()
			runs = abc.runs.sum()
			balls1 = abc.balls.sum()
			over = (balls1/6)
			economy = (runs/over)
			average = (runs/wick)
         
			num_inni = np.asarray(inning)
			df_list1 = num_inni.tolist()

			num_runs = np.asarray(runs)
			df_list2 = num_runs.tolist()

			num_wickets = np.asarray(wick)
			df_list3 = num_wickets.tolist()

			num_average = np.asarray(average)
			df_list4 = num_average.tolist()

			num_economy = np.asarray(economy)
			df_list5 = num_economy.tolist()
			
		#	ball_answer = abc.values.tolist()
		
			answer = {'number of innings':df_list1,'total runs':df_list2,'total wickets':df_list3,'average':df_list4 ,'economy':df_list5}
			#response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
			#an=response
			df = pd.DataFrame(answer,index=['stats'])
			return render_template('imageball.html',tables=[df.to_html(classes='data')], titles=df.columns.values,bowler=name,venue1=name2,vs="Vs")
			




			
@app.route('/batVsVenue')
def my_form_1():
		return render_template('batvenue.html')
			
@app.route('/batVsVenue', methods=['POST'])		
def home_1():

			batting_first = list()
			name = request.form['batsman']
			name2 = request.form['venue']
			batsman_data = delivery_data[(delivery_data.batsman==name)]
			match_data1 = match_data[(match_data.venue==name2)]
			for venue in match_data1.venue.unique():
					matches=match_data1[(match_data1.venue==venue)].id
# 			        print(matches)
					runs=0
					balls=0
					out = 0
					for match in matches:
							runs = 0
							balls = 0
							out = 0
							avg = batsman_data[batsman_data.match_id==match]
							t=batsman_data[batsman_data.match_id==match].batsman_runs.sum()
							runs=runs+t
#           				print(runs)
							out = out+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.player_dismissed==name)])
							balls=balls+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.wide_runs==0)&(batsman_data.noball_runs==0)])
							batting_first=batting_first+[[venue,1,balls,t,out]]
			batvs_venue = pd.DataFrame(batting_first,columns=['venue','batting first','balls','runs','out'])
			batsman_venue = batvs_venue[batvs_venue.balls != 0]
			abc = batsman_venue[batsman_venue.venue==name2]
#			venue_runs = pd.DataFrame(datatoss[(datatoss.venue==name3)])
			total_runs = abc.runs.sum()
			outss = abc.out.sum()
			average = (total_runs/outss)
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
			
			num_out = np.asarray(outss)
			df_list5 = num_out.tolist()
			
			num_average = np.asarray(average)
			df_list6 = num_average.tolist()
		  
		  
		     
			answer = {'centuries':df_list,'half-centuries':df_list1,'strike rate':df_list2,'total run':df_list3 ,'innings':df_list4,'outs' :df_list5,'average':df_list6}
			
	#		bat_vs_venue = abc.drop(columns=['batting first'])
#			bat_array = bat_vs_venue.reset_index().values
		#	bat_answer = abc.values.tolist()
			
		#	response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
		#	an=response
			df = pd.DataFrame(answer,index=['stats'])
			return render_template('batvenue.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,venue1=name2,vs="Vs")
			
		

@app.route('/batVsBallInvVenue')
def my_form_3():
		return render_template('all.html')
			
@app.route('/batVsBallInvVenue', methods=['POST'])		
def home_3():
			batting_first = list()
			name = request.form['batsman']
			name2 = request.form['bowler']
			name3 = request.form['venue']
			batsman_data_1=delivery_data[(delivery_data.batsman==name)&(delivery_data.bowler==name2)]
			match_data1 = match_data[(match_data.venue==name3)]
			for venue in match_data1.venue.unique():
					matches=match_data1[(match_data1.venue==venue)].id
# 			        print(matches)
					runs=0
					balls=0
					out = 0
					for match in matches:
							runs = 0
							balls = 0
							out = 0
							avg = batsman_data_1[batsman_data_1.match_id==match]
							t=batsman_data_1[batsman_data_1.match_id==match].batsman_runs.sum()
							runs=runs+t
#           				print(runs)
							out = out+len(batsman_data_1[(batsman_data_1.match_id==match)&(batsman_data_1.player_dismissed==name)&(batsman_data_1.dismissal_kind!='run out')])
							balls=balls+len(batsman_data_1[(batsman_data_1.match_id==match)&(batsman_data_1.wide_runs==0)&(batsman_data_1.noball_runs==0)])
							batting_first=batting_first+[[venue,1,balls,t,out]]
			batvs_venue = pd.DataFrame(batting_first,columns=['venue','batting first','balls','runs','out'])
			batsman_venue = batvs_venue[batvs_venue.balls != 0]
			abc = batsman_venue[batsman_venue.venue==name3]
			runs = abc.runs.sum()
			balls = abc.balls.sum()
			outs = abc.out.sum()
			strike = (runs/balls)*100
			
			run1 = np.asarray(runs)
			df_list = run1.tolist()
			
			ball1 = np.asarray(balls)
			df_list1 = ball1.tolist()
			
			out1 = np.asarray(outs)
			df_list2 = out1.tolist()
			
			str1 = np.asarray(strike)
			df_list3 = str1.tolist()
			
			
			answer = {'runs':df_list,'balls':df_list1,'out':df_list2,'strike rate':df_list3}
			#an = jsonpify(answer)
			#response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
			#an=response
			df = pd.DataFrame(answer,index=['stats'])
			return render_template('all.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,bowler=name2,venue1=name3,vs="Vs",In="In")
			

@app.route('/batVsteam')
def my_form_4():
		return render_template('batvsteam.html')
			
@app.route('/batVsteam', methods=['POST'])		
def home_4():
			batting_first = list()
			name = request.form['batsman']
			name2 = request.form['team']
			batting_first=list()
			batsman_data = delivery_data[(delivery_data.batsman==name)&(delivery_data.bowling_team==name2)]
			balls=len(batsman_data[(batsman_data.wide_runs==0)&(batsman_data.noball_runs==0)])
			runs1 = batsman_data.batsman_runs.sum()
			out = len(batsman_data[(batsman_data.player_dismissed==name)])
			innings = len(batsman_data.match_id.unique())
			for ids in batsman_data.match_id.unique():
				runs=0
				t=batsman_data[batsman_data.match_id==ids].batsman_runs.sum()
				runs=runs+t
				batting_first=batting_first+[[runs]]
			df=pd.DataFrame(data=batting_first,columns=['runs'])
		#	for ids in match_data.id.unique():
		#			runs=0
		#			balls=0
		#			out=0
		#			team1 = batsman_data.bowling_team[batsman_data.match_id==ids].unique()
            #  print(batsman_data)
            #print(ids1)
            #team1 = match_data[match_data.id==ids1].team1
            #team2 = match_data[match_data.id==ids1].team2
			#		t=batsman_data[batsman_data.match_id==ids].batsman_runs.sum()
			#		runs=runs+t
			#		out = out+len(batsman_data[(batsman_data.match_id==ids)&(batsman_data.player_dismissed==name)])
			#		balls=balls+len(batsman_data[(batsman_data.match_id==ids)&(batsman_data.wide_runs==0)&(batsman_data.noball_runs==0)])
			#		batting_first=batting_first+[[team1,1,balls,runs,out]]


			#df=pd.DataFrame(data=batting_first,columns=['team1','batting_first','balls','runs','out'])
			#datatoss = df.drop(['batting_first'],axis = 1) 
			#abc = datatoss[datatoss.balls!=0] 
			#abc1 = abc[abc.team1==name2]
			#runs = abc1.runs.sum()
			#balls = abc1.balls.sum()
			#outs = abc1.out.sum()
			strike = (runs1/balls)*100
			average = (runs1/out)
			h_cen = 0
			cen = 0
			for fif in df.runs:
					if((fif>49) & (fif<100)):
							h_cen = h_cen+1
					elif(fif>99):
							cen = cen+1
			
			sti1 = np.asarray(strike)
			df_list2 = sti1.tolist()
			
			
			h_cen1 = np.asarray(h_cen)
			df_list1 = h_cen1.tolist()
			
			
			cen1 = np.asarray(cen)
			df_list = cen1.tolist()
			
			total_runs1 = np.asarray(runs1)
			df_list3 = total_runs1.tolist()
			
			num_inni1 = np.asarray(innings)
			df_list4 = num_inni1.tolist()
			
			num_out = np.asarray(out)
			df_list5 = num_out.tolist()
			
			num_average = np.asarray(average)
			df_list6 = num_average.tolist()
			
			answer = {'centuries':df_list,'half-centuries':df_list1,'strike rate':df_list2,'total run':df_list3 ,'innings':df_list4,'outs' :df_list5,'average':df_list6}
			
			#response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
			df = pd.DataFrame(answer,index=['stats'])
			return render_template('batvsteam.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,team1=name2,vss ="Vs")


@app.route('/ballVsteam')
def my_form_5():
		return render_template('ballvsteam.html')

@app.route('/ballVsteam', methods=['POST'])		
def home_5():
			bowling_first = list()
			name = request.form['bowler']
			name2 = request.form['team']
			bowler_data = delivery_data[(delivery_data.bowler==name)&(delivery_data.batting_team==name2)]
			wk = 0
			for wks in bowler_data[(bowler_data.dismissal_kind!='run out')&(bowler_data.dismissal_kind!='')].player_dismissed:
								if wks!='':
									wk = wk+1
			t=bowler_data.total_runs.sum()
			balls=len(bowler_data[(bowler_data.wide_runs==0)&(bowler_data.noball_runs==0)])
			innings = len(bowler_data.match_id.unique())
			
			over = (balls/6)
			economy = (t/over)
			average = (t/wk)

			num_inni = np.asarray(innings)
			df_list1 = num_inni.tolist()

			num_runs = np.asarray(t)
			df_list2 = num_runs.tolist()

			num_wickets = np.asarray(wk)
			df_list3 = num_wickets.tolist()

			num_average = np.asarray(average)
			df_list4 = num_average.tolist()

			num_economy = np.asarray(economy)
			df_list5 = num_economy.tolist()
			
			#ball_answer = abc.values.tolist()
		
			answer = {'number of innings':df_list1,'total runs':df_list2,'total wickets':df_list3,'average':df_list4 ,'economy':df_list5}
			df = pd.DataFrame(answer,index=['stats'])
			return render_template('ballvsteam.html',tables=[df.to_html(classes='data')], titles=df.columns.values,bowler=name,team1=name2,vs="Vs")
			
			
if __name__=='__main__':
     # http = WSGIServer(('', 9000), app.wsgi_app) 
     # Serve your application
     # http.serve_forever()
	 app.run	(debug=True,threaded=True)
