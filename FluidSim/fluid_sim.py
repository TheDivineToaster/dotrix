import numpy as np

class FluidSim():
    def __init__(self, size_x, size_y):
        self.width = size_x
        self.height = size_y
        self.grid = np.zeros((self.width, self.height, 3), dtype=np.float32)

    def iterate(self, grid):

        # Simulate fluid dynamics (simple random movement)
        self.grid += 0.01 * np.random.randn(self.width, self.height, 3)

        # Clamp values to [0, 1]
        density = np.clip(density, 0, 1)

        # Map density to color and draw on the screen
        pixels = (density * 255).astype(np.uint8)