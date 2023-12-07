import math
from datetime import datetime, timedelta
import serial
from turtle import * # https://docs.python.org/3/library/turtle.html

COM_PORT = 'COM6'
BAUDRATE = 9600

global x_pot
x_pot = 0   # can have values between 0 and 1023
global y_pot
y_pot = 0
global speed_pot
speed_pot = 0


ser = serial.Serial(COM_PORT, BAUDRATE)
s = [0,1]

global turtle_time
turtle_time = datetime.now()
turtle_freq = 0.1

global print_freq
print_freq = 0.75 #how often do you want to print the outputs?

def mainloop():
    print_now = datetime.now()
    while True:
        read_serial = ser.readline()
        data = read_serial.decode().strip()

        data_split = data.split(' ')

        setpots(data_split)
        
        if datetime.now() > turtle_time + timedelta(seconds=turtle_freq):
            turtle()


        if datetime.now() > print_now + timedelta(seconds=print_freq):
            print_now = datetime.now()
            x_print = "Horiz: " + str(x_pot)
            y_print = "Vert: " + str(y_pot)
            speed_print = "Speed: " + str(speed_pot)
            #print(f"{x_print : <25}{y_print : ^25}{speed_print : }") 
            print(" %-25s %-25s %-25s" % (x_print, y_print, speed_print))

def setpots(data_split):
    if data_split[0] == "Horiz:":
        try:
            global x_pot
            x_pot = int(data_split[1])
            return
        except:
            temp = 4 # do nothing
    elif data_split[0] == "Vert:":
        try:
            global y_pot
            y_pot = int(data_split[1])
            return
        except:
            temp = 4
    elif data_split[0] == "Speed:":
        try:
            global speed_pot
            speed_pot = int(data_split[1])
            return
        except:
            temp = 4
    else:
        print("reconsider life")
    return


def turtle():
    x = x_pot - 512     # cut in half so values are between -512 and 512
    y = y_pot - 512     # use temp variables so they don't get modified by serial (idk if it's an async process)

    q1 = True
    if (x < 0):
        q1 = False

    distance = speed_pot * 0.00125

    angle = math.degrees(math.atan(x / y))

    if (q1):
        angle += 180

    setheading(angle)
    forward(distance)


    # mainloop should dissect the input and separate into x and y values
    # here, turtle should take the x and y values and set heading as well as speed
    # auto change color for funsies ig


mainloop()