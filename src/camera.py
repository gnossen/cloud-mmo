import numpy as np
import pygame
import bounds

class Camera:
    def __init__(self, size, position=np.array([0, 0])):
        self._position = position
        self._size = size
        self._screen = pygame.display.set_mode((self._size[0], self._size[1]))

    def screen(self):
        return self._screen

    def move_to(self, position):
        self._position = position

    def center_on(self, pos):
        self.move_to(pos - 0.5 * self._size)

    def translate(self, delta):
        self._position += delta

    def reset(self):
        self._screen.fill((0, 0, 0))

    def position(self):
        return self._position.astype(int)

    def size(self):
        return self._size.astype(int)

    def bounds(self):
        return bounds.Bounds(self.position(), self._size)
