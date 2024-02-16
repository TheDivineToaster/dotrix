import os
import sys
import pygame
import numpy as np


class GameOfLife:

    # drawing parameters
    # alive_color = pygame.Color(255, 255, 255)
    alive_color = pygame.Color(59, 125, 216)
    dead_color = pygame.Color(0, 0, 0)
    background_color = pygame.Color(0, 0, 0)

    def __init__(self, size_x, size_y, B, S, nh='Moore',
                 cell_size=1, starting_density=0.5):

        self.neighborhood = nh
        self.step = 0
        self.size_x = size_x
        self.size_y = size_y
        self.cell_size = cell_size

        self.B = B
        self.S = S

        self.generate_random_board(density=starting_density)
        self.generate_neighbor_list(nh)
        self.setup_grid()

    def _handle_events(self):
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
        return True

    def setup_grid(self, margin=0.1):
        """ Grid positions used for drawing """
        self.rects = dict()
        for x in range(self.size_x):
            for y in range(self.size_y):

                side = self.cell_size
                x_pos = int((x+margin/2) * side)
                y_pos = int((y+margin/2) * side)
                width = (1 - margin) * side
                r = pygame.rect.Rect(x_pos, y_pos, width, width)
                self.rects[(x, y)] = r

    def run(self, screen, FPS=20, max_steps=np.inf, savedir=None,
            show_step=False, draw=True, verbose=False):

        # setup
        clock = pygame.time.Clock()
        if savedir is not None:
            os.makedirs(savedir, exist_ok=True)

        # main loop
        running = True
        while running:

            if not self._handle_events():
                break

            # update game
            if draw:
                self.draw(screen, show_step=show_step)
                pygame.display.flip()
                clock.tick(FPS)
            self.evolve(verbose)

            # save snapshot
            if savedir is not None:
                fname = os.path.join(savedir, 'state-{}.png'.format(self.step))
                pygame.image.save(screen, fname)

            # check for stopping
            if self.step > max_steps:
                running = False

    def draw(self, screen, show_step=False):

        screen.fill(self.background_color)

        for x in range(self.size_x):
            for y in range(self.size_y):
                color = self.alive_color if self.board[(x, y)] == 1 else self.dead_color
                r = self.rects[(x, y)]
                pygame.draw.rect(screen, color, r, 0)

        # draw text
        if show_step:
            text_str = 'step {}'.format(self.step)
            font = pygame.font.SysFont('Times', 80)
            self.text = font.render(text_str, 1, (255, 255, 255))
            screen.blit(self.text, (50, 30))

    def evolve(self, verbose):
        # update
        self.step += 1
        to_birth = []
        to_death = []
        for x in self.board.keys():
            nbrs = self.nbr_list[x]
            nbrs_alive = sum(self.board[n] for n in nbrs)
            if self.board[x] == 0:
                if nbrs_alive in self.B:
                    to_birth.append(x)
            else:
                if nbrs_alive not in self.S:
                    to_death.append(x)

        for x in to_death:
            self.board[x] = 0
        for x in to_birth:
            self.board[x] = 1

        # output
        if verbose:
            density = sum(self.board.values()) / (self.size_x * self.size_y)
            print(f'Step {self.step:6d},   density {100 * density:9.5f} %')

    def generate_random_board(self, density=0.5):
        board = np.random.choice([0, 1], (self.size_x, self.size_y), p=[1-density, density])

        board_dict = dict()
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                board_dict[(i, j)] = board[i, j]

        self.board = board_dict

    def generate_neighbor_list(self, nh):

        # possible nbrhoods
        sides = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        corners = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        lookup_dirs = dict(moore=sides+corners,
                           neumann=sides,
                           neumann_r=corners)
        # gen nbr list
        key = nh.lower()
        dirs = lookup_dirs[key]
        self._generate_neighbor_list(dirs)

    def _generate_neighbor_list(self, dirs):

        nbr_list = dict()
        for x in range(self.size_x):
            for y in range(self.size_y):
                nbrs = []
                for n, m in dirs:
                    if self._inside_board(x+n, y+m):
                        nbrs.append((x+n, y+m))
                nbr_list[(x, y)] = nbrs
        self.nbr_list = nbr_list

    def _inside_board(self, x, y):
        if (0 <= x < self.size_x) and (0 <= y < self.size_y):
            return True
        return False


if __name__ == '__main__':

    # setup
    pygame.init()
    np.random.seed(400)

    # Constants
    size_x = 1600
    size_y = 900
    FPS = 10

    # setup display
    pygame.init()
    screen = pygame.display.set_mode((size_x, size_y), pygame.SRCALPHA, 32)

    # grid size
    cell_size = 20
    size_xs = size_x / cell_size
    size_ys = size_y / cell_size

    # assert grid perfectly fits into canvas
    assert abs(size_xs - int(size_xs)) < 1e-10
    assert abs(size_ys - int(size_ys)) < 1e-10
    size_xs = int(size_xs)
    size_ys = int(size_ys)

    # game rules
    B = [3]
    S = [2, 3]
    nh = 'Moore'
    starting_density = 0.6

    # run game of life
    game = GameOfLife(size_xs, size_ys, B=B, S=S, nh=nh,
                      cell_size=cell_size, starting_density=starting_density)
    game.run(screen, FPS=FPS)
    pygame.quit()
