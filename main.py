#!/usr/bin/env python3

from neutron import NeutronGame
from player import HumanPlayer, RandomPlayer
from util import Color

if __name__ == '__main__':
    player1, player2 = RandomPlayer(Color.WHITE), HumanPlayer(Color.BLACK)
    game = NeutronGame(player1, player2)
    game.start()