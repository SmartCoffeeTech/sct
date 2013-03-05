import twitter
import config as cfg
import serial
import MySQLdb as sql
import json
import random
from time import sleep
from datetime import datetime
import collections

def setupSerial():
	port = "/dev/tty.usbmodem1421"
	speed = 9600
	ser = serial.Serial(port,speed)
	return ser

def getMessageFromGrinder(ser):
	if ser.isOpen() is True:
		while True:
			return ser.readline().strip()
	else:
		print 'Serial is closed'
		
def getMessag():
	return 'grinderPercentage 0.00 0.00 36.00'
	

def messageReceived(message):
	if len(message)>0:
		return True
	else:
		print 'Empty msg received from Arduino'
		
def getTweetInfo(customer_name,blend_name,coffee_list):
	if blend_name in coffee_list:
		blend_name = blend_name + ' Single Origin'
	else:
		blend_name = blend_name + ' blend'
		
	tweet = '%s made a cup of the %s w/ the @BuildaBrew platform #coffee #tech. To learn more http://bit.ly/14X7wxa' % (customer_name,blend_name)
	return tweet
	
		
def tweetIt(tweet_msg):
	my_auth = twitter.OAuth(cfg.TOKEN,cfg.TOKEN_KEY,cfg.CON_SEC,cfg.CON_SEC_KEY)
	twit = twitter.Twitter(auth=my_auth)
	twit.statuses.update(status=tweet_msg)
	print 'tweeted'
	 
def setupDb():
	db = sql.connect(user="root",passwd="sct",db="sct")
	cursor = db.cursor()
	return db,cursor
	

def makeJson(coffee_list,grinder_pct_list,blend_name):
	coffeeDict =  dict(zip(coffee_list,grinder_pct_list))
	coffeeDict = collections.OrderedDict(sorted(coffeeDict.items()))
	coffeeDict["blendRecipe"]=blend_name
	coffeeDict["grinderPercentage0"]=grinder_pct_list[0]
	coffeeDict["grinderPercentage1"]=grinder_pct_list[1]
	coffeeDict["grinderPercentage2"]=grinder_pct_list[2]
	coffeeDict["status"]='grinding'
	
	'''
	coffeeDict = {
    "blendRecipe": blend_name,
    "grinderPercentage0": grinder_pct_list[0],
	"grinderPercentage1": grinder_pct_list[1],
	"grinderPercentage2": grinder_pct_list[2],
	coffee_list[0]: grinder_pct_list[0],
	coffee_list[1]: grinder_pct_list[1],
	coffee_list[2]: grinder_pct_list[2],
	"status":'grinding'
	}
	'''
	
	return coffeeDict
	
def updateJson(filename,status):
	file = open(filename,'r+b')
	coffeeDict = json.loads(file.readline())
	coffeeDict['status']=status
	jsonData = json.dumps(coffeeDict)
	
	#pointer to the beginning of the file
	file.seek(0)
	file.truncate()
    #now update and close the file
	file.write(jsonData)
	file.close()
	
def resetJsonFile(filename):
	file = open(filename,'w+')
	file.close()
	
def postJsonToServer(filename,coffeeDict):
	file = open(filename,'w+')
	file.write(json.dumps(coffeeDict))
	file.close()
	
def writeToDb(db_cur,db_con,order_id,customer_id,grinder_pct_list,time):
	
	msg = """INSERT INTO Orders (order_id,customer_id,grinder0_pct,grinder1_pct,grinder2_pct,grind_complete) 
	VALUES (%d,%d,%s,%s,%s,'%s') ON DUPLICATE KEY UPDATE grinder0_pct=VALUES(grinder0_pct),grinder1_pct=VALUES(grinder1_pct),
	grinder2_pct=VALUES(grinder2_pct), grind_complete=VALUES(grind_complete)""" \
	% (order_id,customer_id,grinder_pct_list[0],grinder_pct_list[1],grinder_pct_list[2],time)
	
	db_cur.execute(msg)
	db_con.commit()


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
	

def getFromDb(db_cur):
	query = """Select customer_id,order_id,name,blend_name from Orders o join Blend using(blend_id)
	join Customer using(customer_id) order by o.time_created desc limit 1"""
	db_cur.execute(query)
	result = db_cur.fetchone()
	
	return int(result[0]),int(result[1]),str(result[2]),str(result[3])
	
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
	
	blend_filename = 'dataout1.json'
	log_filename = 'grinder.log'
	
	#setup the connections(grinder and db) and get the latest customer created from the web interface
	ser = setupSerial()
	db_con,db_cur = setupDb()
	
	coffee_list = setupCoffeeList(db_con,db_cur)
	
	return coffee_list,blend_filename,log_filename,ser,db_con,db_cur
	
def letsGrind(coffee_list,blend_filename,log_filename,ser,db_con,db_cur):
	#get the message from the grinder - over serial for now
	#message = getMessag()
	message = getMessageFromGrinder(ser)
	
	#figure out what to do with that message
	if messageReceived(message) is True:
		grinder_pct_list,log_msg,grinder_status = parseMessageAndReturnInfo(message)
		
		try:
			
			if grinder_status.startswith('grind'):
				customer_id,order_id,customer_name,blend_name = getFromDb(db_cur)
				coffee_dict = makeJson(coffee_list,grinder_pct_list,blend_name)
				postJsonToServer(blend_filename,coffee_dict)
				
				if sum(grinder_pct_list)==100:
					time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					customer_id,order_id,customer_name,blend_name = getFromDb(db_cur)
					writeToDb(db_cur,db_con,order_id,customer_id,grinder_pct_list,time)
					updateJson(blend_filename,'readyToBrew')
					tweet_msg = getTweetInfo(customer_name,blend_name,coffee_list)
					tweetIt(tweet_msg)
				
			elif grinder_status.startswith('comp'):
				updateJson(blend_filename,'complete')
				
			elif grinder_status.startswith('reset'):
				resetJsonFile(blend_filename)
				
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