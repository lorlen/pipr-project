from abc import ABC, abstractmethod
import random

from util import directions


class Player(ABC):
    @abstractmethod
    def move_soldier(self, board, soldiers):
        pass

    @abstractmethod
    def move_neutron(self, board, neutron):
        pass


class RandomPlayer(Player):
    def move_soldier(self, board, soldiers):
        board.move(random.choice(soldiers), random.choice(directions.values()))

    def move_neutron(self, board, neutron):
        board.move(neutron, random.choice(directions.values()))


class StrategyPlayer(Player):
    pass


class HumanPlayer(Player):
    pass