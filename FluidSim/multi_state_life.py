import pygame
import numpy as np
import pandas as pd
from collections import Counter
from game_of_life import GameOfLife


class MultiStateLife(GameOfLife):

    color1 = pygame.Color(228, 26, 28)
    color2 = pygame.Color(51, 160, 44)
    color3 = pygame.Color(31, 120, 180)
    color4 = pygame.Color(231, 41, 138)

    def __init__(self, rules, threshold=3, *args, **kwargs):
        """ Rules should be give as

        rules = {1: [2], 2: [3, 4], ...}
        meaning state 0 gets beaten by state 2,
        state 2 gets beaten by both state 3 and 4

        thershold indicates how many of a state is need in the neighborhood
        to count as beating the cell of interest.
        """

        self.setup_rules(rules)
        self.setup_colors()
        self.threshold = threshold
        self.data_records = []

        super().__init__(B=[], S=[], *args, **kwargs)

    @property
    def available_states(self):
        return sorted(self.rules.keys())

    def setup_rules(self, rules):
        self.n_states = len(rules)
        self.rules = rules
        self.inverted_rules = {s: [] for s in self.rules.keys()}
        for s, states in self.rules.items():
            for si in states:
                self.inverted_rules[si].append(s)

    def setup_colors(self):
        import matplotlib.colors as mcolors
        color_names = ['tab:blue', 'tab:orange', 'tab:red', 'tab:green', 'tab:cyan', 'tab:olive']
        color_list = [mcolors.TABLEAU_COLORS[name] for name in color_names]

        states_list = sorted(self.rules.keys())
        self.color_dict = dict()
        for s, c in zip(states_list, color_list):
            color = pygame.Color(c)
            self.color_dict[s] = color

    def generate_random_board(self, density=None):
        board = dict()
        for i in range(self.size_x):
            for j in range(self.size_y):
                board[(i, j)] = int(np.random.choice(self.available_states, 1))
        self.board = board

    def draw(self, screen, show_step=False):
        screen.fill(self.background_color)
        for x in range(self.size_x):
            for y in range(self.size_y):
                color = self.color_dict[self.board[(x, y)]]
                r = self.rects[(x, y)]
                pygame.draw.rect(screen, color, r, 0)

        self._draw_rules(screen)
        self._draw_density_graph(screen)

    def _draw_density_graph(self, screen):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.backends.backend_agg as agg
        import matplotlib.pyplot as plt

        # draw canvas
        w = 410
        h = 290
        r1 = pygame.rect.Rect(240, 0, w+10, h+10)
        r2 = pygame.rect.Rect(240, 0, w, h)
        pygame.draw.rect(screen, (0, 0, 0), r1, 0)
        pygame.draw.rect(screen, (255, 255, 255), r2, 0)

        # plot params
        lw = 2
        x_max = 100
        ylim = [0, 1]
        yticks = np.arange(-2, 2, 0.2)

        # fig
        fig = plt.figure(figsize=[4.1, 2.9], dpi=100)
        ax = fig.gca()

        # data
        df = pd.DataFrame(self.data_records)
        if len(df) > 0:
            max_step = df.step.max()
            df = df[df.step >= max_step - x_max]
            # plot
            for s in self.available_states:
                name = 'density_{}'.format(s)
                color = self.color_dict[s]
                ax.plot(df.step, df[name], '-', color=(color.r/255, color.g/255, color.b/255), lw=lw)
        else:
            max_step = x_max

        xlim = [max(0, max_step-x_max), max(max_step+1, x_max)]
        ax.set_yticks(yticks)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title('Density', fontsize=20)
        ax.tick_params(labelsize=12)

        # get canvas
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (240, 0))
        plt.close()

    def _draw_rules(self, screen):

        col_white = pygame.Color(255, 255, 255)
        col_black = pygame.Color(0, 0, 0)

        # draw canvas
        w = 240
        h = 160 + self.n_states * 40
        h = 300
        r1 = pygame.rect.Rect(0, 0, w, h)
        r2 = pygame.rect.Rect(0, 0, w-10, h-10)
        pygame.draw.rect(screen, col_black, r1, 0)
        pygame.draw.rect(screen, col_white, r2, 0)

        # draw text
        font = pygame.font.SysFont('Times', 45)
        text = font.render('Rules', 1, col_black)
        screen.blit(text, (45, 5))

        # draw rules
        x = 18
        y = 70
        dx = 40  # spacing between rectangles
        dy = 45
        L = 25
        font = pygame.font.SysFont('Times', 30)
        text = font.render('beats', 1, col_black)
        for i, (s, states) in enumerate(self.inverted_rules.items()):
            rs = pygame.rect.Rect(x, y+i*dy, L, L)
            pygame.draw.rect(screen, self.color_dict[s], rs, 0)
            screen.blit(text, (x+44, y-5 + i*dy))
            for j, si in enumerate(states):
                rsi = pygame.rect.Rect(x+120+j*dx, y+i*dy, L, L)
                pygame.draw.rect(screen, self.color_dict[si], rsi, 0)

        # text with threshold value
        if False:
            font = pygame.font.SysFont('Times', 30)
            text = font.render('threshold={}'.format(self.threshold), 1, col_black)
            screen.blit(text, (x+10, y + (i+1.1)*dy))

    def evolve(self, verbose):
        # record data
        row = dict(step=self.step)
        states = list(self.board.values())
        for s in sorted(self.rules.keys()):
            row['density_{}'.format(s)] = states.count(s) / len(states)
        self.data_records.append(row)

        # update
        self.step += 1
        new_board = dict()
        for x, state in self.board.items():
            nbrs = self.nbr_list[x]
            nbrs_states = [self.board[n] for n in nbrs]

            counts = Counter({b: nbrs_states.count(b) for b in self.rules[state]})
            nbr_state, count = counts.most_common(1)[0]
            if count >= self.threshold:
                new_board[x] = nbr_state
            else:
                new_board[x] = state
        self.board = new_board


if __name__ == '__main__':

    # setup
    seed = 42
    pygame.init()
    np.random.seed(seed)

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
    nh = 'Moore'
    threshold = 3

    # 3-state (normal Rock Paper Scissor)
    rules = {0: [2], 1: [0], 2: [1]}

    # 4-state (unbalanced)
    # rules = {1: [4], 2: [1], 3: [1, 2], 4: [2, 3]}

    # 5-state (balanced)
    # rules = {1: [4, 5], 2: [1, 5], 3: [1, 2], 4: [2, 3], 5: [3, 4]}

    # run game of life
    game = MultiStateLife(size_x=size_xs, size_y=size_ys, nh=nh, rules=rules, threshold=threshold,
                          cell_size=cell_size)

    game.run(screen, FPS=FPS, max_steps=1000)
    pygame.quit()
