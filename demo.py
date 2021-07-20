from flask import Flask,render_template,request,make_response,after_this_request
#from flask_mysqldb import MySQL
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
match_data=pd.read_csv("match_data_till_2019_final.csv")

T20_delivery_data=pd.read_csv("international t20 ballbyball.csv")
T20_delivery_data = T20_delivery_data.replace(np.nan, '', regex=True)
T20_match_data=pd.read_csv("T20_match_data.csv")


BBL_delivery_data=pd.read_csv("BBL_BallByBall_data.csv")
BBL_delivery_data = BBL_delivery_data.replace(np.nan, '', regex=True)
BBL_match_data=pd.read_csv("BBL_Match_data.csv")

ddl_PlayerMaster = pd.read_csv("ddlPlayerMasterData.csv")
ddl_TeamMaster = pd.read_csv("ddlTeamMasterData.csv")
ddl_VenueMaster = pd.read_csv("ddlVenueMasterData.csv")


#@app.route('/home')
#def website_home_1():
     
#		return render_template('iplplayerHome.html',playerMastervelue=ddl_PlayerMaster.value.tolist(),playerMasterName=ddl_PlayerMaster.name.tolist())

@app.route('/')
def website_home():
		#print(ddl_PlayerMaster.value.tolist())
		return render_template('iplplayerHome.html',playerMastervelue=ddl_PlayerMaster.value.tolist(),playerMasterName=ddl_PlayerMaster.name.tolist(),teamMaster=ddl_TeamMaster.value.tolist(),venueMaster=ddl_VenueMaster.value.tolist())

#@app.route('/batVsBall')
#def my_form():
		
#		return render_template('imagebat.html')


@app.route('/batVsBall', methods=['GET','POST'])		
def home():
				req = request.get_json()
				#print(req)

   #        print(delivery_data)

				name = req["batsmanName"]
				leaguage = req["leaguageName"]
				name2 = req["bowlerName"]
				#print(name)
				#print(leaguage)
				#print(name2)
				if(leaguage=='IPL'):
					#print('inipl')
					batsman_data_1=delivery_data[(delivery_data.batsman==name)&(delivery_data.bowler==name2)]
				elif (leaguage=='T20i'):
					#print('int20i')
					batsman_data_1=T20_delivery_data[(T20_delivery_data.batsman==name)&(T20_delivery_data.bowler==name2)]
				elif (leaguage=='BBL'):
					#print('inbbl')
					batsman_data_1=BBL_delivery_data[(BBL_delivery_data.batsman==name)&(BBL_delivery_data.bowler==name2)]
				if(leaguage!='IPL'):
					balls=len(batsman_data_1[(batsman_data_1.extra_runs==0)])
				else:
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
				if(balls1==0):
					df_list3 = df_list1
		#		JSONP_data3 = jsonpify(df_list3)
		#		print(JSONP_data)
#			 answer = [JSONP_data,JSONP_data1,JSONP_data2]
				answer = {'runs':df_list,'balls':df_list1,'out':df_list2,'strikeRate':df_list3}
				#print(answer)
#			d = json.dumps(d)
		#		ds = np.asarray(delivery_data)
		#		dds = ds.tolist()
		#		response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
		#		an=response
				#df = pd.DataFrame(answer,index=['stats'])
				#return render_template('imagebat.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,bowler=name2,vs="Vs")
				return jsonpify(answer)


#@app.route('/ballVsVenue')
#def my_form_2():
#		return render_template('imageball.html')

@app.route('/ballVsVenue', methods=['POST'])		
def home_2():
				req = request.get_json()
				#print(req)

   #        print(delivery_data)

				name = req["bowlerName"]
				leaguage = req["leaguageName"]
				name2 = req["venue"]
				#print(name)
				#print(leaguage)
				#print(name2)
				if(leaguage=='IPL'):
					#print('inipl')
					bowler_data= delivery_data[(delivery_data.bowler==name)]
					match_data1 = match_data[(match_data.venue==name2)]
				elif (leaguage=='T20i'):
					#print('int20i')
					bowler_data=T20_delivery_data[(T20_delivery_data.bowler==name)]
					match_data1 = T20_match_data[(T20_match_data.venue==name2)]
				elif (leaguage=='BBL'):
					bowler_data=BBL_delivery_data[(BBL_delivery_data.bowler==name)]
					match_data1 = BBL_match_data[(BBL_match_data.venue==name2)]
						

				bowling_first = list()
				#name = request.form['bowler']
				#name2 = request.form['venue']
				#bowler_data = delivery_data[(delivery_data.bowler==name)]
				#match_data1 = match_data[(match_data.venue==name2)]
				if len(match_data1)>0:
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
									if(leaguage!='IPL'):
										balls = balls + len(bowler_data[(bowler_data.match_id==match)&(bowler_data.extra_runs==0)])
									else:	
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
					if(df_list3 == 0 ):
						df_list4 = 00
					

					answer = {'numberOfinnings':df_list1,'totalruns':df_list2,'totalwickets':df_list3,'average':df_list4 ,'economy':df_list5}
					#print(answer)
					return jsonpify(answer)
					#response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
					#an=response
					#df = pd.DataFrame(answer,index=['stats'])
					#return render_template('imageball.html',tables=[df.to_html(classes='data')], titles=df.columns.values,bowler=name,venue1=name2,vs="Vs")
				else:
					df_list1 = '--'
					df_list2 = '--'
					df_list3 = '--'
					df_list4 = '--'
					df_list5 = '--'
					answer = {'numberOfinnings':df_list1,'totalruns':df_list2,'totalwickets':df_list3,'average':df_list4 ,'economy':df_list5}
					#print(answer)
					return jsonpify(answer)
					#df = pd.DataFrame(answer,index=['stats'])
					#return render_template('imageball.html',tables=[df.to_html(classes='data')], titles=df.columns.values,bowler=name,venue1=name2,vs="Vs")




			
