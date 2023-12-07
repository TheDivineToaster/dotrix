# Just connect Arduino USB Plug to Raspberry PI with USB cable
# check the connection between Arduino and Raspberry pi by typing "ls /dev/tty*" in Raspberry Pi terminal
# the result should be content "/dev/ttyACM0" and you are good to go. 

import serial

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0,1]
while True:
	read_serial=ser.readline()
	s[0] = str(int (ser.readline(),16))
	print (s[0])
	print (read_serial)
