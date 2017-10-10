import numpy as np
import pygame
import camera
import bounds
import random

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
                         (screen_pos[0], screen_pos[1], self._size[0], self._size[0]),
                         0)

    def update(self, elapsed_time, keys):
        raise Exception("Abstract method! What the hell are you doing?")

class NpcEntity(DevEntity):
    DIRECTIONS = [
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, -1.0]),
        np.array([0.0, 1.0]),
        np.array([-1.0, 0.0]),
        np.array([1.0, 0.0])
    ]

    def __init__(self, position):
        color = np.array([random.randrange(256), random.randrange(256), random.randrange(256)])
        size = np.array([30, 30])
        super().__init__(color, size, position)
        self._direction = self.DIRECTIONS[0]
        self._move_duration = 0.0

    def _start_moving(self):
        self._direction = random.choice(self.DIRECTIONS)
        self._move_duration = random.gauss(3.0, 1.0)

    def _move(self, frame_duration):
        delta = 40.0 * frame_duration * self._direction
        self.translate(delta)

    def update(self, elapsed_time, frame_duration, events):
        if self._move_duration < 0:
            self._start_moving()
        self._move(frame_duration)
        self._move_duration -= frame_duration

class PlayerEntity(DevEntity):
    ARROW_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
    DIRECTIONS = [
        np.array([0.0, -1.0]),
        np.array([0.0, 1.0]),
        np.array([-1.0, 0.0]),
        np.array([1.0, 0.0])
    ]

    def __init__(self, position):
        super().__init__((63, 127, 255), np.array([30, 30]), position)
        self._keys = [False] * len(self.ARROW_KEYS)

    def _update_keys(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.ARROW_KEYS:
                    self._keys[self.ARROW_KEYS.index(event.key)] = True
            elif event.type == pygame.KEYUP:
                if event.key in self.ARROW_KEYS:
                    self._keys[self.ARROW_KEYS.index(event.key)] = False

    def _move(self, frame_duration):
        direction = np.array([0.0, 0.0])
        for key, card_dir in zip(self._keys, self.DIRECTIONS):
            if key:
                direction += card_dir
        if not (direction[0] == 0.0 and direction[1] == 0.0):
            direction = (1.0 / np.linalg.norm(direction)) * direction
        delta = 90.0 * frame_duration * direction
        self.translate(delta)

    def update(self, elapsed_time, frame_duration, events):
        self._update_keys(events)
        self._move(frame_duration)
