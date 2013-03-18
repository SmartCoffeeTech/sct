import serialHandle
import dbHandle
import jsonManager as jsonHandle
import tweetHandle
from datetime import datetime
import blendSuggestionCalculator as blendCalc
import json


def parseMessageAndReturnInfo(message):
	
	if message.startswith('grinder'):
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
	
	if serialHandle.grinderInit(ser, 'ready')=='arduinoReady':
		return coffee_list,blends,blend_chars_filename,log_filename,page_location_filename,ser,db_con,db_cur
	else:
		return 'arduino setup failed'
		
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

def stateController(page_location,coffee_list,blends,blend_chars_filename,log_filename,ser,db_con,db_cur):
	# coffee_list,blends,blend_chars_filename,log_filename,page_location_filename,ser,db_con,db_cur
	""" directs python based on the state of the web application. theCondutor"""
	try:
		if page_location in ['index1.html','blend-selection.html']:
			return
		elif page_location == 'base-blend.html':
			# run once
			#get cust1 from the db
			qry = 'select order_id,taste_profile from Orders order by time_created desc limit 1'
			result = dbHandle.executeQuery(db_con,db_cur,qry,'select')
			cust1 = json.loads(result[0][1])
			blend_name = blendCalc.computeCoffeeBlendSuggestion(blends,cust1)
			qry = """update Orders set blend_id=(Select blend_id from Blend where blend_name='%s' where order_id=%d limit 1)""" % (blend_name,int(result[0][0]))
			dbHandle.executeQuery(db_con,db_cur,qry,'insert')
			blend_dict = getBlendDict(blend_name,blends)
			aroma_dict = blendCalc.computeTop3Aromas(blend_dict)
			aroma_json = jsonHandle.makerOfJsons(aroma_dict,'blend')
			jsonHandle.postJsonToServer(blend_chars_filename,aroma_json)
			jsonHandle.updateJson(page_location_filename,'base-blend.htm','status')
			return
		elif page_location == 'grinding.html':
			base_grinder_pct_list=[]
			qry = 'select customization_pct from Orders order by time_created desc limit 1'
			custom_pct = dbHandle.executeQuery(db_con,db_cur,qry,'select')
			custom_pct = int(cust1[0][0])
			blend_name = blendCalc.computeCoffeeBlendSuggestion(blends,cust1)
			qry = """select grinder,coffee_pct from Orders join Blend using(blend_id) join Coffee using(coffee_id) where order_id=(select order_id from Orders order by time_created desc limit 1) order by grinder"""
			result = dbHandle.executeQuery(db_con,db_cur,qry,'select')
			for each in result:
				base_grinder_pct_list.append(int(each[1]))
			base_grinder_pct_list = blendCalc.computeBlendPct(base_grinder_pct_list,custom_pct)
			letsGrind(coffee_list,base_grinder_pct_list,blend_chars_filename,log_filename,ser,db_con,db_cur)
		
		elif page_location == 'twitter.html':
			serialHandle.grinderCommManager(ser,'complete')
		else:
			return
	except Exception, e:
		print e
	
def letsGrind(coffee_list,base_grinder_pct_list,blend_chars_filename,log_filename,ser,db_con,db_cur):
	#get the message from the grinder - over serial for now
	#message = getMessag()
	
	#need a function that gets some data
	#where does the query var get populated
	#dbHandle.executeQuery(db_con,db_cur,query,'select')
	
	#send the base_pct
	base_pct = sum(base_grinder_pct_list)
	msg_to_grinder = 'basePercentage '+str(base_pct)
	#figure out what to do with that message
	serialHandle.grinderCommManager(ser,msg_to_grinder)
	
	#send the grinder pct values
	msg_to_grinder = 'blend ' + str(base_grinder_pct_list[0]) + str(base_grinder_pct_list[1]) + str(base_grinder_pct_list[2])
	serialHandle.grinderCommManager(ser,msg_to_grinder)
	grinder_pct_list,log_msg,message = parseMessageAndReturnInfo(message)
		
		try:
			
			if message.startswith('grinderPercentage'):
				#customer_id,order_id,customer_name,blend_name = dbHandle.executeQuery(db_con,db_cur,query,'select')
				coffee_dict = jsonHandle.makeJson(grinder_pct_list)
				#add in code to build the new json during grinding
				jsonHandle.updaterOfJsons(blend_chars_filename,'customer',coffee_dict)
				
				if sum(grinder_pct_list)==100:
					time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					customer_id,order_id,customer_name,blend_name = getFromDb(db_cur)
					qry = """insert into Orders (order_id,customer_id,grinder0_pct,grinder1_pct,grinder2_pct,grind_complete) VALUES (%d,%d,%f,'%s') ON DUPLICATE KEY UPDATE grinder0_pct=VALUES(grinder0_pct), grinder1_pct=VALUES(grinder1_pct), grinder2_pct=VALUES(grinder2_pct), grind_complete=VALUES(grind_complete)""" % (order_id,customer_id,grinder_pct_list[0],grinder_pct_list[1],grinder_pct_list[2],time)
					dbHandle.executeQuery(db_cur,db_con,qry,'insert')
					jsonHandle.updaterOfJsons(blend_chars_filename,'status','readyToBrew')
					tweet_msg = tweetHandle.getTweetInfo(customer_name,blend_name,coffee_list)
					tweetHandle.tweetIt(tweet_msg)
					jsonHandle.updateJson(page_location_filename,'grinding.htm','status')
				
			elif message.startswith('grinderCanister'):
				#add code to update the farm json
				roaster = message[1]
				coffee_dict = jsonHandle.getCoffeeJsons(roaster)
				jsonHandle.updaterOfJsons(blend_chars_filename,'coffee',coffee_dict)
				jsonHandle.updaterOfJsons(blend_chars_filename,'canister','true')
				
			elif message.startswith('noCanister'):
				jsonHandle.updatetOfJsons(blend_chars_filename,'canister','false')
			
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
			stateController(getApplicationState(page_location_filename),coffee_list,blends,blend_chars_filename,log_filename,ser,db_con,db_cur)
		except Exception, e:
			print e
			
if __name__=='__main__':
	main()