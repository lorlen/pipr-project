from abc import ABC, abstractmethod
import random
import re
import numpy as np

from util import Vec, Color, directions_abbrev


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
        self.enemy_row = len(self.board.grid) - 1 - self.home_row

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
    """
    A player that plays the game by randomly moving his soldiers around the
    board. The randomness has one exception: the player won't move the neutron
    into the enemy row, unless forced to.
    """
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
    def block_enemy_row(self, soldiers):
        """
        Tries to block an empty spot in enemy's home row by putting one of the
        soldiers in there.

        Args:
            soldiers (list): list of this player's soldiers.
            enemy_row (int): index of the enemy player's row.

        Returns:
            bool: ``True`` if the move was successful, ``False`` otherwise
        """
        empty_enemy_pos = {
            Vec(x, self.enemy_row)
            for x in range(len(self.board.grid[self.enemy_row]))
            if self.board.grid[self.enemy_row, x] == 0
        }

        losing_positions = self.board.neutron.possible_moves & empty_enemy_pos

        eligible_soldiers = [
            (soldier, soldier.possible_moves & losing_positions)
            for soldier in soldiers
            if soldier.possible_moves & losing_positions
        ]

        # if there is no empty place the neutron can move immediately to,
        # still try to block some empty enemy row spot.
        if not eligible_soldiers:
            eligible_soldiers = [
                (soldier, soldier.possible_moves & empty_enemy_pos)
                for soldier in soldiers
                if soldier.possible_moves & empty_enemy_pos
            ]

        if eligible_soldiers:
            soldier, moves = random.choice(eligible_soldiers)
            soldier.move_to_pos(random.choice(tuple(moves)))
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

        # as we find coordinates of empty neighbors in an subarray, we need to
        # map those coordinates back to global ones.
        def mapper(t):
            return Vec.fromtuple(t) + Vec(x - 1, y - 1)

        empty_neighbors = set(map(mapper, zip(*np.where(
            self.board.grid[
                max(0, y-1):min(maxy, y+2),
                max(0, x-1):min(maxx, x+2)
            ] == 0
        ))))

        if len(empty_neighbors) != 1:
            return False

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

    def avoid_enemy_row(self):
        not_enemy_row = [
            pos
            for pos in self.board.neutron.possible_moves
            if pos.y != self.enemy_row
        ]

        if not_enemy_row:
            self.board.neutron.move_to_pos(random.choice(not_enemy_row))
            return True

        return False

    def move_soldier(self):
        soldiers = self.board.get_soldiers(self.color)

        if self.block_neutron(soldiers):
            return
        if self.block_enemy_row(soldiers):
            return
        super().move_soldier()

    def move_neutron(self):
        if self.move_into_home():
            return
        if self.avoid_enemy_row():
            return
        super().move_neutron()


class HumanPlayer(Player):
    _pattern = re.compile(r'([ABCDE])([12345])')

    def __init__(self, board, color, home_row):
        super().__init__(board, color, home_row)
        print(f'You control {Color.color_names[color]} soldiers')

    @staticmethod
    def _input_or_exit(prompt):
        input_str = input(prompt)
        if input_str.strip().lower() == 'exit':
            exit()
        else:
            return input_str

    def move_soldier(self):
        print(f"You're moving a {Color.color_names[self.color]} soldier.")
        while True:
            pos_str = self._input_or_exit(
                'Enter coordinates of soldier you want to move: '
            )
            match = self._pattern.fullmatch(pos_str.strip().upper())
            if not match:
                print(self.board)
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
                print(self.board)
                print('This is not a position of your soldier.')
                continue
            dir = self._input_or_exit('Enter direction you want to move: ')
            if dir in soldier[0].possible_directions:
                soldier[0].move(dir)
                break
            elif dir in directions_abbrev.keys():
                soldier[0].move(directions_abbrev[dir])
                break
            else:
                print(self.board)
                print("You can't move in this direction.")

    def move_neutron(self):
        print(f"You're moving the neutron")
        while True:
            dir = self._input_or_exit('Enter direction you want to move: ')
            if dir in self.board.neutron.possible_directions:
                self.board.neutron.move(dir)
                break
            elif dir in directions_abbrev.keys():
                self.board.neutron.move(directions_abbrev[dir])
                break
            else:
                print(self.board)
                print(f"You can't move in this direction")