#@app.route('/batVsVenue')
#def my_form_1():
#		return render_template('batvenue.html')
			
@app.route('/batVsVenue', methods=['POST'])		
def home_1():
				req = request.get_json()
				#print(req)

   #        print(delivery_data)

				name = req["batsmanName"]
				leaguage = req["leaguageName"]
				name2 = req["venueName"]
				#print(name)
				#print(leaguage)
				#print(name2)
				if(leaguage=='IPL'):
					#print('inipl')
					batsman_data= delivery_data[(delivery_data.batsman==name)]
					match_data1 = match_data[(match_data.venue==name2)]
				elif (leaguage=='T20i'):
					#print('int20i')
					batsman_data=T20_delivery_data[(T20_delivery_data.batsman==name)]
					match_data1 = T20_match_data[(T20_match_data.venue==name2)]
				elif (leaguage=='BBL'):
					batsman_data=BBL_delivery_data[(BBL_delivery_data.batsman==name)]
					match_data1 = BBL_match_data[(BBL_match_data.venue==name2)]
				   	


				batting_first = list()
	#			name = request.form['batsman']
	#			name2 = request.form['venue']
	#			batsman_data = delivery_data[(delivery_data.batsman==name)]
	#			match_data1 = match_data[(match_data.venue==name2)]
				if len(match_data1)>0:
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
									if(leaguage!='IPL'):
										out = out+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.player_dismissed==name)])
									else:	
										out = out+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.player_dismissed==name)&(batsman_data.is_super_over==0)])
									if(leaguage!='IPL'):
										balls = balls+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.extra_runs==0)])
									else:	
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



					answer = {'centuries':df_list,'halfCen':df_list1,'strikerate':df_list2,'totalrun':df_list3 ,'innings':df_list4,'outs' :df_list5,'average':df_list6}
					#print(answer)
					return jsonpify(answer)
			#		bat_vs_venue = abc.drop(columns=['batting first'])
		#			bat_array = bat_vs_venue.reset_index().values
				#	bat_answer = abc.values.tolist()

				#	response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
				#	an=response
				#	df = pd.DataFrame(answer,index=['stats'])
				#	return render_template('batvenue.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,venue1=name2,vs="Vs")
				else:
					df_list = '--'
					df_list1 = '--'
					df_list2 = '--'
					df_list3 = '--'
					df_list4 = '--'
					df_list5 = '--'
					df_list6 = '--'
					answer = {'centuries':df_list,'halfCen':df_list1,'strikerate':df_list2,'totalrun':df_list3 ,'innings':df_list4,'outs' :df_list5,'average':df_list6}
					#print(answer)
					return jsonpify(answer)
					#df = pd.DataFrame(answer,index=['stats'])
					#return render_template('batvenue.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,venue1=name2,vs="Vs")
		

#@app.route('/batVsBallInvVenue')
#def my_form_3():
#		return render_template('all.html')
			
@app.route('/batVsBallInvVenue', methods=['POST'])		
def home_3():
				req = request.get_json()
				#print(req)

   #        print(delivery_data)

				name = req["batsmanName"]
				leaguage = req["leaguageName"]
				name2 = req["bowlerName"]
				name3 = req["venue"]
				#print(name)
				#print(leaguage)
				#print(name2)
				if(leaguage=='IPL'):
					#print('inipl')
					batsman_data_1= delivery_data[(delivery_data.batsman==name)&(delivery_data.bowler==name2)]
					match_data1 = match_data[(match_data.venue==name3)]
				elif (leaguage=='T20i'):
					#print('int20i')
					batsman_data_1=T20_delivery_data[(T20_delivery_data.batsman==name)&(T20_delivery_data.bowler==name2)]
					match_data1 = T20_match_data[(T20_match_data.venue==name3)]
				elif (leaguage=='BBL'):
					batsman_data_1=BBL_delivery_data[(BBL_delivery_data.batsman==name)&(BBL_delivery_data.bowler==name2)]
					match_data1 = BBL_match_data[(BBL_match_data.venue==name3)]
					

				batting_first = list()
				#name = request.form['batsman']
				#name2 = request.form['bowler']
				#name3 = request.form['venue']
				#batsman_data_1=delivery_data[(delivery_data.batsman==name)&(delivery_data.bowler==name2)]
				#match_data1 = match_data[(match_data.venue==name3)]
				if len(match_data1)>0:
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
									if(leaguage!='IPL'):
										balls = balls+len(batsman_data_1[(batsman_data_1.match_id==match)&(batsman_data_1.extra_runs==0)])
									else:	
										balls=balls+len(batsman_data_1[(batsman_data_1.match_id==match)&(batsman_data_1.wide_runs==0)&(batsman_data_1.noball_runs==0)])
									#balls=balls+len(batsman_data_1[(batsman_data_1.match_id==match)&(batsman_data_1.wide_runs==0)&(batsman_data_1.noball_runs==0)])
									batting_first=batting_first+[[venue,1,balls,t,out]]
					batvs_venue = pd.DataFrame(batting_first,columns=['venue','batting first','balls','runs','out'])
					batsman_venue = batvs_venue[batvs_venue.balls != 0]
					abc = batsman_venue[batsman_venue.venue==name3]
					runs = abc.runs.sum()
					balls = abc.balls.sum()
					outs = abc.out.sum()
					#print(balls)
					if (balls != 0):
						strike = (runs/balls)*100
					else:
						strike = 00	

					run1 = np.asarray(runs)
					df_list = run1.tolist()

					ball1 = np.asarray(balls)
					df_list1 = ball1.tolist()

					out1 = np.asarray(outs)
					df_list2 = out1.tolist()

					str1 = np.asarray(strike)
					df_list3 = str1.tolist()


					answer = {'runs':df_list,'balls':df_list1,'out':df_list2,'strikerate':df_list3}
					#print(answer)
					return jsonpify(answer)
					#an = jsonpify(answer)
					#response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
					#an=response
					#df = pd.DataFrame(answer,index=['stats'])
					#return render_template('all.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,bowler=name2,venue1=name3,vs="Vs",In="In")
				else:
					df_list = '--'
					df_list1 = '--'
					df_list2 = '--'
					df_list3 = '--'
					answer = {'runs':df_list,'balls':df_list1,'out':df_list2,'strikerate':df_list3}
					#print(answer)
					return jsonpify(answer)
					#df = pd.DataFrame(answer,index=['stats'])
					#return render_template('all.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,bowler=name2,venue1=name3,vs="Vs",In="In")

