import itertools
import random
import numpy as np

from util import *


class NeutronBoard:
    def __init__(self):
        self._grid = np.array([
            [3, 3, 3, 3, 3],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2]
        ])

    def get_white_soldiers(self):
        return [Vec.from_numpy(elem) for elem in zip(*np.where(self._grid == Soldier.WHITE))]

    def get_black_soldiers(self):
        return [Vec.from_numpy(elem) for elem in zip(*np.where(self._grid == Soldier.BLACK))]

    def get_neutron(self):
        return [Vec.from_numpy(elem) for elem in zip(*np.where(self._grid == Soldier.NEUTRON))][0]

    def furthest_empty_spot(self, pos, dir):
        orig_pos = pos
        while (0 < pos.x < len(self._grid[pos.y]) - 1) \
               and (0 < pos.y < len(self._grid) - 1) \
               and self._grid[tuple(pos + dir)] == Soldier.EMPTY:
            pos += dir
        return pos if pos != orig_pos else None

    def move(self, pos, dir):
        if self._grid[tuple(pos)] == Soldier.EMPTY:
            raise ValueError('nothing to move!')
        furthest = self.furthest_empty_spot(pos, dir)
        if furthest is None:
            raise ValueError('no space to move in the given direction!')
        self._grid[tuple()] = self._grid[tuple(pos)]
        self._grid[tuple(pos)] = 0

    def neighbors(self, x, y):
        neighbors = self._grid[max(0, y-1):min(y+2, len(self._grid)), max(0, x-1):min(x+2, len(self._grid[y]))]
        index_flattened = x + y * neighbors.shape[1]
        return np.delete(neighbors.flatten(), index_flattened)


class Neutron:
    def __init__(self, first_player, second_player):
        self.board = NeutronBoard()
        self.players = itertools.cycle([first_player, second_player])
        self.current_player = next(self.players)
        self.won = False
        self.initial_round = True

    def start(self):
        while not self.won:
            self.play_round()
            self.current_player = next(self.players)

    def play_round(self):
        if not self.initial_round:
            self.current_player.move_neutron(self.board)
        self.current_player.move_soldier(self.board)

        self.won |= all(neighbor != 0 for neighbor in self.board.neighbors(*self.board.get_neutron()))
        self.won |= self.board.get_neutron()[0] in [0, 4]
    