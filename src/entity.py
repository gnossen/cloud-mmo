import numpy as np
import pygame
import camera
import bounds
import random
from directions import *
from key_state import *

class Entity:
    def __init__(self, size, position):
        self._size = size
        self._position = position.astype(float)

    def move_to(self, position):
        self._position = position.astype(float)

    def center(self):
        return self._position + 0.5 * self._size

    def translate(self, delta):
        self._position += delta

    def position(self):
        return self._position.astype(int)

    def bounds(self):
        return bounds.Bounds(self._position, self._size)

    def intersects(self, other):
        return self.bounds().intersects(other.bounds())

    def blit(self, camera):
        raise Exception("Abstract method! What the hell are you doing?")

    def update(self, events):
        pass

class DevEntity(Entity):
    def __init__(self, color, size, position):
        super().__init__(size, position)
        self._color = color

    def blit(self, camera):
        screen_pos = self._position - camera.position()
        pygame.draw.rect(camera.screen(),
                         self._color,
                         (screen_pos[0], screen_pos[1], self._size[0], self._size[1]),
                         0)

    def update(self, elapsed_time, keys):
        raise Exception("Abstract method! What the hell are you doing?")

class NpcEntity(DevEntity):
    def __init__(self, position):
        color = np.array([random.randrange(256), random.randrange(256), random.randrange(256)])
        size = np.array([30, 30])
        super().__init__(color, size, position)

class PlayerEntity(DevEntity):
    def __init__(self, position):
        super().__init__((63, 127, 255), np.array([30, 30]), position)
        self._dir_key_state = DirectionKeyState()
        self._sword_entity = None

class SwordEntity(DevEntity):
    def __init__(self, position, direction):
        size = None
        if direction[0] == 0.0:
            size = np.array([10, 25])
        else:
            size = np.array([25, 10])
        super().__init__((255, 255, 255), size, position - 0.5 * size)