#@app.route('/batVsteam')
#def my_form_4():
#		return render_template('batvsteam.html')
			
@app.route('/batVsteam', methods=['POST'])		
def home_4():
				req = request.get_json()
				#print(req)

   #        print(delivery_data)

				name = req["batsmanName"]
				leaguage = req["leaguageName"]
				name2 = req["team"]
				
				#print(name)
				#print(leaguage)
				#print(name2)
				if(leaguage=='IPL'):
					#print('inipl')
					batsman_data= delivery_data[(delivery_data.batsman==name)&(delivery_data.bowling_team==name2)]
					
				elif (leaguage=='T20i'):
					#print('int20i')
					batsman_data=T20_delivery_data[(T20_delivery_data.batsman==name)&(T20_delivery_data.bowling_team==name2)]
				elif (leaguage=='BBL'):
					batsman_data=BBL_delivery_data[(BBL_delivery_data.batsman==name)&(BBL_delivery_data.bowling_team==name2)]
				

				batting_first = list()
				#name = request.form['batsman']
				#name2 = request.form['team']
				#batting_first=list()
				#batsman_data = delivery_data[(delivery_data.batsman==name)&(delivery_data.bowling_team==name2)]
				if(leaguage!='IPL'):
					balls = len(batsman_data[(batsman_data.extra_runs==0)])
				else:	
					balls=len(batsman_data[(batsman_data.wide_runs==0)&(batsman_data.noball_runs==0)])
				#balls=len(batsman_data[(batsman_data.wide_runs==0)&(batsman_data.noball_runs==0)])
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
				
				answer = {'centuries':df_list,'halfcenturies':df_list1,'strikerate':df_list2,'totalrun':df_list3 ,'innings':df_list4,'outs' :df_list5,'average':df_list6}
				#print(answer)
				return jsonpify(answer)
				#response = json.dumps(answer, sort_keys = True, indent = 4, separators = (',', ': '))
				#df = pd.DataFrame(answer,index=['stats'])
				#return render_template('batvsteam.html',tables=[df.to_html(classes='data')], titles=df.columns.values,batsman=name,team1=name2,vss ="Vs")


#@app.route('/ballVsteam')
#def my_form_5():
#		return render_template('ballvsteam.html')

@app.route('/ballVsteam', methods=['POST'])		
def home_5():
				req = request.get_json()
				#print(req)

   #        print(delivery_data)

				name = req["bowlerName"]
				leaguage = req["leaguageName"]
				name2 = req["team"]
				
				
				if(leaguage=='IPL'):
					print('inipl')
					bowler_data= delivery_data[(delivery_data.bowler==name)&(delivery_data.batting_team==name2)]
					
				elif (leaguage=='T20i'):
					print('int20i')
					bowler_data=T20_delivery_data[(T20_delivery_data.bowler==name)&(T20_delivery_data.batting_team==name2)]
				elif (leaguage=='BBL'):
					print('int20i')
					bowler_data=BBL_delivery_data[(BBL_delivery_data.bowler==name)&(BBL_delivery_data.batting_team==name2)]	

				bowling_first = list()
				#name = request.form['bowler']
				#name2 = request.form['team']
				#bowler_data = delivery_data[(delivery_data.bowler==name)&(delivery_data.batting_team==name2)]
				wk = 0
				for wks in bowler_data[(bowler_data.dismissal_kind!='run out')&(bowler_data.dismissal_kind!='')].player_dismissed:
									if wks!='':
										wk = wk+1
				t=bowler_data.total_runs.sum()
				if(leaguage!='IPL'):
					balls = len(bowler_data[(bowler_data.extra_runs==0)])
				else:	
					balls=len(bowler_data[(bowler_data.wide_runs==0)&(bowler_data.noball_runs==0)])
				#balls=len(bowler_data[(bowler_data.wide_runs==0)&(bowler_data.noball_runs==0)])
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
			
				answer = {'innings':df_list1,'totalruns':df_list2,'totalwickets':df_list3,'average':df_list4 ,'economy':df_list5}
				#print(answer)
				return jsonpify(answer)
				#df = pd.DataFrame(answer,index=['stats'])
				#return render_template('ballvsteam.html',tables=[df.to_html(classes='data')], titles=df.columns.values,bowler=name,team1=name2,vs="Vs")
			

