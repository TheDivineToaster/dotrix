import os
import pygame
import random
import itertools
import numpy as np


class CellularAutomata():

    def __init__(self, rule, save_state_dir=None, *args, **kwargs):

        super().__init__(*args, **kwargs, B=[], S=[])

        self.rule = rule
        self.save_state_dir = save_state_dir
        self.update_rules = self.get_update_dict(rule)

    def generate_neighbor_list(self, nh):

        # possible nbrhoods
        mid = [[0, 0]]
        sides = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        corners = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        lookup_dirs = dict(moore=sides+corners+mid,
                           neumann=sides+mid,
                           neumann_r=corners+mid)
        # gen nbr list
        key = nh.lower()
        dirs = lookup_dirs[key]
        self._generate_neighbor_list(dirs)

    def get_update_dict(self, rule_index):
        n_nbrs = len(self.nbr_list[(0, 0)])

        # hard code bit-string for Neumann (4) or Moore (8)
        if self.neighborhood.lower() == 'neumann':
            self.rule_key = '{:032b}'.format(rule_index)
        elif self.neighborhood.lower() == 'moore':
            self.rule_key = '{:0512b}'.format(rule_index)
        else:
            raise ValueError(self.neighborhood)

        # make rules into dict
        unique_nbrhoods = itertools.product([0, 1], repeat=n_nbrs)
        update_rules = dict()
        for nbrhood, rule in zip(unique_nbrhoods, self.rule_key):
            update_rules[nbrhood] = int(rule)
        return update_rules

    def print_rules(self, full=False):
        print(self.neighborhood, self.rule)

        if full:
            print('State 0: ')
            for nbrhood, rule in self.update_rules.items():
                print(nbrhood, rule)

    def evolve(self, verbose):

        # save state
        if self.save_state_dir is not None:
            fname = os.path.join(self.save_state_dir, 'state-{}.npy'.format(self.step))
            frame = np.zeros((self.size_x, self.size_y), dtype=int)
            for x, v in self.board.items():
                frame[x] = v
            np.save(fname, frame)

        # update
        self.step += 1
        new_board = dict()
        for x in self.board.keys():
            nbrs = self.nbr_list[x]
            nbrhood = tuple(self.board[n] for n in nbrs)
            new_board[x] = self.update_rules[nbrhood]
        self.board = new_board

    def _generate_neighbor_list(self, dirs):
        nbr_list = dict()
        for x in range(self.size_x):
            for y in range(self.size_y):
                nbrs = []
                for n, m in dirs:
                    if self._inside_board(x+n, y+m):
                        nbrs.append((x+n, y+m))

                # for edge cells, append themselves enough times to get correct number of neighbors
                nbrs = nbrs + [(x, y)] * (len(dirs) - len(nbrs))
                assert len(nbrs) == len(dirs)
                nbr_list[(x, y)] = nbrs
        self.nbr_list = nbr_list


if __name__ == '__main__':

    # setup
    pygame.init()
    np.random.seed(42)

    # Constants
    size_x = 1600
    size_y = 800
    FPS = 8

    # setup display
    pygame.init()
    screen = pygame.display.set_mode((size_x, size_y), pygame.SRCALPHA, 32)

    # grid size
    cell_size = 8
    size_xs = size_x / cell_size
    size_ys = size_y / cell_size

    # assert grid perfectly fits into canvas
    assert abs(size_xs - int(size_xs)) < 1e-10
    assert abs(size_ys - int(size_ys)) < 1e-10
    size_xs = int(size_xs)
    size_ys = int(size_ys)

    # rules
    starting_density = 0.5
    nh = 'Neumann'
    if nh == 'Neumann':
        n_max = 2**32
    if nh == 'Moore':
        n_max = 2**512

    # random rule
    rule = random.randint(0, n_max)
    rule = 327623947

    # run game of life
    game = CellularAutomata(size_x=size_xs, size_y=size_ys, nh=nh,
                            rule=rule,
                            cell_size=cell_size, starting_density=starting_density)
    game.print_rules(full=True)
    game.run(screen, FPS=FPS)
    pygame.quit()
