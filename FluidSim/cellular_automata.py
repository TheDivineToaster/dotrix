import pygame
import random
import numpy

class RockPaperScissors():

    color1 = pygame.Color(228, 26, 28)
    color2 = pygame.Color(51, 160, 44)
    color3 = pygame.Color(31, 120, 180)
    color4 = pygame.Color(231, 41, 138)
    colors = [color1, color2, color3, color4]


    def __init__(self, size_x, size_y, num_colors, starting_density):
        self.width = size_x
        self.height = size_y
        self.num_colors = num_colors
        self.density = starting_density # currently unused
        self.step_count = 0
        self.neighbor_list = None
        self.board = self.board_init()
        self.screen = numpy.zeros((self.width, self.height))

    def board_init(self):
        mid = [[0, 0]]
        sides = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        corners = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        possible_neighbors = mid + sides  # modify here if you want corners or different neighbors

        board = list()
        for x in range(self.width):
            column = [None] * self.height
            for y in range(self.height):
                xy_color = self.colors[random.randint(1, self.num_colors)]
                neighbors = []
                for n, m in possible_neighbors:
                    if ((x+n) > 0 and (x+n) < self.width and (y+m) > 0 and (y+m) < self.height):
                        neighbors.append((x+n, y+m))

                # for edge cells, append themselves enough times to get correct number of neighbors
                neighbors = neighbors + [(x, y)] * (len(possible_neighbors) - len(neighbors))
                assert len(neighbors) == len(possible_neighbors)
                column[y] = (xy_color, neighbors)
            board.append(column)
    

    def evolve(self):
        self.step_count += 1
        new_board = self.board.copy()
        for x in range(self.board):
            for y in range(self.board[x]):
                curr_state = self.board[x][y][0]
                neighbors = self.board[x][y][1]
                states = []
                for elem in neighbors:
                    states.append(self.board[x + elem[0]][y + elem[1]])
                curr_state = max(set(states), key=states.count)
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
                return self.color1  # change this later?
'''  
    def draw(self, screen, show_step=False):
        screen.fill(self.background_color)
        for x in range(self.size_x):
            for y in range(self.size_y):
                color = self.color_dict[self.board[(x, y)]]
                r = self.rects[(x, y)]
                pygame.draw.rect(screen, color, r, 0)

'''