#@app.route('/selection')
#def my_form_7():
#		return render_template('selection.html')
		
			
@app.route('/selection', methods=['POST'])		
def home_7():
				req = request.get_json()
				#print(req)

   #        print(delivery_data)

				bat1 = req['batsman1']
				bat2 = req['batsman2']
				bat3 = req['batsman3']
				bat4 = req['batsman4']
				bat5 = req['batsman5']
				bat6 = req['batsman6']

				ball1 = req['bowler1']
				ball2 = req['bowler2']
				ball3 = req['bowler3']
				ball4 = req['bowler4']
				ball5 = req['bowler5']
				ball6 = req['bowler6']

				leaguage = req["leaguageName"]
				
				
				#print(name)
				#print(leaguage)
				#print(name2)
				#if(leaguage=='IPL'):
				#	print('inipl')
				#	delivery_data = delivery_data
					
				#elif (leaguage=='T20i'):
				#	print('int20i')
			#		delivery_data =T20_delivery_data

				#bat1 = request.form['batsman1']
				#bat2 = request.form['batsman2']
				#bat3 = request.form['batsman3']
				#bat4 = request.form['batsman4']
				#bat5 = request.form['batsman5']
				#ball1 = request.form['bowler1']
				#ball2 = request.form['bowler2']
				#ball3 = request.form['bowler3']
				#ball4 = request.form['bowler4']
				#ball5 = request.form['bowler5']
				a = [bat1,bat2,bat3,bat4,bat5,bat6]
				b = [ball1,ball2,ball3,ball4,ball5,ball6]
				batsman = list()
				bowler = list()			
				for i in a:
					for y in b:
						if(leaguage=='IPL'):
							batsman_data_1=delivery_data[(delivery_data.batsman==i)&(delivery_data.bowler==y)]
							batsman_data_full=delivery_data[(delivery_data.batsman==i)]
							out = len(delivery_data.player_dismissed==i)
							bowler_data_full = delivery_data[(delivery_data.bowler==y)]
						elif (leaguage=='T20i'):
							batsman_data_1=T20_delivery_data[(T20_delivery_data.batsman==i)&(T20_delivery_data.bowler==y)]
							batsman_data_full=T20_delivery_data[(T20_delivery_data.batsman==i)]
							out = len(T20_delivery_data.player_dismissed==i)
							bowler_data_full = T20_delivery_data[(T20_delivery_data.bowler==y)]
						elif (leaguage=='BBL'):
							batsman_data_1=BBL_delivery_data[(BBL_delivery_data.batsman==i)&(BBL_delivery_data.bowler==y)]
							batsman_data_full=BBL_delivery_data[(BBL_delivery_data.batsman==i)]
							out = len(BBL_delivery_data.player_dismissed==i)
							bowler_data_full = BBL_delivery_data[(BBL_delivery_data.bowler==y)]	
							

						#batsman_data_1=delivery_data[(delivery_data.batsman==i)&(delivery_data.bowler==y)]

						
						#batsman_data_full = delivery_data[(delivery_data.batsman==i)]
						runs_full = batsman_data_full.batsman_runs.sum()


						#out = len(delivery_data.player_dismissed==i)
						batsman_average = runs_full/out # batsman batting average 
						runs = batsman_data_1.batsman_runs.sum()
	        
						outss=0
						for outs in batsman_data_1.dismissal_kind:
							if ((outs!="")&(outs!="run out")):
								outss = outss + 1
						batsman_average_bowler = runs/outss    # batsman vs bowler batting average
						if outss==0:
							batsman_average_bowler = runs


						#bowler_data_full = delivery_data[(delivery_data.bowler==y)]
						runs_bowler = bowler_data_full.total_runs.sum()
						outs1=0
						for outs in bowler_data_full.dismissal_kind:
							if ((outs!="")&(outs!="run out")):
								outs1 = outs1 + 1
						bowler_average = runs_bowler/outs1    #bowler average
						#print(bowler_average)
						runs_bowler_batsman = batsman_data_1.total_runs.sum()
						bowler_average_batsman = runs_bowler_batsman/outss # bowler vs batsman bowling average
						if outss==0:
							#print('in bowler if')
							bowler_average_batsman = runs_bowler_batsman
						
						
						#balls=len(batsman_data_1[(batsman_data_1.wide_runs==0)&(batsman_data_1.noball_runs==0)])
						
						#six = len(batsman_data_1[batsman_data_1.batsman_runs==6])
						#four = len(batsman_data_1[batsman_data_1.batsman_runs==4])
						#dotball = len(batsman_data_1[batsman_data_1.total_runs==0])
						bat_score = (batsman_average_bowler/bowler_average)*100
						bowl_score = (batsman_average/bowler_average_batsman)*100
						if (len(batsman_data_1)==0):
							#print('in len if')
							bat_score = batsman_average
							bowl_score = (1/bowler_average)  
						if runs==0:
							bowl_score = (1/bowler_average)
						batsman = batsman+[[i,y,bat_score]]
						bowler = bowler+[[y,i,bowl_score]]
						
				dsds=pd.DataFrame(data=batsman,columns=['batsman','bowler','bat_score'])
				batsman_list = list()
				ds=pd.DataFrame(data=bowler,columns=['bowler','batsman','bowl_score'])
				bowler_list = list()
				for i in a:
					final_score = dsds[dsds.batsman==i].bat_score.sum()
					batsman_list = batsman_list+[[i,final_score]]
				for y in b:
					final_score = ds[ds.bowler==y].bowl_score.sum()
					bowler_list = bowler_list+[[y,final_score]]    
				df = pd.DataFrame(data=batsman_list,columns=['batsman','finalscore'])
				abcd = df[df.batsman!='']
				dfdf = pd.DataFrame(data=bowler_list,columns=['bowler','finalscore'])
				abcd1 = dfdf[dfdf.bowler!='']
				#print(abcd)
				#print(abcd1)
				return jsonpify(batsman = json.loads(abcd.to_json(orient='index')), bowler = json.loads(abcd1.to_json(orient='index')))
				#return render_template('selection.html',tables=[abcd.to_html(classes='data')],tables2=[abcd1.to_html(classes='data')])
	

#@app.route('/batvsground')
#def my_form_8():
#		return render_template('batsmanvsground.html')	
		
