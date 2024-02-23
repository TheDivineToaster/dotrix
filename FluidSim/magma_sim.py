import math
import pygame
import numpy as np
import matplotlib.pyplot as pyplot
from game_of_life import GameOfLife


class MagmaSim(GameOfLife):

    def __init__(self, size_x, size_y, pixels_per_led, FPS, 
                 neighbor_rules, starting_density, delta_x = 0.25, cmap='magma', wrap_color=True):
        self.width = size_x * pixels_per_led
        self.height = size_y * pixels_per_led

        
        super().__init__(size_x=size_x, size_y=size_y, B=[], S=[], 
                         nh=neighbor_rules, cell_size=pixels_per_led, starting_density=starting_density)
        self.pixels_per_led = pixels_per_led
        self.FPS = FPS
        self.delta_x = delta_x
        self.wrap_color = wrap_color
        self.cmap = pyplot.get_cmap(cmap)

        self.main()

    def get_new_state(self, state, nbr_sum, n_nbrs):
        """ update rule for a given cell """
        x = (state + nbr_sum) / (n_nbrs+1)
        new_state = math.modf(x + self.delta_x)[0]
        new_state = max(min(new_state, 1), 0)
        # print(state, nbr_sum, x, new_state)
        return new_state

    def evolve(self, verbose):

        # update
        self.step += 1
        new_board = dict()
        for x in self.board.keys():
            nbrs = self.nbr_list[x]
            nbr_sum = np.sum([self.board[n] for n in nbrs])

            state = self.board[x]
            new_val = self.get_new_state(state, nbr_sum, len(nbrs))
            new_board[x] = new_val
        self.board = new_board

        # output
        if verbose:
            density = sum(self.board.values()) / (self.size_x * self.size_y)
            print(f'Step {self.step:6d},   density {100 * density:9.5f} %')

    def generate_random_board(self, density=0.5):
        board = np.random.choice([0, 1], (self.size_x, self.size_y), p=[1-density, density])
        board = board * np.random.random((self.size_x, self.size_y))
        board_dict = dict()
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                board_dict[(i, j)] = board[i, j]
        self.board = board_dict

    def draw(self, screen, show_step=False):

        screen.fill(self.background_color)
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.wrap_color:
                    # wrapped cmap, meaning e.g. 0.2 == 0.8
                    s = self.board[(x, y)]
                    c_val = 2 * s if s <= 0.5 else 2 - 2 * s
                else:
                    # normal cmap
                    c_val = self.board[(x, y)]

                # get color
                c = self.cmap(c_val)
                color = pygame.Color(int(255 * c[0]), int(255 * c[1]), int(255 * c[2]))

                # draw
                r = self.rects[(x, y)]
                pygame.draw.rect(screen, color, r, 0)

    def main(self):
        # Initialize Pygame
        pygame.init()
        np.random.seed(400)

        # Create Pygame window
        screen = pygame.display.set_mode((self.width, self.height), pygame.SRCALPHA, 32)
        pygame.display.set_caption("Magma Fluid Sim")

        # ---- Main loop ----
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.run(screen, FPS=self.FPS)

            # Cap the frame rate
            clock.tick(self.FPS)
            print(clock.get_fps())

        # Quit Pygame
        pygame.quit()


