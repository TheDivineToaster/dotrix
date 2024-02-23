import numpy as np
import pygame

class FluidSim():
    def __init__(self, size_x, size_y, pixels_per_led, FPS):
        self.width = size_x
        self.height = size_y
        self.pixels_per_led = pixels_per_led
        self.FPS = FPS
        self.grid = np.zeros((self.width, self.height, 3), dtype=np.float32)
        self.screen = (self.grid * 255).astype(np.uint8)

        self.main()

    def evolve(self):

        # Simulate fluid dynamics (simple random movement)
        self.grid += 0.01 * np.random.randn(self.width, self.height, 3)

        # Clamp values to [0, 1]
        density = np.clip(self.grid, 0, 1)

        # Map density to color and draw on the screen
        self.screen = (density * 255).astype(np.uint8)
        return pygame.surfarray.make_surface(self.screen)
    
    def main(self):
        # Initialize Pygame
        pygame.init()

        # Create Pygame window
        display = pygame.display.set_mode((self.width * self.pixels_per_led, self.height * self.pixels_per_led))
        pygame.display.set_caption("Fluid Sim")

        # Initialize default screen
        screen = pygame.surfarray.make_surface(np.zeros((self.width, self.height, 3)))

        # ---- Main loop ----
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen = self.evolve() # all sims should use a common function if we want to go with this being the base runner
            display.blit(pygame.transform.scale(screen, (self.width * self.pixels_per_led, self.height * self.pixels_per_led)), (0, 0))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(self.FPS)
            print(clock.get_fps())

        # Quit Pygame
        pygame.quit()

