import math
from datetime import datetime, timedelta
import serial
from turtle import * # https://docs.python.org/3/library/turtle.html

COM_PORT = 'COM6'
BAUDRATE = 9600

x_pot = 0   # can have values between 0 and 1023
y_pot = 0
speed_pot = 0


ser = serial.Serial(COM_PORT, BAUDRATE)
s = [0,1]

now = datetime.now()
freq = 2 #how often do you want to print the outputs?

def mainloop():
    now = datetime.now()
    while True:
        read_serial = ser.readline()
        data = read_serial.decode().strip()
        parsedata(data)
        if datetime.now() > now + timedelta(seconds=freq):
            now = datetime.now()
            x_print = "Vert: " + str(x_pot)
            y_print = "Horiz: " + str(y_pot)
            speed_print = "Speed: " + str(speed_pot)
            #print(f"{x_print : <25}{y_print : ^25}{speed_print : }") 
            print(" %-25s %-25s %-25s" % (x_print, y_print, speed_print))


def parsedata(data):
    data_split = data.split(' ')
    if data_split[0] == "Vert:":
        y_pot = int(data_split[1])
        return
    elif data_split[0] == "Horiz:":
        x_pot = int(data_split[1])
        return
    elif data_split[0] == "Speed:":
        speed_pot = int(data_split[1])
        return
    else:
        print("reconsider your life")
        return

def turtle():
    x = x_pot - 512     # cut in half so values are between -512 and 512
    y = y_pot - 512     # use temp variables so they don't get modified by serial (idk if it's an async process)

    q1 = True
    if (x < 0):
        q1 = False

    distance = speed * 0.125

    x /= 512
    y /= 512

    angle = math.degrees(math.atan(x / y))

    if (q1):
        angle += 180

    setheading(angle)
    forward(distance)


    # mainloop should dissect the input and separate into x and y values
    # here, turtle should take the x and y values and set heading as well as speed
    # auto change color for funsies ig


mainloop()