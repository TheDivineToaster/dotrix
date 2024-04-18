import numpy
from cv_processor import cv_processor
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

computer_vision = cv_processor(r"Visuals\weights\best.pt")
computer_vision.start_cam(0)

def get_hand_input(self, radius=1):
    radius /= 2
    computer_vision.capture()

    hand_list = computer_vision.get_xy_list()
    scaled_hand_list = []
    for hand in hand_list:
        hand[0] /= 10
        hand[1] /= 10
        scaled_hand_list.append((int(WIDTH - hand[0]),int(hand[1])))
    hand_list = []
    
    for hand in scaled_hand_list:
        xmin = max(0, (int)(hand[0] - radius)) 
        xmax = min(WIDTH - 1, (int)(hand[0] + radius))
        ymin = max(0, (int)(hand[1] - radius))
        ymax = min(HEIGHT - 1, (int)(hand[1] + radius))
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                hand_list.append((x, y))
    return hand_list


# Choose which sim we use
game_select = numpy.random.randint(0,2) # inclusive
game_select = 2

# --- Basic Game of Life --- #
if (game_select == 0):
    FPS = 10
    # game rules
    B = [3]
    S = [2, 3]
    nh = 'Moore'
    starting_density = 0.6
    radius = 3
    # run game of life
    game = GameOfLife(size_x=WIDTH, size_y=HEIGHT, FPSs=FPS, B=B, S=S, nh=nh,
                      cell_size=pixels_per_led, starting_density=starting_density, run_main=True, rad=radius)

# --- RockPaperScissors/MultiStateLife --- #
elif (game_select == 1):
    FPS = 10
    nh = 'Moore'
    threshold = 3
    radius = 7
    rules_select = numpy.random.randint(0,2) # inclusive

    if (rules_select == 0): # 3-state (normal Rock Paper Scissor)
        rules = {1: [2], 2: [0], 3: [1]}
    elif (rules_select ==1): # 4-state (unbalanced)
        rules = {1: [4], 2: [1], 3: [1, 2], 4: [2, 3]}
    else: # (rules_select==2): # 5-state (balanced)
        rules = {1: [4, 5], 2: [1, 5], 3: [1, 2], 4: [2, 3], 5: [3, 4]}
    game = MultiStateLife(size_x=WIDTH, size_y=HEIGHT, pixels_per_led=pixels_per_led, FPS=FPS,
                          neighbor_rules=nh, rules=rules, threshold=threshold, rad=radius)

# --- Magma Sim --- #
elif (game_select == 2):
    FPS = 10
    nh = 'Moore'
    delta_x = 0.01
    starting_density = 0.5
    radius = 7
    cmap_options = ['viridis', 'magma', 'ocean', 'Paired', 'twilight', 'hsv']
    colormap = cmap_options[numpy.random.randint(0, len(cmap_options) - 1)]
    game = MagmaSim(size_x=WIDTH, size_y=HEIGHT, pixels_per_led=pixels_per_led, FPS=FPS, 
                    neighbor_rules=nh, delta_x=delta_x, starting_density=starting_density, cmap=colormap, rad=radius)
    
