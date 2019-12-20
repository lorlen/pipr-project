import itertools
import random
import numpy as np

# class InvalidStateError(Exception):
#     pass

class Soldier:
    EMPTY = 0
    NEUTRON = 1
    WHITE = 2
    BLACK = 3

# class NeutronState:
#     MoveNeutronWhite = 0
#     MoveNeutronBlack = 1
#     MoveWhite = 2
#     MoveBlack = 3
#     GameWon = 4

class NeutronBoard:
    def __init__(self):
        self.grid = np.array([
            [3, 3, 3, 3, 3],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2]
        ])

    def get_white_soldiers(self):
        return list(zip(*np.where(self.grid == Soldier.WHITE)))

    def get_black_soldiers(self):
        return list(zip(*np.where(self.grid == Soldier.BLACK)))

    def get_neutron(self):
        return next(zip(*np.where(self.grid == Soldier.NEUTRON)))

    def move(self, src, dst):
        if self.grid[src[1], src[0]] == Soldier.EMPTY:
            raise ValueError('nothing to move!')
        self.grid[dst[1], dst[0]] = self.grid[src[1], src[0]]
        self.grid[src[1], src[0]] = 0

    def neighbors(self, x, y):
        neighbors = self.grid[max(0, y-1):min(y+2, len(self.grid)), max(0, x-1):min(x+2, len(self.grid[y]))]
        index_flattened = x + y * neighbors.shape[1]
        return np.delete(neighbors.flatten(), index_flattened)

class Neutron:
    def __init__(self, first_player, second_player):
        self.board = NeutronBoard()
        self.players = itertools.cycle([first_player, second_player])
        self.current_player = next(self.players)
        self.won = False

    def start(self):
        while not self.won:
            self.play_round()
            self.current_player = next(self.players)

    def play_round(self):
        
    