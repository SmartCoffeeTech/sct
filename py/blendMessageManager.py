import serialHandle
import dbHandle
import jsonManager as jsonHandle
import tweetHandle
from datetime import datetime
import blendSuggestionCalculator as blendCalc
import json


def parseMessageAndReturnInfo(message):
	print "parseMessageAndReturnInfo:", message
	if message.startswith('grinderPercentage'):
		parsed_msg = message.split(' ')
		grind_pct_list = [float(parsed_msg[1]),float(parsed_msg[2]),float(parsed_msg[3])]
		log_msg = str(parsed_msg[0]) + "|" + str(parsed_msg[1]) + "|" + str(parsed_msg[2]) +  "|" + str(parsed_msg[3]) + "|" + str(datetime.now())
		# grinder_status = log_msg[0:8]
		return grind_pct_list,log_msg,message
	# no longer get these messages
	
	elif message.startswith('comp') or message.startswith('reset'):
		parsed_msg = message.split(' ')
		grind_pct_list = ['0','0','0']
		log_msg = str(parsed_msg[0]) + "|" + str( datetime.now())
		# grinder_status = log_msg[0:8]
		return grind_pct_list,log_msg,message
	
	elif message.startswith('grinderCanister'):
		parsed_msg = message.split(' ')
		grind_pct_list = ['0','0','0']
		log_msg = str(parsed_msg[0]) + "|" + str( datetime.now())
		return grind_pct_list,log_msg,message
		
	elif message.startswith('noCanister'):
		parsed_msg = message.split(' ')
		grind_pct_list = ['0','0','0']
		log_msg = str(parsed_msg[0]) + "|" + str( datetime.now())
		return grind_pct_list,log_msg,message
		
	else:
		print "Failure. did not receive an expected value! I got: %s" % message

	
def logGrinderMessage(filename,message):
	file = open(filename,'a')
	message += ' \n'
	file.write(message)
	file.close()

#do we need this?
def setupCoffeeList(db_con,db_cur):
	coffee_list=[]
	query = """Select country_of_origin,grinder from Coffee order by grinder"""
	db_cur.execute(query)
	result = db_cur.fetchall()
	
	for each in result:
		coffee_list.append(each[0]+'n')
	
	return coffee_list
	
def setup():
	#get coffee country_of_origin from database
	#set these in a config file
	blend_chars_filename = '../www/data/dataout2.json'
	log_filename = '../log/grinder.log'
	page_location_filename = '../www/data/page_location.json'
	
	#initalize blend jsons - next iter move to db
	blends = blendCalc.initData('blend')
	#setup the connections(grinder and db) and get the latest customer created from the web interface
	ser = serialHandle.setupSerial()
	#setup db conns
	db_con,db_cur = dbHandle.openConn()
	#setup coffe list - needed?
	coffee_list = setupCoffeeList(db_con,db_cur)
	jsonHandle.initJson(blend_chars_filename)
	
	if serialHandle.grinderInit(ser)=='arduinoReady':
		return coffee_list,blends,blend_chars_filename,log_filename,page_location_filename,ser,db_con,db_cur
		
def getBlendDict(blend_name,blends):
	for each_dict in blends:
		if each_dict['name']==blend_name:
			return each_dict
		else:
			'No blend_name matches, you sir, are fucked.'
	
def getApplicationState(filename):
	page_location = jsonHandle.readJson(filename)
	page_location = page_location['status']
	return page_location

