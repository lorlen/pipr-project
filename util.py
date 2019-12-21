class Vec:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @staticmethod
    def from_numpy(numpy_pos):
        return Vec(numpy_pos[1], numpy_pos[0])

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def _make_iter(self):
        yield self.y
        yield self.x

    def __iter__(self):
        return self._make_iter()


class Soldier:
    EMPTY = 0
    NEUTRON = 1
    WHITE = 2
    BLACK = 3


directions = {
    'north': Vec(0, -1),
    'east': Vec(1, 0),
    'south': Vec(0, 1),
    'west': Vec(-1, 0) 
}