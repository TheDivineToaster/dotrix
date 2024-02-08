import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluid Simulation")

# Initialize grid
grid_size = 50
density = np.zeros((grid_size, grid_size, 3), dtype=np.float32)

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simulate fluid dynamics (simple random movement)
    density += 0.01 * np.random.randn(grid_size, grid_size, 3)

    # Clamp values to [0, 1]
    density = np.clip(density, 0, 1)

    # Map density to color and draw on the screen
    pixels = (density * 255).astype(np.uint8)
    surface = pygame.surfarray.make_surface(pixels)
    screen.blit(pygame.transform.scale(surface, (WIDTH, HEIGHT)), (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()



