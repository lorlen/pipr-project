from neutron import NeutronBoard
from util import Vec

def test_move():
    board = NeutronBoard([
        [2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ])

    soldier = board.white_soldiers[0]

    soldier.move('east')
    assert soldier.pos == (0, 4)
    soldier.move('south')
    assert soldier.pos == (4, 4)
    soldier.move('west')
    assert soldier.pos == (4, 0)
    soldier.move('north')
    assert soldier.pos == (0, 0)
    soldier.move('southeast')
    assert soldier.pos == (4, 4)
    soldier.move('northwest')
    assert soldier.pos == (0, 0)
    soldier.move('east')
    soldier.move('southwest')
    assert soldier.pos == (4, 0)
    soldier.move('northeast')
    assert soldier.pos == (0, 4)

def test_neighbors():
    board = NeutronBoard([
        [0, 2, 0, 1, 0],
        [3, 1, 2, 3, 2],
        [0, 8, 0, 4, 0],
        [6, 7, 6, 5, 4],
        [0, 8, 0, 6, 0],
    ])
    assert set(board.neighbors(Vec(2, 2))) == {1, 2, 3, 4, 5, 6, 7, 8}
    assert set(board.neighbors(Vec(0, 0))) == {1, 2, 3}
    assert set(board.neighbors(Vec(4, 0))) == {1, 2, 3}
    assert set(board.neighbors(Vec(4, 4))) == {4, 5, 6}
    assert set(board.neighbors(Vec(0, 4))) == {6, 7, 8}