def stateController(page_location,page_location_filename,coffee_list,blends,blend_chars_filename,log_filename,ser,db_con,db_cur):
	""" directs python based on the state of the web application"""
	
	try:
		
		if page_location in ['index1.html','blend-selection.html']:
			return
			
		elif page_location == 'base-blend.html':
			# run once
			#get cust1 from the db
			qry = 'select order_id,taste_profile from Orders order by time_created desc limit 1'
			result = dbHandle.executeQuery(db_con,db_cur,qry,'select')
			cust1 = json.loads(result[0][1])
			
			#global blend_name
			blend_name = blendCalc.computeCoffeeBlendSuggestion(blends,cust1)
			qry = """update Orders set blend_id=(Select blend_id from Blend where blend_name='%s' limit 1) where order_id=%d""" % (blend_name,int(result[0][0]))
			dbHandle.executeQuery(db_con,db_cur,qry,'insert')
			
			global blend_dict
			blend_dict = getBlendDict(blend_name,blends)
			aroma_dict = blendCalc.computeTop3Aromas(blend_dict)
			aroma_json = jsonHandle.makerOfJsons(aroma_dict,'blendAromas')
			jsonHandle.postJsonToServer(blend_chars_filename,aroma_json)
			jsonHandle.updateJson(page_location_filename,'base-blend.htm')
			return
			
		elif page_location == 'grinding.html':
			
			global base_grinder_pct_list
			base_grinder_pct_list=[]
			qry = 'select customization_pct from Orders order by time_created desc limit 1'
			custom_pct = dbHandle.executeQuery(db_con,db_cur,qry,'select')
			custom_pct = int(custom_pct[0][0])
			qry = """select grinder,coffee_pct from Orders join Blend using(blend_id) join Coffee using(coffee_id) where order_id=(select order_id from Orders order by time_created desc limit 1) order by grinder"""
			result = dbHandle.executeQuery(db_con,db_cur,qry,'select')
			
			for each in result:
				base_grinder_pct_list.append(int(each[1]))
			base_grinder_pct_list = blendCalc.computeBlendPct(base_grinder_pct_list,custom_pct)
			
			#send the base_pct
			print 'sending the base pct'
			global base_pct
			base_pct = sum(base_grinder_pct_list)
			msg_to_grinder = 'basePercentage '+str(int(base_pct))
			serialHandle.grinderCommManager(ser,msg_to_grinder)
			
			#send the grinder pct values
			print 'sending grinder pct values'
			msg_to_grinder = 'blend ' + str(base_grinder_pct_list[0]) + ' ' + str(base_grinder_pct_list[1]) + ' ' + str(base_grinder_pct_list[2])
			serialHandle.grinderCommManager(ser,msg_to_grinder)
			
			#make the necessary jsons
			print 'making jsons'
			blend_pct_dict = jsonHandle.makeJson(base_grinder_pct_list)
			jsonHandle.updaterOfJsons(blend_chars_filename,'blendPercentages',blend_pct_dict)
			jsonHandle.updaterOfJsons(blend_chars_filename,'state','base')
			jsonHandle.updaterOfJsons(blend_chars_filename,'status','grinding')
			coffee_dict = jsonHandle.makeJson([0,0,0])
			jsonHandle.updaterOfJsons(blend_chars_filename,'customerPercentages',coffee_dict)
			jsonHandle.updaterOfJsons(blend_chars_filename,'customerAcidity',blend_dict['acidity'])
			jsonHandle.updaterOfJsons(blend_chars_filename,'customerBody',blend_dict['body'])
			#update the page to avoid running again
			jsonHandle.updateJson(page_location_filename,'grinding.htm')
			
			
		elif page_location == 'grinding.htm':
			letsGrind(coffee_list,blend_chars_filename,blends,log_filename,ser,db_con,db_cur,page_location_filename)
		
		elif page_location == 'twitter.html':
			serialHandle.grinderCommManager(ser,'complete')
			jsonHandle.updateJson(page_location_filename,'twitter.htm')
		else:
			return
	except Exception, e:
		print e