@app.route('/batvsground', methods=['POST'])		
def home_8():
				req = request.get_json()
				

   #        print(delivery_data)

				bat1 = req['batsmanS1']
				bat2 = req['batsmanS2']
				bat3 = req['batsmanS3']
				bat4 = req['batsmanS4']
				bat5 = req['batsmanS5']

				bat6 = req['batsmanS6']
				bat7 = req['batsmanS7']
				bat8 = req['batsmanS8']
				bat9 = req['batsmanS9']
				bat10 = req['batsmanS10']
				
				name2 = req['venueName']
				
				leaguage = req["leaguageName"]

			
				d = [bat1,bat2,bat3,bat4,bat5,bat6,bat7,bat8,bat9,bat10]
				batman = list()

				if(leaguage=='IPL'):
					match_data_1_1 = match_data[(match_data.venue==name2)]
					#out = len(delivery_data.player_dismissed==i)
				elif (leaguage=='T20i'):
					match_data_1_1 = T20_match_data[(T20_match_data.venue==name2)]
				elif (leaguage=='BBL'):
					match_data_1_1 = BBL_match_data[(BBL_match_data.venue==name2)]	
					#out = len(T20_delivery_data.player_dismissed==i)


				#match_data_1_1 = match_data[(match_data.venue==name2)]

				if len(match_data_1_1)>0:
					for i in d:
						batting_first = list()
						if(leaguage=='IPL'):
							batsman_data = delivery_data[(delivery_data.batsman==i)]
							match_data1 = match_data[(match_data.venue==name2)]
						elif (leaguage=='T20i'):
							batsman_data = T20_delivery_data[(T20_delivery_data.batsman==i)]
							match_data1 = T20_match_data[(T20_match_data.venue==name2)]
						elif (leaguage=='BBL'):
							batsman_data = BBL_delivery_data[(BBL_delivery_data.batsman==i)]
							match_data1 = BBL_match_data[(BBL_match_data.venue==name2)]	

						for venue in match_data1.venue.unique():
								matches=match_data1[(match_data1.venue==venue)].id
						#  print(matches)
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
									if(leaguage!='IPL'):
										out = out+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.player_dismissed==i)])
										balls=balls+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.extra_runs==0)])
									else:
										out = out+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.player_dismissed==i)&(batsman_data.is_super_over==0)])
										balls=balls+len(batsman_data[(batsman_data.match_id==match)&(batsman_data.wide_runs==0)&(batsman_data.noball_runs==0)])

									batting_first=batting_first+[[venue,1,balls,t,out]]
						batvs_venue = pd.DataFrame(batting_first,columns=['venue','batting first','balls','runs','out'])
						batsman_venue = batvs_venue[batvs_venue.balls != 0]
						abc = batsman_venue[batsman_venue.venue==name2]
						#			venue_runs = pd.DataFrame(datatoss[(datatoss.venue==name3)])
						total_runs = abc.runs.sum()
						outss = abc.out.sum()
						average = total_runs/outss
						h_cen = 0
						cen = 0
						num_inni = len(abc.index)
						for fif in abc.runs:
								if((fif>49) & (fif<100)):
									h_cen = h_cen+1
								elif(fif>99):
									cen = cen+1

						sti = (total_runs/abc.balls.sum())*100
						zeros = len(abc[(abc.runs==0)&(abc.out==1)])
						score = average*0.4228+num_inni*0.2358+sti*0.044072+cen*0.1863+0.1105*h_cen
						batman = batman + [[i,name2,score]]

					batman_ground = pd.DataFrame(batman,columns=['batsman','venue','score'])
					abcd = batman_ground[batman_ground.batsman!='']
					abcd1 = abcd.drop(columns='venue')
					#print(abcd1)
					return jsonpify(batsman = json.loads(abcd1.to_json(orient='index')))
					#return render_template('batsmanvsground.html',tables=[abcd1.to_html(classes='data')],venue1=name2)
				else:
					i = '--'
					name2 = '--'
					score = '--'
					batman = batman + [[i,name2,score]]
					ballman_ground = pd.DataFrame(batman,columns=['batsman','venue','score'])
					ballman_ground1 = ballman_ground.drop(columns='venue')
					return jsonpify(batsman = json.loads(ballman_ground1.to_json(orient='index')))
					#return render_template('batsmanvsground.html',tables=[ballman_ground.to_html(classes='data')],venue1=name2)

#@app.route('/ballvsground')
#def my_form_9():
#		return render_template('bowlervsground.html')	
		
