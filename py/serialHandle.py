import serial
from time import sleep
import os

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


def testMessages():
	msg = 'basePercentage 33'
	msg2 = 'blend 20 10 3'
	msg3 = 'complete'
	msg4 = 'reset'
	msg5 = 'grinderCanister 0'
	msg6 = 'noCanister'

def grinderInit(ser):
	try:
		if getMessageFromGrinder(ser).startswith('ready'):
			print 'ready'
			return 'arduinoReady'
		else:
			raise Exception('not ready')
	except Exception, e:
		print e
		sleep(1)
		grinderInit(ser)
		
def grinderCommManager(ser,msg_to_grinder):
	try:
		sendMessageToGrinder(ser,msg_to_grinder)
		msg_from_grinder = getMessageFromGrinder(ser)
		
		if msg_from_grinder==msg_to_grinder:
			print 'ok msg_to_grinder', msg_to_grinder
			print 'ok msg_from_grinder', msg_from_grinder
			return
		else:
			print 'fail msg_to_grinder', msg_to_grinder
			print 'fail msg_from_grinder', msg_from_grinder
			raise Exception("invalid message")
	except Exception, e:
		print e
		sleep(.1)
		grinderCommManager(ser,msg_to_grinder)
	
def messageReceived(message):
	if len(message)>0:
		return True
	else:
		print 'Empty msg received from Arduino'

if __name__=='__main__':
	main()
	

	