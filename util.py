class Vec:
    def __init__(self, x, y):
        self.x, self.y = int(x), int(y)

    @staticmethod
    def fromtuple(numpy_pos):
        return Vec(numpy_pos[1], numpy_pos[0])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def _make_iter(self):
        yield self.y
        yield self.x

    def __iter__(self):
        return self._make_iter()

    def __str__(self):
        return f'({self.x}, {self.y})'


directions = {
    'north': Vec(0, -1),
    'northeast': Vec(1, -1),
    'east': Vec(1, 0),
    'southeast': Vec(1, 1),
    'south': Vec(0, 1),
    'southwest': Vec(-1, 1),
    'west': Vec(-1, 0),
    'northwest': Vec(-1, -1)
}


class Color:
    WHITE = 2
    BLACK = 3
    color_names = {
        WHITE: 'white',
        BLACK: 'black'
    }
