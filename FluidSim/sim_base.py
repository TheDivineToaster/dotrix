import numpy
from rock_paper_scissors import RockPaperScissors
from fluid_sim import FluidSim

'''Thoughts here are that this script acts as the pygame interpreter, 
and we have other scripts to control different ways to mess with the image.
like fluid sim or cellular automata'''


# Constants
WIDTH, HEIGHT = 123, 48 # number of "LEDs" on the screen
pixels_per_led = 10
FPS = 60    # base fps value, each game should have their own


# Choose which sim we use
game_select = numpy.random.randint(0,1) # inclusive
game_select = 1 # hard set to test TODO: REMOVE THIS
if (game_select == 0):
    game = RockPaperScissors(WIDTH, HEIGHT, pixels_per_led, 4, FPS=2) # grid size and number of colors
elif (game_select == 1):
    game = FluidSim(WIDTH, HEIGHT, pixels_per_led, FPS=60)


