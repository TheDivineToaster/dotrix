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
        self.step_count = 0
        self.neighbor_list = None
        self.board = self.board_init()
        print(self.board) # testing
        self.screen = numpy.zeros((self.width, self.height, 3)) # needs to be able to be pygame.surfarray.make_surface'd

    def board_init(self):
        mid = [[0, 0]]
        sides = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        corners = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        possible_neighbors = mid + sides  # modify here if you want corners or different neighbors

        # board is a 2D list where each element is a (integer, array)
        # the integer represents its color, the array holds all its valid neighbors
        board = list()
        for x in range(self.width):
            column = [None] * self.height
            for y in range(self.height):
                # set color
                xy_color = self.colors[random.randint(1, self.num_colors)]

                # find possible neighbors
                neighbors = []
                for elem in possible_neighbors:
                    if x + elem[0] > 0 and x + elem[0] < self.width and y + elem[1] > 0 and y + elem[1] < self.height:
                        neighbors.append(elem)

                # set item
                column[y] = [xy_color, neighbors]

                # for edge cells, append themselves enough times to get correct number of neighbors
                # taken from online, don't understand and don't think we need if we do most common
                '''neighbors = neighbors + [(x, y)] * (len(possible_neighbors) - len(neighbors))
                assert len(neighbors) == len(possible_neighbors)
                column[y] = (xy_color, neighbors)'''
            # append column to row
            board.append(column)
        return board

    def evolve(self):
        self.step_count += 1 # currently unused
        new_board = self.board.copy() # save board
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                # here's the fucky bits
                curr_state = self.board[x][y][0] # mirrors xy_color from board_init
                neighbors = self.board[x][y][1] # mirrors neighbors
                states = []
                for elem in neighbors:
                    states.append(self.board[x + elem[0]][y + elem[1]][0]) # should grab the color from the neighboring cell

                # the following two lines found online at https://stackoverflow.com/questions/1518522/find-the-most-common-element-in-a-list
                counter = Counter(states)
                curr_state = counter.most_common(1)[0][0]

                # set new board
                new_board[x][y][0] = curr_state

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
