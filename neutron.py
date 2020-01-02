import itertools
import textwrap
import numpy as np
from colorama import Fore, Back, Style

from util import *


class Soldier:
    def __init__(self, board, position, color):
        self._board = board
        self.pos = position
        self.color = color

    @property
    def possible_directions(self):
        return [dir for dir in directions if self._board.furthest_empty_spot(self.pos, dir) is not None]

    def move(self, direction):
        if direction not in self.possible_directions:
            raise ValueError('not possible to move in this direction')
        dst = self._board.furthest_empty_spot(self.pos, direction)
        self._board.grid[tuple(dst)] = self.color
        self._board.grid[tuple(self.pos)] = 0
        self.pos = dst


class Neutron(Soldier):
    VALUE = 1

    def __init__(self, board, position):
        super().__init__(board, position, self.VALUE)


class NeutronBoard:
    def __init__(self):
        self.grid = np.array([
            [3, 3, 3, 3, 3],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2]
        ])

        self.white_soldiers = [
            Soldier(self, Vec.fromtuple(idx), Color.WHITE)
            for idx in zip(*np.where(self.grid == Color.WHITE))
        ]

        self.black_soldiers = [
            Soldier(self, Vec.fromtuple(idx), Color.BLACK)
            for idx in zip(*np.where(self.grid == Color.BLACK))
        ]

        self.neutron = Neutron(self, Vec.fromtuple(next(zip(*np.where(self.grid == Neutron.VALUE)))))

    def get_soldiers(self, color):
        if color == Color.WHITE:
            return self.white_soldiers
        elif color == Color.BLACK:
            return self.black_soldiers
        else:
            raise ValueError('invalid soldier color')

    def furthest_empty_spot(self, pos, dir):
        orig_pos = pos
        dir = directions[dir]
        while (0 <= (pos + dir).x < len(self.grid[pos.y])) \
                and (0 <= (pos + dir).y < len(self.grid)) \
                and self.grid[tuple(pos + dir)] == 0:
            pos += dir
        return pos if pos != orig_pos else None

    def neighbors(self, pos):
        neighbors = []
        for y in range(max(0, pos.y - 1), min(pos.y + 2, len(self.grid))):
            for x in range(max(0, pos.x - 1), min(pos.x + 2, len(self.grid[y]))):
                if x != pos.x or y != pos.y:
                    neighbors.append(self.grid[y, x])
        return neighbors

    def __str__(self):
        grid_str = Fore.BLACK + Back.YELLOW + textwrap.dedent("""
                1   2   3   4   5
              +---+---+---+---+---+
            A | {} | {} | {} | {} | {} |
              +---+---+---+---+---+
            B | {} | {} | {} | {} | {} |
              +---+---+---+---+---+
            C | {} | {} | {} | {} | {} |
              +---+---+---+---+---+
            D | {} | {} | {} | {} | {} |
              +---+---+---+---+---+
            E | {} | {} | {} | {} | {} |
              +---+---+---+---+---+""") + Style.RESET_ALL

        color_map = {
            Color.WHITE: Fore.WHITE,
            Color.BLACK: Fore.BLACK,
            Neutron.VALUE: Fore.RED
        }

        formats = []

        for j in range(self.grid.shape[0]):
            for i in range(self.grid.shape[1]):
                if self.grid[j, i]:
                    formats.append(color_map[self.grid[j, i]] + '\u2022' + Fore.BLACK)
                else:
                    formats.append(' ')

        return grid_str.format(*formats)


class NeutronGame:
    def __init__(self, first_player, second_player):
        self.board = NeutronBoard()
        self.players = itertools.cycle([first_player, second_player])
        self.current_player = next(self.players)
        self.winner = None
        self.initial_round = True

    def start(self):
        while not self.winner:
            self.play_round()
            self.current_player = next(self.players)
        print(self.board)
        print(f'{Color.color_names[self.winner]} player won the game!'.capitalize())

    def play_round(self):
        if not self.initial_round:
            self.current_player.move_neutron(self.board)
            if self.check_won():
                return

        self.current_player.move_soldier(self.board)
        if self.check_won():
            return

        self.initial_round = False

    def check_won(self):
        if all(neighbor != 0 for neighbor in self.board.neighbors(self.board.neutron.pos)):
            self.winner = self.current_player.color
        elif self.board.neutron.pos.y == 0:
            self.winner = Color.BLACK
        elif self.board.neutron.pos.y == 4:
            self.winner = Color.WHITE
        return self.winner