@app.route('/ballvsground', methods=['POST'])		
def home_9():
				req = request.get_json()
				

   #        print(delivery_data)

				ball1 = req['bowlerS1']
				ball2 = req['bowlerS2']
				ball3 = req['bowlerS3']
				ball4 = req['bowlerS4']
				ball5 = req['bowlerS5']

				ball6 = req['bowlerS6']
				ball7 = req['bowlerS7']
				ball8 = req['bowlerS8']
				ball9 = req['bowlerS9']
				ball10 = req['bowlerS10']
				
				name2 = req['venueName']
				
				leaguage = req["leaguageName"]

			
				d = [ball1,ball2,ball3,ball4,ball5,ball6,ball7,ball8,ball9,ball10]
				bowlerlist = list()
				#match_data_1_1 = match_data[(match_data.venue==name2)]
				if(leaguage=='IPL'):
					match_data_1_1 = match_data[(match_data.venue==name2)]
					#out = len(delivery_data.player_dismissed==i)
				elif (leaguage=='T20i'):
					match_data_1_1 = T20_match_data[(T20_match_data.venue==name2)]
				elif (leaguage=='BBL'):
					match_data_1_1 = BBL_match_data[(BBL_match_data.venue==name2)]	

				if len(match_data_1_1)>0:
					for i in d:
						bowling_first = list()
						if(leaguage=='IPL'):
							bowler_data = delivery_data[(delivery_data.bowler==i)]
							match_data1 = match_data[(match_data.venue==name2)]
						elif (leaguage=='T20i'):
							bowler_data = T20_delivery_data[(T20_delivery_data.bowler==i)]
							match_data1 = T20_match_data[(T20_match_data.venue==name2)]
						elif (leaguage=='BBL'):
							bowler_data = BBL_delivery_data[(BBL_delivery_data.bowler==i)]
							match_data1 = BBL_match_data[(BBL_match_data.venue==name2)]
	

						#bowler_data = delivery_data[(delivery_data.bowler==i)]
						#match_data1 = match_data[(match_data.venue==name2)]
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
												if wks!='\r':
														wk = wk+1
										t=bowler_data[bowler_data.match_id==match].total_runs.sum()
										if(leaguage=='IPL'):
											balls=balls+len(bowler_data[(bowler_data.match_id==match)&(bowler_data.wide_runs==0)&(bowler_data.noball_runs==0)])
										else:
											balls=balls+len(bowler_data[(bowler_data.match_id==match)&(bowler_data.extra_runs==0)])
										
										bowling_first=bowling_first+[[venue,t,wk,balls]]
						bowvs_venue = pd.DataFrame(bowling_first,columns=['venue','runs','wickets','balls'])
						bowler_venue = bowvs_venue[bowvs_venue.balls != 0]
						abc = bowler_venue[bowler_venue.venue==name2]

						inning = len(abc.index)
						wick = abc.wickets.sum()
						runs = abc.runs.sum()
						balls1 = abc.balls.sum()
						over = int(balls1/6)
						strike = balls1/wick
						#economy = (runs/over)
						average = runs/wick
						ff = len(abc[abc.wickets>=3])
						score = 0.168678*inning+ 0.24294*(1/strike)*1000+ 0.364488*(1/average)*1000+0.2234*ff
						bowlerlist = bowlerlist + [[i,name2,score]]
					ballman_ground = pd.DataFrame(bowlerlist,columns=['bowler','venue','score'])
					abcd = ballman_ground[ballman_ground.bowler!='']
					abcd1 = abcd.drop(columns='venue')
					#print(abcd1)
					return jsonpify(bowler = json.loads(abcd1.to_json(orient='index')))
					#return render_template('bowlervsground.html',tables=[abcd1.to_html(classes='data')],venue1=name2)
				else:
					i = '--'
					name2 = '--'
					score = '--'
					bowlerlist = bowlerlist + [[i,name2,score]]
					ballman_ground = pd.DataFrame(bowlerlist,columns=['bowler','venue','score'])
					abcd = ballman_ground[ballman_ground.bowler!='']
					abcd1 = abcd.drop(columns='venue')
					return jsonpify(bowler = json.loads(abcd1.to_json(orient='index')))
					#return render_template('bowlervsground.html',tables=[ballman_ground.to_html(classes='data')],venue1=name2)


#@app.route('/batindepth')
#def my_form_10():
#		return render_template('bat_indepth.html')
		

