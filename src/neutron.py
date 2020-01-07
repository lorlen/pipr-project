import itertools
import textwrap
import numpy as np
from colorama import Fore, Back, Style

from util import Vec, Color, directions


class Soldier:
    """
    Class representing a soldier on the board.

    Its main task is to enforce proper movement rules, to prevent the board
    from getting into an invalid state from the point of view of the game's
    rules.

    Args:
        board (neutron.NeutronBoard): home board of this Soldier.
        position (util.Vec): position of this Soldier on the board.
        color (int): color of this Soldier.
    """
    def __init__(self, board, position, color):
        self._board = board
        self.pos = position
        self.color = color

    @property
    def possible_directions(self):
        """List of directions this Soldier can move

        Works by checking for which directions :func:`NeutronBoard.furthest_empty_spot`
        """
        return [
            dir
            for dir in directions
            if self._board.furthest_empty_spot(self.pos, dir) is not None
        ]

    @property
    def possible_moves(self):
        """
        List of positions this Soldier can be after one move.

        Works by supplying :func:`NeutronBoard.furthest_empty_spot` with all
        possible directions, then filtering out ``None`` results.
        """
        return filter(None, [
            self._board.furthest_empty_spot(self.pos, dir)
            for dir in directions
        ])

    def move(self, direction):
        """
        Tries to move this ``Soldier`` in the given direction.

        For this method to succeed, the direction given must be present in
        ``self.possible_directions``.

        Works by calling :func:`NeutronBoard.furthest_empty_spot`, setting
        the position returned by this function to this Soldier's color,
        and the original position to 0.

        Args:
            direction (str): direction in which to move this Soldier.

        Raises:
            ValueError: if the given direction is not in
            self.possible_directions.
        """
        if direction not in self.possible_directions:
            raise ValueError('not possible to move in this direction')
        dst = self._board.furthest_empty_spot(self.pos, direction)
        self._board.grid[tuple(dst)] = self.color
        self._board.grid[tuple(self.pos)] = 0
        self.pos = dst


class Neutron(Soldier):
    """
    A special case of a :class:`Soldier`.

    A ``Neutron`` is different from a ``Soldier`` only by having a unique color
    value.
    """
    VALUE = 1

    def __init__(self, board, position):
        super().__init__(board, position, self.VALUE)


class NeutronBoard:
    """
    The Neutron game board.

    It is represented by a 5x5 NumPy array. The purpose of this class is to
    manage the array, ensuring it doesn't get into an invalid state, and to
    provide useful functions for the game's logic.

    Args:
        starting_grid (:class:`numpy.array`): array representing starting
        board data.

    Attributes:
        grid (numpy.array): the array containing raw data of this board.
        white_soldiers (list): list of Soldier objects representing white soldiers.
        black_soldiers (list): list of Soldier objects representing black soldiers.
    """
    def __init__(self, starting_grid=None):
        if not isinstance(starting_grid, np.ndarray):
            starting_grid = np.array(starting_grid)
        if starting_grid.shape != (5, 5):
            raise ValueError(f'Invalid game board shape: {starting_grid.shape}')
        self.grid = np.array(starting_grid) if starting_grid is not None else np.array([
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

        self.neutron = Neutron(self, Vec.fromtuple(
                       next(zip(*np.where(self.grid == Neutron.VALUE)))))

    def get_soldiers(self, color):
        """
        Get all soldiers of a given color present on the board.

        Args:
            color (int): color of the soldiers.

        Returns:
            list: a list of Soldier objects containing all soldiers of a given color.

        Raises:
            ValueError: if the color given is not a valid soldier color
        """
        if color == Color.WHITE:
            return self.white_soldiers
        elif color == Color.BLACK:
            return self.black_soldiers
        else:
            raise ValueError('invalid soldier color')

    def furthest_empty_spot(self, pos, dir):
        """
        Get the furthest empty position one can get by moving in direction
        ``dir`` from position ``pos`` without colliding with anything.

        Implemented as a while loop checking following conditions:

        * if the position after a step in the given direction is still in
          the board's bounds,

        * if the position after the step is empty.

        While those conditions are met, the step is performed, adding direction
        to position.
        If, after executing the loop, the resulting position is different from
        the starting position, we return it. Else, the move could not be made,
        and we return ``None``.

        Args:
            pos (util.Vec): starting position.
            dir (str or util.Vec): direction in which to move.

        Returns:
            util.Vec: position of the furthest empty spot in the line of sight
            of source position, or ``None`` if the movement cannot be made.
        """
        orig_pos = pos
        if not isinstance(dir, Vec):
            dir = directions[dir]
        # we check if the position would still be in the board's bounds even
        # after we move one step in the given direction
        while (0 <= (pos + dir).x < len(self.grid[pos.y])) \
                and (0 <= (pos + dir).y < len(self.grid)) \
                and self.grid[tuple(pos + dir)] == 0:
            pos += dir
        return pos if pos != orig_pos else None

    def neighbors(self, pos):
        """
        Get values of board cells neighboring cell with position ``pos``.

        It iterates over coordinates from x-1 to x+1 and y-1 to y+1, making
        sure they are not out of the bounds of the board, and appends values
        at those positions to the resulting list. The source position itself
        is not included.

        Args:
            pos (util.Vec): position of the cell.

        Returns:
            list: list of neighboring cells' values, without the source cell
        """
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
    """
    The main Neutron game class.

    Args:
        first_player (player.Player): the player who will start the game
        second_player (player.Player): the second player
    """
    def __init__(self, first_player, second_player):
        self.board = NeutronBoard()
        self.players = itertools.cycle([first_player, second_player])
        self.current_player = next(self.players)
        self.winner = None
        self.initial_round = True

    def start(self):
        """
        Starts the game, playing rounds until the game is won by either of
        the players.
        """
        while not self.winner:
            self.play_round()

        print(self.board)
        print(f'{Color.color_names[self.winner]} player won the game!'.capitalize())

    def play_round(self):
        """Plays one round, swapping players afterwards."""
        if not self.initial_round:
            self.current_player.move_neutron(self.board)
            if self.check_won():
                return

        self.current_player.move_soldier(self.board)
        if self.check_won():
            return

        self.initial_round = False
        self.current_player = next(self.players)

    def check_won(self):
        """
        Checks if the game was won, updating self.winner variable with the
        color of the winning player.

        Returns:
            int: winning player's color
        """
        if all(neighbor != 0 for neighbor in self.board.neighbors(self.board.neutron.pos)):
            self.winner = self.current_player.color
        elif self.board.neutron.pos.y == 0:
            self.winner = Color.BLACK
        elif self.board.neutron.pos.y == 4:
            self.winner = Color.WHITE
        return self.winner
