from abc import ABC, abstractmethod
import random
import re
import numpy as np

from util import Vec, Color


class Player(ABC):
    """
    Abstract base class of all Neutron game players. Defines methods called by
    the game to allow players to make decisions about the next move.

    Args:
        board (neutron.NeutronBoard):
            board of the game played by this player.
        color (int): color of this player's soldiers.
        home_row (int): index of this player's home row on board.
    """
    def __init__(self, board, color, home_row):
        self.board = board
        self.color = color
        self.home_row = home_row

    @abstractmethod
    def move_soldier(self):
        """
        Method called by the game when it's this player's turn to move one of
        their soldiers.
        """
        pass

    @abstractmethod
    def move_neutron(self):
        """
        Method called by the game when it's this player's turn to move the
        neutron.
        """
        pass


class RandomPlayer(Player):
    def move_soldier(self):
        soldier = random.choice([
            soldier
            for soldier in self.board.get_soldiers(self.color)
            if soldier.possible_directions
        ])
        soldier.move(random.choice(tuple(soldier.possible_directions)))

    def move_neutron(self):
        self.board.neutron.move(
            random.choice(tuple(self.board.neutron.possible_directions))
        )


class StrategyPlayer(RandomPlayer):
    """
    A player that tries to apply some simple rules to increase its winning
    chance. If no rule can be applied in the current situation, it falls
    back to random movement.
    """
    def block_enemy_row(self, soldiers, enemy_row):
        """
        Tries to block an empty spot in enemy's home row by putting one of the
        soldiers in there.

        Args:
            soldiers (list): list of this player's soldiers.
            enemy_row (int): index of the enemy player's row.

        Returns:
            bool: ``True`` if the move was successful, ``False`` otherwise
        """
        empty_enemy_pos = [
            Vec(x, enemy_row)
            for x in range(len(self.board.grid[enemy_row]))
            if self.board.grid[enemy_row, x] == 0
        ]

        losing_positions = [
            pos
            for pos in self.board.neutron.possible_moves
            if pos in empty_enemy_pos
        ]

        eligible_soldiers = []

        for soldier in soldiers:
            moves = [
                pos
                for pos in soldier.possible_moves
                if pos in losing_positions
            ]
            if moves:
                eligible_soldiers.append((soldier, moves))

        if eligible_soldiers:
            soldier, moves = random.choice(eligible_soldiers)
            soldier.move_to_pos(random.choice(moves))
            return True

        return False

    def move_into_home(self):
        """
        Tries to move the neutron into the home row

        Returns:
            bool: ``True`` if the move was successful, ``False`` otherwise
        """
        try:
            self.board.neutron.move_to_pos(next(
                pos
                for pos in self.board.neutron.possible_moves
                if pos.y == self.home_row
            ))
            return True
        except StopIteration:
            return False

    def block_neutron(self, soldiers):
        """
        Tries to completely block neutron from moving, if there's only one
        direction the neutron can move.

        Returns:
            bool: ``True`` if the move was successful, ``False`` otherwise
        """
        y, x = self.board.neutron.pos
        maxy, maxx = self.board.grid.shape

        empty_neighbors = set(zip(*np.where(
            self.board.grid[
                max(0, y-1):min(maxy, y+2),
                max(0, x-1):min(maxx, x+2)
            ] == 0
        )))

        eligible_soldiers = [
            (soldier, soldier.possible_moves & empty_neighbors)
            for soldier in soldiers
            if soldier.possible_moves & empty_neighbors
        ]

        if eligible_soldiers:
            soldier, moves = random.choice(eligible_soldiers)
            soldier.move_to_pos(random.choice(tuple(moves)))
            return True

        return False

    def move_soldier(self):
        soldiers = self.board.get_soldiers(self.color)
        enemy_row = len(self.board.grid) - 1 - self.home_row

        if self.block_neutron(soldiers):
            pass
        elif self.block_enemy_row(soldiers, enemy_row):
            pass
        else:
            super().move_soldier()

    def move_neutron(self):
        if self.move_into_home():
            pass
        else:
            super().move_neutron()


class HumanPlayer(Player):
    _pattern = re.compile(r'([ABCDE])([12345])')

    def __init__(self, board, color, home_row):
        super().__init__(board, color, home_row)
        print(f'You control {Color.color_names[color]} soldiers')

    def move_soldier(self):
        print(f"You're moving a {Color.color_names[self.color]} soldier.")
        while True:
            pos_str = input('Enter coordinates of soldier you want to move: ')
            match = self._pattern.fullmatch(pos_str.strip().upper())
            if not match:
                print(
                    f'The string {pos_str} cannot be interpreted as position.'
                )
                continue
            pos = Vec(int(match.group(2)) - 1, ord(match.group(1)) - ord('A'))
            soldier = [
                soldier
                for soldier in self.board.get_soldiers(self.color)
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

    def move_neutron(self):
        print(f"You're moving the neutron")
        while True:
            dir = input('Enter direction you want to move: ')
            if dir in self.board.neutron.possible_directions:
                self.board.neutron.move(dir)
                break
            else:
                print(f"You can't move in this direction")
