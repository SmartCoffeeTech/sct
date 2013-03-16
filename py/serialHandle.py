import serial
from time import sleep

def getSerialPort():
	for each_file in os.listdir("/dev"):
		if each_file.startswith('tty.usb'):
			return '/dev/' + each_file

def setupSerial():
	port = getSerialPort()
	speed = 9600
	ser = serial.Serial(port,speed)
	return ser

def getMessageFromGrinder(ser):
	if ser.isOpen() is True:
		while True:
			return ser.readline().strip()
	else:
		print 'Serial is closed'
		
def sendMessageToGrinder(ser,msg):
	ser.write(msg)

def messageReceived(message):
	if len(message)>0:
		return True
	else:
		print 'Empty msg received from Arduino'
		
if __name__=='__main__':
	main()

msg = 'basePercentage 33'
msg2 = 'blend 20 10 3'
msg3 = 'complete'
msg4 = 'reset'
msg5 = 'grinderCanister 0'
msg6 = 'noCanister'

# update so that arduino returns ready even if i send it twice
# case arduino got ready, but for some reason returns an invalid msg
# sending reading twice or 20 times is ok, failure in system but should not hold anything up


def grinderInit(ser):
	try:
		if getMessageFromGrinder(ser).startswith('ready'):
			return 'arduinoReady'
		else:
			raise Exception('not ready')
	except Exception, e:
		print e
		sleep(.7)
		grinderInit(ser)
		
def grinderCommManager(ser,msg_to_grinder):
	try:
		sendMessageToGrinder(ser,msg_to_grinder)
		if getMessageFromGrinder(ser)==msg_to_grinder:
			return
		else:
			raise Exception("invalid message")
	except Exception, e:
		print e
		sleep(.1)
		grinderCommManager(ser,msg_to_grinder)

if grinderInit(ser,'ready')=='arduinoReady':
	#wait for php to send a message
	#when they indicate how much customization they want
	#20,40,60 or 100
	msg_to_grinder = getValueFromDbOrJson()
	if msg_to_grinder.startswith('basePercentage'):
		# 'basePercentage 33'
		grinderCommManager(ser,msg_to_grinder)
		msg_to_grinder = 'blend 20 10 3'
		grinderCommManager(ser,msg_to_grinder)
		
	msg_to_grinder = getValueFromDbOrJson()
	# 'blend 20 10 3'
	grinderCommManager(ser,msg_to_grinder)
	#if sum == 100 'complete'
	grinderCommManager(ser,msg_to_grinder)
	#wait a bit then 'reset'
	grinderCommManager(ser,msg_to_grinder)
	
'Handshake: always return message sent'

#on invalid message return what was expected	
'expecting basePercentage'
'expecting blend'
'expecting complete'
'expecting reset'
'expecting ready'

getMessageFromGrinder(ser)
	
if grinderCommManager(msg).startswith('ready'):
	
else if grinderCommManager(msg).startswith('basePercentage'):
	
else if grinderCommManager(msg).startswith('blend'):
	
else if grinderCommManager(msg).startswith('complete'):
	
	
	

	