#add code to declare the state: base or custom
#keep the base pct and pass it in
def letsGrind(coffee_list,blend_chars_filename,blends,log_filename,ser,db_con,db_cur,page_location_filename):
	message = serialHandle.getMessageFromGrinder(ser)
	
	if len(message)>0:
		grinder_pct_list,log_msg,message = parseMessageAndReturnInfo(message)
		print "we've sent and parsed the msg to the grndr"
		try:
			
			if message.startswith('grinderPercentage'):
				print 'in the grinder pct loop'
				print 'grinder_pct_list'
				coffee_dict = jsonHandle.makeJson(grinder_pct_list)
				print 'coffee_dict', coffee_dict
				jsonHandle.updaterOfJsons(blend_chars_filename,'customerPercentages',coffee_dict)
				print 'made the jsons'
				
				#base_pct is a global var
				if sum(grinder_pct_list)>=base_pct:
					print "in the greater than base loop"
					blend_ab_dict={}
					blend_ab_dict['acidity']=blend_dict['acidity']
					blend_ab_dict['body']=blend_dict['body']
					cust_ac,cust_bdy = blendCalc.computeCoffeeChange(grinder_pct_list,base_grinder_pct_list,blend_ab_dict,base_pct)
					print "customer acidity", cust_ac
					print "customer body", cust_bdy
					jsonHandle.updaterOfJsons(blend_chars_filename,'customerAcidity',cust_ac)
					jsonHandle.updaterOfJsons(blend_chars_filename,'customerBody',cust_bdy)
					jsonHandle.updaterOfJsons(blend_chars_filename,'state','custom')
					print "customeracid and body jsons updated and state set to custom"
					
				#base_pct is a global var
				if sum(grinder_pct_list)<base_pct:
					print "in the less than base loop"
					pass
					
				if sum(grinder_pct_list)==100:
					time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					print "in the 100pct grinder pre db insert loop"
					qry = """insert into Orders (order_id,grinder0_pct,grinder1_pct,grinder2_pct,grind_complete)
					VALUES ((select order_id from (select order_id from Orders order by time_created desc limit 1) as x),%f,%f,%f,'%s')
					ON DUPLICATE KEY UPDATE grinder0_pct=VALUES(grinder0_pct), grinder1_pct=VALUES(grinder1_pct),
					grinder2_pct=VALUES(grinder2_pct), grind_complete=VALUES(grind_complete)
					""" % (grinder_pct_list[0],grinder_pct_list[1],grinder_pct_list[2],time)
					
					print "database order qry prepped"
					dbHandle.executeQuery(db_con,db_cur,qry,'insert')
					jsonHandle.updaterOfJsons(blend_chars_filename,'status','readyToBrew')
					print "readytobrew json made"
					qry = 'select name from Customer order by time_created desc limit 1'
					customer_name = dbHandle.executeQuery(db_con,db_cur,qry,'select')
					customer_name = customer_name[0][0]
					tweet_msg = tweetHandle.getTweetInfo(customer_name,blend_dict['name'],coffee_list)
					tweetHandle.tweetIt(tweet_msg)
					print "tweet made"
					#update page status while waiting for redirect
					jsonHandle.updateJson(page_location_filename,'grind.htm')
				
			elif message.startswith('grinderCanister'):
				#add code to update the farm json
				print 'in the canister loop'
				parsed_msg = message.split(' ')
				roaster = int(parsed_msg[1])
				coffee_dict = jsonHandle.getCoffeeJsons(roaster)
				print 'coffee_dict defined'
				jsonHandle.updaterOfJsons(blend_chars_filename,'coffee',coffee_dict)
				print 'coffee json updated'
				jsonHandle.updaterOfJsons(blend_chars_filename,'canister','true')
				print 'canister json updated'
				
			elif message.startswith('noCanister'):
				print 'in the NOcanister loop'
				jsonHandle.updaterOfJsons(blend_chars_filename,'canister','false')
			
			else:
				raise Exception('no matching messages!')
		
		except Exception, e:
			print e
		
		finally:
			logGrinderMessage(log_filename,log_msg)
			#db_cur.close()
			#db_con.close()
			
	else:
		pass	
	
#create a function that gets the most recent id for the customer created, use that throughout the process		
def main():
	
	coffee_list,blends,blend_chars_filename,log_filename,page_location_filename,ser,db_con,db_cur = setup()
	
	while True:
		try:
			stateController(getApplicationState(page_location_filename),page_location_filename,coffee_list,blends,blend_chars_filename,log_filename,ser,db_con,db_cur)
		except Exception, e:
			print e
			
if __name__=='__main__':
	main()