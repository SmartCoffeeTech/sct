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
		grinder_status = log_msg[0:5]
		return grind_pct_list,log_msg,grinder_status
	# no longer get these messages
	'''
	elif message.startswith('comp') or message.startswith('reset'):
		parsed_msg = message.split(' ')
		grind_pct_list = ['0','0','0']
		log_msg = str(parsed_msg[0]) + "|" + str( datetime.now())
		grinder_status = log_msg[0:5]
		return grind_pct_list,log_msg,grinder_status
		'''
	else:
		print "Failure. did not receive an expected value! I got: %s" % message

	
def logGrinderMessage(filename,message):
	file = open(filename,'a')
	message += ' \n'
	file.write(message)
	file.close()
	
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
	blend_filename = '../www/data/dataout1.json'
	blend_chars_filename = '../www/data/dataout2.json'
	log_filename = '../log/grinder.log'
	page_location_filename = '../www/data/page_location.json'
	
	#initalize blend jsons - next iter move to db
	blends = blendCalc.initData('blend')
	#setup the connections(grinder and db) and get the latest customer created from the web interface
	ser = serialHandle.setupSerial()
	#setup db conns
	db_con,db_cur = dbHandle.openDbConnection()
	#setup coffe list - needed?
	coffee_list = setupCoffeeList(db_con,db_cur)
	
	if serialHandle.grinderInit(ser, 'ready')=='arduinoReady':
		return base_blend_calls,coffee_list,blends,blend_filename,blend_chars_filename,log_filename,page_location_filename,ser,db_con,db_cur
	else:
		return 'arduino setup failed'
		
def getTheBlendDict(blend_name,blends):
	for each_dict in blends:
		if each_dict['name']==blend_name:
			return each_dict
		else:
			'No blend_name matches, you sir, are fucked.'
	
def getApplicationState(filename):
	page_location = jsonHandle.readJson(filename)
	page_location = page_location['status']
	return page_location

def stateController(base_blend_calls,page_location,coffee_list,blends,blend_filename,blend_chars_filename,log_filename,ser,db_con,db_cur):
	# coffee_list,blends,blend_filename,blend_chars_filename,log_filename,page_location_filename,ser,db_con,db_cur
	""" directs python based on the state of the web application. theCondutor"""
	if page_location in ['index1.html','blend-selection.html']:
		return
	elif page_location == 'base-blend.html':
		# run once
		blend_name = blendCalc.computeCoffeeBlendSuggestion(blends,cust1)
		blend_dict = getTheBlendDict(blend_name,blends)
		aroma_dict = blendCalc.computeTop3Aromas(blend_dict)
		aroma_json = jsonHandle.makerOfJsons(aroma_dict,'blend')
		jsonHandle.postJsonToServer(blend_chars_filename,aroma_json)
		jsonHandle.updateJson(page_location_filename,'base-blend.htm','status')
		return
	elif page_location == 'grinding.html':
		letsGrind(coffee_list,blend_filename,log_filename,ser,db_con,db_cur)
	elif page_location == 'brewing.html':
		return
	elif page_location == 'twitter.html':
		letsGrind(coffee_list,blend_filename,log_filename,ser,db_con,db_cur)
	else:
		return
	
	
def letsGrind(coffee_list,blend_filename,log_filename,ser,db_con,db_cur):
	#get the message from the grinder - over serial for now
	#message = getMessag()
	
	#need a function that gets some data
	dbHandle.executeDbQuery(db_con,db_cur,query,'select')
	
	#figure out what to do with that message
	if grinderCommManager(ser,msg_to_grinder) is True:
		grinder_pct_list,log_msg,grinder_status = parseMessageAndReturnInfo(message)
		
		try:
			
			if grinder_status.startswith('grind'):
				customer_id,order_id,customer_name,blend_name = dbHandle.executeDbQuery(db_con,db_cur,query,'select')
				coffee_dict = jsonHandle.makeJson(coffee_list,grinder_pct_list,blend_name)
				#add in code to build the new json during grinding
				jsonHandle.updaterOfJsons(blend_chars_filename,coffee_dict)
				jsonHandle.postJsonToServer(blend_filename,coffee_dict)
				
				if sum(grinder_pct_list)==100:
					serialHandle.sendMesageToGrinder(ser,'complete')
					time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					customer_id,order_id,customer_name,blend_name = getFromDb(db_cur)
					dbHandle.executeDbQuery(db_cur,db_con,order_id,customer_id,grinder_pct_list,time)
					jsonHandle.updateJson(blend_filename,'readyToBrew')
					tweet_msg = tweetHandle.getTweetInfo(customer_name,blend_name,coffee_list)
					tweetHandle.tweetIt(tweet_msg)
				
			elif grinder_status.startswith('canisterG'):
				jsonHandle.updateJson(status,'canisterGrinder0')
				
			elif grinder_status.startswith('noCanister'):
				jsonHandle.updateJson(status,'noCanister')
				
			elif grinder_status.startswith('comp'):
				jsonHandle.updateJson(blend_filename,'complete')
				
			elif grinder_status.startswith('reset'):
				jsonHandle.resetJsonFile(blend_filename)
				
		finally:
			logGrinderMessage(log_filename,log_msg)
			#db_cur.close()
			#db_con.close()
			
	else:
		pass	
	
#create a function that gets the most recent id for the customer created, use that throughout the process		
def main():
	
	coffee_list,blends,blend_filename,blend_chars_filename,log_filename,page_location_filename,ser,db_con,db_cur = setup()
	
	while True:
		stateController(getApplicationState(page_location_filename),coffee_list,blends,blend_filename,blend_chars_filename,log_filename,ser,db_con,db_cur)
	
if __name__=='__main__':
	main()