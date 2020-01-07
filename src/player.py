from abc import ABC, abstractmethod
import random
import re

from util import Vec, Color


class Player(ABC):
    """
    Abstract base class of all Neutron game players. Defines methods called by
    the game to allow players to make decisions about the next move.

    Args:
        color (int): color of this player's soldiers.
    """
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def move_soldier(self, board):
        """
        Method called by the game when it's this player's turn to move one of
        their soldiers.

        Args:
            board (neutron.NeutronBoard): board of the game played by this
            player.
        """
        pass

    @abstractmethod
    def move_neutron(self, board):
        """
        Method called by the game when it's this player's turn to move the
        neutron.

        Args:
            board (neutron.NeutronBoard): board of the game played by this
            player.
        """
        pass


class RandomPlayer(Player):
    def move_soldier(self, board):
        soldier = random.choice([
            soldier
            for soldier in board.get_soldiers(self.color)
            if soldier.possible_directions
        ])
        soldier.move(random.choice(soldier.possible_directions))

    def move_neutron(self, board):
        board.neutron.move(random.choice(board.neutron.possible_directions))


class StrategyPlayer(Player):
    pass


class HumanPlayer(Player):
    _pattern = re.compile(r'([ABCDE])([12345])')

    def __init__(self, color):
        super().__init__(color)
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
            soldier = [
                soldier
                for soldier in board.get_soldiers(self.color)
                if soldier.pos == pos
            ]
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
