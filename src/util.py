class Vec:
    """
    A very simple implementation of a 2D vector, used to facilitate operations
    on positions and directions.

    Args:
        x (int): vector's x coordinate.
        y (int): vector's y coordinate.
    """
    __slots__ = 'x', 'y'

    def __init__(self, x, y):
        self.x, self.y = int(x), int(y)

    @staticmethod
    def fromtuple(tuple_pos):
        """
        Creates a :class:`Vec` from tuple (y, x). This order of coordinates
        was chosen to be compatible with NumPy's way of indexing
        multidimensional arrays.

        Args:
            tuple_pos (tuple):
                a (y, x) tuple representing vector's coordinates.

        Returns:
            Vec: a newly created Vec.
        """
        return Vec(tuple_pos[1], tuple_pos[0])

    def __eq__(self, other):
        return other is not None and tuple(self) == tuple(other)

    def __hash__(self):
        return hash(tuple(self))

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def _make_iter(self):
        yield self.y
        yield self.x

    def __iter__(self):
        return self._make_iter()

    def __str__(self):
        return f'({self.x}, {self.y})'


class Color:
    WHITE = 2
    BLACK = 3
    color_names = {
        WHITE: 'white',
        BLACK: 'black'
    }


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

directions_abbrev = {
    'n': 'north',
    'ne': 'northeast',
    'e': 'east',
    'se': 'southeast',
    's': 'south',
    'sw': 'southwest',
    'w': 'west',
    'nw': 'northwest',
}
