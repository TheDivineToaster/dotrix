import numpy
from multi_state_life_sim import MultiStateLife
import fluid_sim     # ambiguous naming scheme, settle on one sim
from game_of_life_sim import GameOfLife
from magma_sim import MagmaSim
import Fluidsimtest1 # ambiguous naming scheme, settle on one sim

'''Thoughts here are that this script acts as the pygame interpreter, 
and we have other scripts to control different ways to mess with the image.
like fluid sim or cellular automata'''


# Constants
WIDTH, HEIGHT = 123, 48 # number of "LEDs" on the screen
pixels_per_led = 10
FPS = 60    # base fps value, each game should have their own


# Choose which sim we use
game_select = numpy.random.randint(0,4) # inclusive
game_select = 5 # hard set to test TODO: REMOVE THIS

# --- RockPaperScissors/MultiStateLife --- #
if (game_select == 0):
    FPS = 10
    nh = 'Moore'
    threshold = 3
    rules_select = numpy.random.randint(0,2) # inclusive
    rules_select = 2 # hard set to test TODO: REMOVE THIS

    if (rules_select == 0): # 3-state (normal Rock Paper Scissor)
        rules = {0: [2], 1: [0], 2: [1]}
    elif (rules_select ==1): # 4-state (unbalanced)
        rules = {1: [4], 2: [1], 3: [1, 2], 4: [2, 3]}
    else: # (rules_select==2): # 5-state (balanced)
        rules = {1: [4, 5], 2: [1, 5], 3: [1, 2], 4: [2, 3], 5: [3, 4]}
    game = MultiStateLife(size_x=WIDTH, size_y=HEIGHT, pixels_per_led=pixels_per_led, FPS=FPS,
                          neighbor_rules=nh, rules=rules, threshold=threshold)
# --- Fluid Sim --- #
elif (game_select == 1):
    game = fluid_sim.FluidSim(size_x=WIDTH, size_y=HEIGHT, duration=200)
    game.main()

# --- Basic Game of Life --- #
elif (game_select == 2):
    FPS = 10
    # game rules
    B = [3]
    S = [2, 3]
    nh = 'Moore'
    starting_density = 0.6
    # run game of life
    game = GameOfLife(size_x=WIDTH, size_y=HEIGHT, FPSs=FPS, B=B, S=S, nh=nh,
                      cell_size=pixels_per_led, starting_density=starting_density, run_main=True)

# --- Magma Sim --- #
elif (game_select == 3):
    FPS = 10
    nh = 'Moore'
    delta_x = 0.01
    starting_density = 0.5
    game = MagmaSim(size_x=WIDTH, size_y=HEIGHT, pixels_per_led=pixels_per_led, FPS=FPS, 
                    neighbor_rules=nh, delta_x=delta_x, starting_density=starting_density)
    

# --- Fluidsimtest1 ---
elif (game_select == 5):
    FPS = 60
    game = Fluidsimtest1.FluidSim(size_x=WIDTH, size_y=HEIGHT, pixels_per_led=pixels_per_led, FPS=FPS)
