#import serial
import serialHandle
#import MySQLdb as sql dbHandle imports it
import dbHandle
#import json
import jsonManager as jaysohn
#import random
#from time import sleep
import tweetHandle
from datetime import datetime
#import collections
import blendSuggestionCalculator



def parseMessageAndReturnInfo(message):
	
	if message.startswith('grinder'):
		parsed_msg = message.split(' ')
		grind_pct_list = [float(parsed_msg[1]),float(parsed_msg[2]),float(parsed_msg[3])]
		log_msg = str(parsed_msg[0]) + "|" + str(parsed_msg[1]) + "|" + str(parsed_msg[2]) +  "|" + str(parsed_msg[3]) + "|" + str(datetime.now())
		grinder_status = log_msg[0:5]
		return grind_pct_list,log_msg,grinder_status
		
	elif message.startswith('comp') or message.startswith('reset'):
		parsed_msg = message.split(' ')
		grind_pct_list = ['0','0','0']
		log_msg = str(parsed_msg[0]) + "|" + str( datetime.now())
		grinder_status = log_msg[0:5]
		return grind_pct_list,log_msg,grinder_status
		
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
	blend_filename = 'dataout1.json'
	log_filename = '../log/grinder.log'
	
	#setup the connections(grinder and db) and get the latest customer created from the web interface
	ser = serialHandle.setupSerial()
	db_con,db_cur = dbHandle.openDbConnection()
	
	coffee_list = setupCoffeeList(db_con,db_cur)
	return coffee_list,blend_filename,log_filename,ser,db_con,db_cur
	
def letsGrind(coffee_list,blend_filename,log_filename,ser,db_con,db_cur):
	#get the message from the grinder - over serial for now
	#message = getMessag()
	serialHandle.grinderInit(ser)
	
	#need a function that gets some data
	dbHandle.executeDbQuery(db_con,db_cur,query,'select')
	
	#figure out what to do with that message
	if grinderCommManager(ser,msg_to_grinder).startswith():
		grinder_pct_list,log_msg,grinder_status = parseMessageAndReturnInfo(message)
		
		try:
			
			if grinder_status.startswith('grind'):
				customer_id,order_id,customer_name,blend_name = dbHandle.executeDbQuery(db_con,db_cur,query,'select')
				coffee_dict = jaysohn.makeJson(coffee_list,grinder_pct_list,blend_name)
				jaysohn.postJsonToServer(blend_filename,coffee_dict)
				
				if sum(grinder_pct_list)==100:
					serialHandle.sendMesageToGrinder(ser,'complete')
					time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					customer_id,order_id,customer_name,blend_name = getFromDb(db_cur)
					dbHandle.executeDbQuery(db_cur,db_con,order_id,customer_id,grinder_pct_list,time)
					jaysohn.updateJson(blend_filename,'readyToBrew')
					tweet_msg = tweetHandle.getTweetInfo(customer_name,blend_name,coffee_list)
					tweetHandle.tweetIt(tweet_msg)
				
			elif grinder_status.startswith('comp'):
				jaysohn.updateJson(blend_filename,'complete')
				
			elif grinder_status.startswith('reset'):
				jaysohn.resetJsonFile(blend_filename)
				
		finally:
			logGrinderMessage(log_filename,log_msg)
			#db_cur.close()
			#db_con.close()
			
	else:
		pass	
	
#create a function that gets the most recent id for the customer created, use that throughout the process		
def main():
	
	coffee_list,blend_filename,log_filename,ser,db_con,db_cur = setup()
	
	while True:
		letsGrind(coffee_list,blend_filename,log_filename,ser,db_con,db_cur)
	
if __name__=='__main__':
	main()