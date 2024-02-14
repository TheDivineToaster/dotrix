import pygame
import random
import numpy
from collections import Counter

class RockPaperScissors():
    # set team colors
    color1 = (228, 26, 28)
    color2 = (51, 160, 44)
    color3 = (31, 120, 180)
    color4 = (231, 41, 138)
    colors = [color1, color2, color3, color4]


    def __init__(self, size_x, size_y, num_colors):
        self.width = size_x
        self.height = size_y
        self.num_colors = num_colors
        self.neighbor_list = None
        self.board = self.board_init()
        self.screen = numpy.zeros((self.width, self.height, 3)) # needs to be able to be pygame.surfarray.make_surface'd

    def board_init(self):
        mid = [[0, 0]]
        sides = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        corners = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        possible_neighbors = mid + sides  # modify here if you want corners or different neighbors

        # board is a 2D list where each element is a (integer, array)
        # the integer represents its color, the array holds all its valid neighbors
        board = [[None] * self.height] * self.width
        for x in range(self.width):
            for y in range(self.height):
                xy_color = self.colors[random.randint(0, self.num_colors - 1)]
                print(xy_color)

                # find possible neighbors
                neighbors = []
                for possible_neighbor in possible_neighbors:
                    if x + possible_neighbor[0] > 0 and x + possible_neighbor[0] < self.width and y + possible_neighbor[1] > 0 and y + possible_neighbor[1] < self.height:
                        neighbors.append(possible_neighbor)
                board[x][y] = {'color': xy_color, 'neighbors': neighbors}
        return board



    def evolve(self):
        new_board = self.board.copy() # save board
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                # here's the fucky bits
                board_piece = self.board[x][y]
                curr_state = board_piece['color']
                neighbors = board_piece['neighbors']
                neighboring_colors = []
                for neighbor in neighbors:
                    neighboring_colors.append(self.board[x + neighbor[0]][y + neighbor[1]]['color']) # should grab the color from the neighboring cell

                # the following two lines found online at https://stackoverflow.com/questions/1518522/find-the-most-common-element-in-a-list
                curr_state = Counter(neighboring_colors).most_common(1)[0][0]

                # set new board
                new_board[x][y]['color'] = curr_state

                # set screen
                self.screen[x][y] = self.get_color(curr_state)
        self.board = new_board
        return pygame.surfarray.make_surface(self.screen)

    def get_color(self, curr_state):
        match (curr_state):
            case 1:
                return self.color1
            case 2:
                return self.color2
            case 3:
                return self.color3
            case 4:
                return self.color4
            case _:
                return self.color1  # change this default value later?
