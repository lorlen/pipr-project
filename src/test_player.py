from neutron import NeutronBoard
from player import StrategyPlayer
from util import Color


def test_block_enemy_row():
    board = NeutronBoard([
        [3, 0, 0, 3, 3],
        [3, 0, 0, 0, 0],
        [2, 0, 1, 0, 3],
        [0, 0, 0, 0, 0],
        [0, 2, 2, 2, 2],
    ])
    player = StrategyPlayer(board, Color.WHITE, 4)
    player.move_soldier()
    assert board.grid[0, 2] == 2


def test_block_neutron():
    board = NeutronBoard([
        [3, 0, 0, 0, 0],
        [0, 3, 3, 3, 0],
        [0, 3, 1, 2, 0],
        [0, 0, 2, 2, 0],
        [2, 0, 0, 0, 2],
    ])
    player = StrategyPlayer(board, Color.WHITE, 4)
    player.move_soldier()
    assert board.grid[3, 1] == 2


def test_move_into_home():
    board = NeutronBoard([
        [3, 3, 3, 3, 3],
        [2, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 2, 2, 2, 2],
    ])
    player = StrategyPlayer(board, Color.WHITE, 4)
    player.move_neutron()
    assert board.grid[4, 0] == 1


def test_avoid_enemy_row():
    for _ in range(10):
        board = NeutronBoard([
            [3, 0, 0, 0, 3],
            [3, 0, 0, 0, 3],
            [0, 0, 1, 0, 3],
            [0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2],
        ])
        player = StrategyPlayer(board, Color.WHITE, 4)
        player.move_neutron()
        assert all(board.grid[0, x] == 0 for x in range(1, 4))
