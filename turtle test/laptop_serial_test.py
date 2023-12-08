import math
from datetime import datetime, timedelta
import serial
from turtle import * # https://docs.python.org/3/library/turtle.html
import keyboard_input

# === setup Serial port readings ===
COM_PORT = 'COM6'
BAUDRATE = 9600
SER_TIMEOUT = 0.04

ser = serial.Serial(port=COM_PORT, baudrate=BAUDRATE, timeout=SER_TIMEOUT)

# === setup turtle screen ===
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)

# === setup Serial port variables and how often we call turtle and print variables to terminal ===
x_pot = 512   # pots can have values between 0 and 1023
y_pot = 512
speed_pot = 512
pot_set = [False, False, False]

turtle_time = datetime.now()
turtle_freq = 0.1   # how often do we call turtle()?

print_time = datetime.now()
print_freq = 1.25   # how often do you want to print the outputs?

# === main loop takes input from serial port ===
def mainloop():
    turtle_x = 0
    turtle_y = 0
    with keyboard_input.KeyPoller() as keyPoller:
        while True:
            c = keyPoller.poll()
            if not c is None:
                print(c)
                keyboardinput(c)

            read_serial = ser.readline()
            data = read_serial.decode().strip()
            
            if data:
                data_split = data.split(' ')
                setpots(data_split)
                
                global turtle_time
                global pot_set
                if all(pot_set) and datetime.now() > turtle_time + timedelta(seconds=turtle_freq):
                    for elem in pot_set:
                        elem = False
                    turtle_time = datetime.now()
                    turtle_x, turtle_y = turtle()
                    # ser.readlines() # dequeue all serial outputs

                global print_time
                if datetime.now() > print_time + timedelta(seconds=print_freq):
                    print_time = datetime.now()
                    x_print = "Horiz: " + str(x_pot)
                    y_print = "Vert: " + str(y_pot)
                    speed_print = "Speed: " + str(speed_pot)
                    turt_x = "Turtle X: " + str(round(turtle_x, 2))
                    turt_y = "Turtle Y: " + str(round(turtle_y, 2))
                    print(" %-25s %-25s %-25s %-25s %-25s" % (x_print, y_print, speed_print, turt_x, turt_y))

def setpots(data_split):
    global pot_set
    if data_split[0] == "Horiz:":
        try:
            global x_pot
            x_pot = int(data_split[1])
            pot_set[0] = True
            return
        except:
            temp = 4 # do nothing
    elif data_split[0] == "Vert:":
        try:
            global y_pot
            y_pot = int(data_split[1])
            pot_set[1] = True
            return
        except:
            temp = 4
    elif data_split[0] == "Speed:":
        try:
            global speed_pot
            speed_pot = int(data_split[1])
            pot_set[2] = True
            return
        except:
            temp = 4
    else:
        print("reconsider life")
    return

def keyboardinput(s):
    s = s.lower()
    if s == "c":
        clearscreen()   # clear screen but do not move turtle
    elif s == "r":
        clearscreen()   # reset both screen and turtle position
        home()
    elif s == "d":
        if isdown():    # toggle turtle up or down
            up()
        else:
            down()


def set_degrees(x, y):
    if x == 0:
        if y == 0:
            return 0
        else:
            angle = 90 if y > 0 else 270
            return angle
    elif y == 0:
        angle = 0 if x > 0 else 180
        return angle
    
    angle = math.degrees(math.atan(y / x))

    if x < 0:   # atan returns q4 when should be q2 and q1 when should be q3
        return angle + 180
    elif y > 0: # correctly in q1
        return angle
    else:       # returns q4, just add 360 so it's positive
        return angle + 360


def turtle():
    x = x_pot - 512     # cut in half so values are between -512 and 512
    y = y_pot - 512     # use temp variables so they don't get modified by serial (idk if it's an async process)


    distance = speed_pot * 0.005

    angle = set_degrees(x, y)
    if x == 0 and y == 0:
        distance = 0

    setheading(angle)
    forward(distance)

    x,y = position() # make sure turtle is within bounds
    if not -SCREEN_WIDTH / 2 < x < SCREEN_WIDTH / 2 or not -SCREEN_HEIGHT / 2 < y < SCREEN_HEIGHT / 2:
        undo()  # undo error

    return x, y


mainloop()