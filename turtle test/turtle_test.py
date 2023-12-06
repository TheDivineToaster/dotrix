from turtle import *

forward(100)
left(120)
forward(100)
left(120)
forward(100)

for steps in range(100):
    for c in ('blue', 'red', 'green'):
        color(c)
        forward(steps)
        right(30)