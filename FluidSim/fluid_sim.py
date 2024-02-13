import numpy as np
import pygame

class FluidSim():
    def __init__(self, size_x, size_y):
        self.width = size_x
        self.height = size_y
        self.grid = np.zeros((self.width, self.height, 3), dtype=np.float32)
        self.screen = (self.grid * 255).astype(np.uint8)

    def evolve(self):

        # Simulate fluid dynamics (simple random movement)
        self.grid += 0.01 * np.random.randn(self.width, self.height, 3)

        # Clamp values to [0, 1]
        density = np.clip(self.grid, 0, 1)

        # Map density to color and draw on the screen
        self.screen = (density * 255).astype(np.uint8)
        return pygame.surfarray.make_surface(self.screen)