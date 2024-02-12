import pygame
import numpy as np

'''Thoughts here are that this script acts as the pygame interpreter, 
and we have other scripts to control different ways to mess with the image.
like fluid sim or cellular automata'''

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 123, 48 # number of "LEDs" on the screen
pixels_per_led = 10
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create Pygame window
screen = pygame.display.set_mode((WIDTH * pixels_per_led, HEIGHT * pixels_per_led))
pygame.display.set_caption("Fluid Simulation")

# Initialize grid
density = np.zeros((WIDTH, HEIGHT, 3), dtype=np.float32)

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simulate fluid dynamics (simple random movement)
    density += 0.01 * np.random.randn(WIDTH, HEIGHT, 3)

    # Clamp values to [0, 1]
    density = np.clip(density, 0, 1)

    # Map density to color and draw on the screen
    pixels = (density * 255).astype(np.uint8)
    surface = pygame.surfarray.make_surface(pixels)
    screen.blit(pygame.transform.scale(surface, (WIDTH * pixels_per_led, HEIGHT * pixels_per_led)), (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()



