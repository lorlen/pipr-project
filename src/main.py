#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap

from neutron import NeutronGame, NeutronBoard
from player import HumanPlayer, RandomPlayer, StrategyPlayer
from util import Color

if __name__ == '__main__':
    parser = ArgumentParser(description=textwrap.dedent("""
        User Guide

        The game, upon start, presents the player a 5x5 grid. The top and
        bottom rows are home rows of the respective players.

        When there's the player's turn, the game prints what exactly the
        player is supposed to move (the neutron or a regular soldier),
        and then asks to provide the position of a soldier they want to move.
        It should be first the row letter, and then the column number, e.g.
        A1. Those letters and numbers are written on the edges of the board to
        help the player visualize it. If the position is invalid or is not a
        position of one of the player's soldiers, the game asks again. Then it
        asks for a direction in which to move the soldier. It should be one of
        standard compass directions, e.g. 'north' or 'southwest'.

        If the information provided by player is correct, the move is executed
        and the computer player takes its turn. The updated grid state
        displayed takes into account moves of both the human and the computer
        player.

        When either of the players executes a winning move, the final state of
        the board, alongside with the message who won the game, is printed,
        and the game exits.
    """), formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--color', choices=['black', 'white'],
                        default='black',
                        help="Color of player's soldiers. Defaults to black")
    parser.add_argument('-f', '--first', choices=['computer', 'human'],
                        default='human', help="Defines who should start the \
                        game: computer or human player.")
    parser.add_argument('-p', '--player-type', choices=['random', 'strategy'],
                        default='strategy', help="Sets the preferred player \
                        type: random, which makes random movements, and \
                        strategy, which makes decisions based on rules.")
    args = parser.parse_args()

    board = NeutronBoard()
    player_constructor = StrategyPlayer if args.player_type == 'strategy' \
        else RandomPlayer
    computer = player_constructor(
        board,
        Color.WHITE if args.color == 'black' else Color.BLACK,
        4 if args.color == 'black' else 0
    )
    human = HumanPlayer(
        board,
        Color.WHITE if args.color == 'white' else Color.BLACK,
        4 if args.color == 'white' else 0
    )
    game = NeutronGame(
        board,
        computer if args.first == 'computer' else human,
        computer if args.first == 'human' else human
    )
    try:
        game.start()
    except KeyboardInterrupt:
        pass
