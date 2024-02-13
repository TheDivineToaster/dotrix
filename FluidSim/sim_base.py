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
FPS = 60    # move to outside constants, as fps is more of a step function, which will be dependent on what's running

# Colors
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
game_select = 0 # hard set to test rock_paper_scissors
if (game_select == 0):
    game = RockPaperScissors(WIDTH, HEIGHT, 3) # grid size and number of colors

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen = game.evolve()
    display.blit(pygame.transform.scale(screen, (WIDTH * pixels_per_led, HEIGHT * pixels_per_led)), (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
    #print(clock.get_fps())

# Quit Pygame
pygame.quit()



