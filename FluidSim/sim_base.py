import pygame
import numpy as np
from rock_paper_scissors import RockPaperScissors
from fluid_sim import FluidSim

'''Thoughts here are that this script acts as the pygame interpreter, 
and we have other scripts to control different ways to mess with the image.
like fluid sim or cellular automata'''

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 123, 48 # number of "LEDs" on the screen
pixels_per_led = 10
FPS = 60    # base fps value, each game should have their own

# Colors _currently unused_
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create Pygame window
display = pygame.display.set_mode((WIDTH * pixels_per_led, HEIGHT * pixels_per_led))
pygame.display.set_caption("Fluid Simulation")

# Initialize grid
grid = np.zeros((WIDTH, HEIGHT, 3))
screen = pygame.surfarray.make_surface(grid) # default screen

# Choose which sim we use
game_select = np.random.randint(0,1) # inclusive
game_select = 1 # hard set to test rock_paper_scissors
if (game_select == 0):
    game = RockPaperScissors(WIDTH, HEIGHT, 3) # grid size and number of colors
    FPS = 10
elif (game_select == 1):
    game = FluidSim(WIDTH, HEIGHT)
    FPS = 60

# ---- Main loop ----
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen = game.evolve() # all sims should use a common function if we want to go with this being the base runner
    display.blit(pygame.transform.scale(screen, (WIDTH * pixels_per_led, HEIGHT * pixels_per_led)), (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
    print(clock.get_fps())

# Quit Pygame
pygame.quit()



