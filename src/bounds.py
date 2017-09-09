import numpy as np

def in_range(x, a, b):
    return x >= a and x <= b

class Bounds:
    def __init__(self, position, size):
        self._position = position
        self._size = size

    def _vertically_intersects(self, other):
        return in_range(self.top(), other.top(), other.bottom()) or \
                in_range(self.bottom(), other.top(), other.bottom())

    def _horizontally_intersects(self, other):
        return in_range(self.left(), other.left(), other.right()) or \
                in_range(self.right(), other.left(), other.right())

    def _is_partially_contained(self, other):
        return self._vertically_intersects(other) and \
                self._horizontally_intersects(other)

    def intersects(self, other):
        return self._is_partially_contained(other) or \
                other._is_partially_contained(self)

    def top(self):
        return self._position[1]

    def bottom(self):
        return self._position[1] + self._size[1]

    def left(self):
        return self._position[0]

    def right(self):
        return self._position[0] + self._size[0]