@app.route('/batindepth', methods=['POST'])
def my_home_10():
				req = request.get_json()
				
				i = req['batsmanName']
				
				name2 = req['teamName']
				
				leaguage = req["leaguageName"]

				#i = request.form['batsman']
				#name2 = request.form['team']
				batsman = list()
				batsman2 = list()
				if name2=='Royal Challengers Bangalore':
					name2 = ['Mohammed Siraj','N Saini','A Zampa','YS Chahal','KW Richardson','Shahbaz Ahmed','Washington Sundar','HV Patel','DT Christian']
				elif name2=='Kolkata Knight Riders':
					name2 = ['AD Russell','N Rana','Kuldeep Yadav','LH Ferguson','P Krishna','SP Narine','PJ Cummins','Shivam Mavi','KL Nagarkoti','V Chakravarthy','Shakib Al Hasan','Harbhajan Singh','BCJ Cutting']
				elif name2=='Kings XI Punjab':
					name2 = ['CJ Jordan','R Bishnoi','Mohammed Shami','H Brar','M Ashwin','Arshdeep Singh','MC Henriques']
				elif name2=='Delhi Capitals':
					name2 = ['A Mishra','AR Patel','Avesh Khan','I Sharma','K Rabada','T Curran','R Ashwin','CR Woakes','MP Stoinis','UT Yadav','Anrich Nortje']
				elif name2=='Sunrisers Hyderabad':
					name2= ['B Kumar','Abhishek Sharma','Mohammad Nabi','Rashid Khan','Sandeep Sharma','S Nadeem','S Kaul','K Ahmed','Basil Thampi','JO Holder','T Natarajan','V Shankar','Mujeeb Ur Rahman']
				elif name2=='Mumbai Indians':
					name2=['DS Kulkarni','HH Pandya','JJ Bumrah','KA Pollard','A Roy','J Yadav','RD Chahar','NM Coulter-Nile','KH Pandya','TA Boult','AF Milne','PP Chawla','JDS Neesham']
				elif name2=='Rajasthan Royals':	
					name2= ['BA Stokes','J Archer','M Markande','S Gopal','Kartik Tyagi','M Lomror','AJ Tye','R Tewatia','JD Unadkat','R Parag','S Dube','CH Morris','Mustafizur Rahman']
				elif name2=='Chennai Super Kings':	
					name2= ['DL Chahar','S Curran','Imran Tahir','M Santner','RA Jadeja','DJ Bravo','SN Thakur','KV Sharma','L Ngidi','Hazlewood','M Ali','K Gowtham']
				
				if(leaguage=='IPL'):
					batsman_data_2 = delivery_data[(delivery_data.batsman==i)]
				elif(leaguage=='T20i'):
					batsman_data_2 = T20_delivery_data[(T20_delivery_data.batsman==i)]
				elif(leaguage=='BBL'):
					batsman_data_2 = BBL_delivery_data[(BBL_delivery_data.batsman==i)]	
						
				if len(batsman_data_2)>0: 
					if(leaguage=='IPL'):
						batsman_data_2 = delivery_data[(delivery_data.batsman==i)]
						hardhitting2 = ((4*len(batsman_data_2[batsman_data_2.batsman_runs==4]))+(6*len(batsman_data_2[batsman_data_2.batsman_runs==6])))/len(batsman_data_2[(batsman_data_2.noball_runs==0)&(batsman_data_2.wide_runs==0)])
						finisher2 = ((len(batsman_data_2.match_id.unique())-len(delivery_data[delivery_data.player_dismissed==i])))/len(batsman_data_2.match_id.unique())
						fastscore2 = batsman_data_2.batsman_runs.sum()/len(batsman_data_2[(batsman_data_2.noball_runs==0)&(batsman_data_2.wide_runs==0)])
						average2 = batsman_data_2.batsman_runs.sum()/len(delivery_data[delivery_data.player_dismissed==i])
						runningBW2 = ((batsman_data_2.batsman_runs.sum())-((4*len(batsman_data_2[batsman_data_2.batsman_runs==4]))+(6*len(batsman_data_2[batsman_data_2.batsman_runs==6]))))/len(batsman_data_2[(batsman_data_2.batsman_runs!=4)&(batsman_data_2.batsman_runs!=6)&(batsman_data_2.noball_runs==0)&(batsman_data_2.wide_runs==0)])
						batsman2 = batsman2 + [[i,hardhitting2,finisher2,fastscore2,average2,runningBW2]]
					
					elif(leaguage=='T20i'):
						batsman_data_2 = T20_delivery_data[(T20_delivery_data.batsman==i)]
						hardhitting2 = ((4*len(batsman_data_2[batsman_data_2.batsman_runs==4]))+(6*len(batsman_data_2[batsman_data_2.batsman_runs==6])))/len(batsman_data_2[(batsman_data_2.extra_runs==0)])
						finisher2 = ((len(batsman_data_2.match_id.unique())-len(T20_delivery_data[T20_delivery_data.player_dismissed==i])))/len(T20_delivery_data.match_id.unique())
						fastscore2 = batsman_data_2.batsman_runs.sum()/len(batsman_data_2[(batsman_data_2.extra_runs==0)])
						average2 = batsman_data_2.batsman_runs.sum()/len(T20_delivery_data[T20_delivery_data.player_dismissed==i])
						runningBW2 = ((batsman_data_2.batsman_runs.sum())-((4*len(batsman_data_2[batsman_data_2.batsman_runs==4]))+(6*len(batsman_data_2[batsman_data_2.batsman_runs==6]))))/len(batsman_data_2[(batsman_data_2.batsman_runs!=4)&(batsman_data_2.batsman_runs!=6)&(batsman_data_2.extra_runs==0)])
						batsman2 = batsman2 + [[i,hardhitting2,finisher2,fastscore2,average2,runningBW2]]

					elif(leaguage=='BBL'):
						batsman_data_2 = BBL_delivery_data[(BBL_delivery_data.batsman==i)]
						hardhitting2 = ((4*len(batsman_data_2[batsman_data_2.batsman_runs==4]))+(6*len(batsman_data_2[batsman_data_2.batsman_runs==6])))/len(batsman_data_2[(batsman_data_2.extra_runs==0)])
						finisher2 = ((len(batsman_data_2.match_id.unique())-len(BBL_delivery_data[BBL_delivery_data.player_dismissed==i])))/len(BBL_delivery_data.match_id.unique())
						fastscore2 = batsman_data_2.batsman_runs.sum()/len(batsman_data_2[(batsman_data_2.extra_runs==0)])
						average2 = batsman_data_2.batsman_runs.sum()/len(BBL_delivery_data[BBL_delivery_data.player_dismissed==i])
						runningBW2 = ((batsman_data_2.batsman_runs.sum())-((4*len(batsman_data_2[batsman_data_2.batsman_runs==4]))+(6*len(batsman_data_2[batsman_data_2.batsman_runs==6]))))/len(batsman_data_2[(batsman_data_2.batsman_runs!=4)&(batsman_data_2.batsman_runs!=6)&(batsman_data_2.extra_runs==0)])
						batsman2 = batsman2 + [[i,hardhitting2,finisher2,fastscore2,average2,runningBW2]]	
					

					for y in name2:
						if(leaguage=='IPL'):
							batsman_data_1 = delivery_data[(delivery_data.batsman==i)&(delivery_data.bowler==y)]
						elif(leaguage=='T20i'):
							batsman_data_1 = T20_delivery_data[(T20_delivery_data.batsman==i)&(T20_delivery_data.bowler==y)]
						elif(leaguage=='BBL'):
							batsman_data_1 = BBL_delivery_data[(BBL_delivery_data.batsman==i)&(BBL_delivery_data.bowler==y)]	
								
						if len(batsman_data_1)>0:
							if(leaguage=='IPL'):
								out = len(batsman_data_1[(batsman_data_1.player_dismissed==i)&(batsman_data_1.dismissal_kind!='run out')])
								hardhitting = ((4*len(batsman_data_1[batsman_data_1.batsman_runs==4]))+(6*len(batsman_data_1[batsman_data_1.batsman_runs==6])))/len(batsman_data_1[(batsman_data_1.noball_runs==0)&(batsman_data_1.wide_runs==0)])
								# finisher = ((len(batsman_data_1.match_id.unique())-len(batsman_data_1[batsman_data_1.player_dismissed==i])))/len(batsman_data_1.match_id.unique())
								# fastscore = batsman_data_1.batsman_runs.sum()/len(batsman_data_1[(batsman_data_1.noball_runs==0)&(batsman_data_1.wide_runs==0)])
								# average = batsman_data_1.batsman_runs.sum()/len(batsman_data_1[batsman_data_1.player_dismissed==i])
								runningBW = ((batsman_data_1.batsman_runs.sum())-((4*len(batsman_data_1[batsman_data_1.batsman_runs==4]))+(6*len(batsman_data_1[batsman_data_1.batsman_runs==6]))))/len(batsman_data_1[(batsman_data_1.batsman_runs!=4)&(batsman_data_1.batsman_runs!=6)&(batsman_data_1.noball_runs==0)&(batsman_data_1.wide_runs==0)])
								batsman = batsman + [[i,y,hardhitting,runningBW,out]]
							else:
								out = len(batsman_data_1[(batsman_data_1.player_dismissed==i)&(batsman_data_1.dismissal_kind!='run out')])
								hardhitting = ((4*len(batsman_data_1[batsman_data_1.batsman_runs==4]))+(6*len(batsman_data_1[batsman_data_1.batsman_runs==6])))/len(batsman_data_1[(batsman_data_1.extra_runs==0)])
								# finisher = ((len(batsman_data_1.match_id.unique())-len(batsman_data_1[batsman_data_1.player_dismissed==i])))/len(batsman_data_1.match_id.unique())
								# fastscore = batsman_data_1.batsman_runs.sum()/len(batsman_data_1[(batsman_data_1.noball_runs==0)&(batsman_data_1.wide_runs==0)])
								# average = batsman_data_1.batsman_runs.sum()/len(batsman_data_1[batsman_data_1.player_dismissed==i])
								runningBW = ((batsman_data_1.batsman_runs.sum())-((4*len(batsman_data_1[batsman_data_1.batsman_runs==4]))+(6*len(batsman_data_1[batsman_data_1.batsman_runs==6]))))/len(batsman_data_1[(batsman_data_1.batsman_runs!=4)&(batsman_data_1.batsman_runs!=6)&(batsman_data_1.extra_runs==0)])
								batsman = batsman + [[i,y,hardhitting,runningBW,out]]

									
						else:
							hardhitting = 0 
							runningBW = 0 
							out = 0 
							batsman = batsman + [[i,y,hardhitting,runningBW,out]]


					dsds=pd.DataFrame(data=batsman,columns=['batsman','bowler','hardhitting','runningBTWWicket','out'])    
					ds=pd.DataFrame(data=batsman2,columns=['batsman','hardhitting','finisher','fastscore','average','runningBTWWicket'])
					abcd1 = dsds.drop(columns='batsman')
					abcd2 = ds.drop(columns='batsman')
					#print(abcd1)
					#print(abcd2)
					return jsonpify(teamlist = json.loads(abcd1.to_json(orient='index')),batsman = json.loads(abcd2.to_json(orient='index')) )
					#return render_template('bat_indepth.html',tables=[abcd2.to_html(classes='data')],tables2=[abcd1.to_html(classes='data')],p=i,k='ALL IPL PERFORMANCE')
				else:
					i = '--'
					y = '--'
					hardhitting = '--'
					runningBW = '--'
					out = '--'
					batsman = batsman + [[i,y,hardhitting,runningBW,out]]
					dsds=pd.DataFrame(data=batsman,columns=['batsman','bowler','hardhitting','runningBTWWicket','out'])
					ds=pd.DataFrame(data=batsman,columns=['batsman','bowler','hardhitting','runningBTWWicket','out'])
					abcd1 = dsds.drop(columns='batsman')
					abcd2 = ds.drop(columns='batsman')
					return jsonpify(teamlist = json.loads(abcd1.to_json(orient='index')),batsman = json.loads(abcd2.to_json(orient='index')) )
					


