from abc import ABC, abstractmethod
import random
import re

from util import *


class Player(ABC):
    @abstractmethod
    def move_soldier(self, board):
        pass

    @abstractmethod
    def move_neutron(self, board):
        pass


class RandomPlayer(Player):
    def __init__(self, color):
        self.color = color

    def move_soldier(self, board):
        soldier = random.choice([soldier for soldier in board.get_soldiers(self.color) if soldier.possible_directions])
        soldier.move(random.choice(soldier.possible_directions))

    def move_neutron(self, board):
        board.neutron.move(random.choice(board.neutron.possible_directions))


class StrategyPlayer(Player):
    pass


class HumanPlayer(Player):
    _pattern = re.compile(r'([ABCDE])([12345])')

    def __init__(self, color):
        self.color = color
        print(f'You control {Color.color_names[color]} soldiers')

    def move_soldier(self, board):
        print(board)
        print(f"You're moving a {Color.color_names[self.color]} soldier.")
        while True:
            pos_str = input('Enter coordinates of soldier you want to move: ')
            match = self._pattern.fullmatch(pos_str.strip().upper())
            if not match:
                print(f'The string {pos_str} cannot be interpreted as position.')
                continue
            pos = Vec(ord(match.group(1)) - ord('A'), int(match.group(2)) - 1)
            soldier = [soldier for soldier in board.get_soldiers(self.color) if soldier.pos == pos]
            if not soldier:
                print('This is not a position of your soldier.')
                continue
            dir = input('Enter direction you want to move: ')
            if dir in soldier[0].possible_directions:
                soldier[0].move(dir)
                break
            else:
                print("You can't move in this direction.")

    def move_neutron(self, board):
        print(board)
        print(f"You're moving the neutron")
        while True:
            dir = input('Enter direction you want to move: ')
            if dir in board.neutron.possible_directions:
                board.neutron.move(dir)
                break
            else:
                print(f"You can't move in this direction")
