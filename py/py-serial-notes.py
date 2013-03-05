import serial
import io
from datetime import datetime

orderTime = datetime.now.date()
customerOrder = raw_input("What is your selection?")


# receive the serial communication from the arduino
# record which blend was selected (0 = total control, 1-9 blends)
# record when the order was complete
# record 

# Arduino reading in serial data
"""/**
 * Called in between each loop() iteration
 * Reads & stores data for handling. if no
 * data is available, it does nothing. NOTHING!
 */
void serialEvent(){

  while(Serial.available()){

    char in = (char) Serial.read();
    if(in == '\n'){

      inputComplete = true;
    }
    else{

      inputString += in;
    }
  }
}"""

"""
#To receive serial data, you need to start the serial connection as you would to send serial data.
#Then inside loop(), check if any serial data has arrived with Serial.available().
#If data has arrived and is available, store that data in a variable.
#You'll notice that the ASCII value for each character you type is printed out.
int incomingByte = 0;   // for incoming serial data
 
void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}
 
void loop() {
 
        // send data only when you receive data:
        if (Serial.available() > 0) {
                // read the incoming byte:
                incomingByte = Serial.read();
 
                // say what you got:
                Serial.print("I received: ");
                Serial.println(incomingByte, DEC);
        }
}
"""

# listen for certain commands when you recieve them take an action
import serial
from time import sleep

port = "/dev/tty.usbmodem1421"
speed = 9600
polarfile = 'polarfile.out'

f = open(polarfile, 'rw+')

ser = serial.Serial(port, speed, timeout=0)

while True:
	data = ser.readline(9999)
	if len(data) > 0:
		ab.append(data)
	else:
		sleep(0.5)

    sleep(1)

ser.close()


port = "/dev/tty.usbmodem1421"
speed = 9600

ser = serial.Serial(port,speed)
ser.isOpen()
while True:
	print ser.readline().strip()









