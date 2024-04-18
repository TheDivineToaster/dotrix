import numpy
from game_of_life_sim import GameOfLife
from multi_state_life_sim import MultiStateLife
from magma_sim import MagmaSim

'''Thoughts here are that this script acts as the pygame interpreter, 
and we have other scripts to control different ways to mess with the image.
like fluid sim or cellular automata'''


# Constants
WIDTH, HEIGHT = 60, 60 # number of "LEDs" on the screen
pixels_per_led = 10
FPS = 60    # base fps value, each game should have their own


# Choose which sim we use
game_select = numpy.random.randint(0,2) # inclusive

# --- Basic Game of Life --- #
if (game_select == 0):
    FPS = 10
    # game rules
    B = [3]
    S = [2, 3]
    nh = 'Moore'
    starting_density = 0.6
    # run game of life
    game = GameOfLife(size_x=WIDTH, size_y=HEIGHT, FPSs=FPS, B=B, S=S, nh=nh,
                      cell_size=pixels_per_led, starting_density=starting_density, run_main=True)

# --- RockPaperScissors/MultiStateLife --- #
elif (game_select == 1):
    FPS = 10
    nh = 'Moore'
    threshold = 3
    rules_select = numpy.random.randint(0,2) # inclusive

    if (rules_select == 0): # 3-state (normal Rock Paper Scissor)
        rules = {1: [2], 2: [0], 3: [1]}
    elif (rules_select ==1): # 4-state (unbalanced)
        rules = {1: [4], 2: [1], 3: [1, 2], 4: [2, 3]}
    else: # (rules_select==2): # 5-state (balanced)
        rules = {1: [4, 5], 2: [1, 5], 3: [1, 2], 4: [2, 3], 5: [3, 4]}
    game = MultiStateLife(size_x=WIDTH, size_y=HEIGHT, pixels_per_led=pixels_per_led, FPS=FPS,
                          neighbor_rules=nh, rules=rules, threshold=threshold)

# --- Magma Sim --- #
elif (game_select == 2):
    FPS = 10
    nh = 'Moore'
    delta_x = 0.01
    starting_density = 0.5
    game = MagmaSim(size_x=WIDTH, size_y=HEIGHT, pixels_per_led=pixels_per_led, FPS=FPS, 
                    neighbor_rules=nh, delta_x=delta_x, starting_density=starting_density)
    