#@app.route('/ballindepth')
#def my_form_11():
#		return render_template('ball_indepth.html')
		

@app.route('/ballindepth', methods=['POST'])
def my_home_11():
				req = request.get_json()
				
				a = req['bowlerName']
				
				leaguage = req["leaguageName"]

				bowler_final = list()
				#a = request.form['bowler']
				bowler = list()
				#print(a)
				if(leaguage=='IPL'):
					bowler_data = delivery_data[delivery_data.bowler==a]
					t=bowler_data.total_runs.sum()
					balls=len(bowler_data[(bowler_data.wide_runs==0)&(bowler_data.noball_runs==0)])
				elif(leaguage=='T20i'):
					bowler_data = T20_delivery_data[T20_delivery_data.bowler==a]	
					t=bowler_data.total_runs.sum()
					balls=len(bowler_data[(bowler_data.extra_runs==0)])
				elif(leaguage=='BBL'):
					bowler_data = BBL_delivery_data[BBL_delivery_data.bowler==a]	
					t=bowler_data.total_runs.sum()
					balls=len(bowler_data[(bowler_data.extra_runs==0)])	

				#print(bowler_data)
				innings = len(bowler_data.match_id.unique())
				economy = t/(balls/6)
				out = len(bowler_data[(bowler_data.dismissal_kind!='')&(bowler_data.dismissal_kind!='run out')])
				#print(t,out)
				if out!=0:
					wicket_takers = balls/out
					wicket_takers_final = 1/wicket_takers
					average = t/out
				else:
					wicket_takers_final = '--'
					average = '--'
				for i in bowler_data.match_id.unique():
					out = len(bowler_data[(bowler_data.dismissal_kind!='')&(bowler_data.dismissal_kind!='run out')&(bowler_data.match_id==i)])
					bowler = bowler + [[i,out]]
				bowler_ = pd.DataFrame(data=bowler,columns=['match_id','wickets'])
				wick3 = len(bowler_[bowler_.wickets>=3])
				if innings!=0:
					big_wick = wick3/innings
					short_perfo = ((bowler_.wickets.sum())-(3*wick3))/(innings-wick3)
					short_perfo_final = 1/short_perfo
				else:
					big_wick = '--'
					short_perfo = '--'
					short_perfo_final = '--'
				bowler_final = bowler_final + [[economy,wicket_takers_final,average,big_wick,short_perfo]]
				bowler_final_ = pd.DataFrame(data=bowler_final,columns=['economy','wicket_takers','average','big_wicket_taker','short_performance'])
				#print(bowler_final_)
				return jsonpify(bowler = json.loads(bowler_final_.to_json(orient='index')))
				#return render_template('ball_indepth.html',tables=[bowler_final_.to_html(classes='data')],k = a)
		
		
if __name__=='__main__':
      #http = WSGIServer(('', 5000), app.wsgi_app) 
      #http.serve_forever()
	   app.run	(debug=True,threaded=True)
