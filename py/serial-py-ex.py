## import the serial library
import serial

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

def sendMesageToGrinder(ser,msg):
	## Tell the arduino to blink!
	ser.write(msg)


msg = 'basePercentage 33'
msg2 = 'blend 20 10 3'
msg3 = 'complete'
msg4 = 'reset'
ser = setupSerial()

print getMessageFromGrinder(ser) #read
sendMesageToGrinder(ser,msg)
print getMessageFromGrinder(ser) # equals the msg just sent
sendMesageToGrinder(ser,msg2) 
print getMessageFromGrinder(ser) #validSum
sendMesageToGrinder(ser,msg3)
print getMessageFromGrinder(ser)
sendMesageToGrinder(ser,msg4)
print getMessageFromGrinder(ser)



'''
arduino sends to me:
ready
send to arduino:
basePercentage 33 (check this value in python handshake)
blend 20 10 3

complete
reset

arduino sends to me:
basePercentage 33 (check this value in python handshake)
validSum

on error:
invalidProtocol
invalidSum (resend blend 20 10 3)'''