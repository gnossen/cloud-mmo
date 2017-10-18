import numpy as np
import pygame
import camera
import bounds
import random
from directions import *

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

class KeyState:
    def __init__(self, key_codes):
        self._key_codes = key_codes
        self._key_states = [False] * len(key_codes)

    def state(self, key_code):
        return self._key_states[self._key_codes.index(key_code)]

    def update(self, events):
        for event in events:
            self._update(event)

    def _update(self, event):
        self._update_key(event, pygame.KEYDOWN, True)
        self._update_key(event, pygame.KEYUP, False)

    def _update_key(self, event, event_type, key_state):
        if event.type == event_type and event.key in self.PYGAME_DIRECTIONS:
            self._key_states[self._key_codes.index(event.key)] = key_state

class DirectionKeyState(KeyState):
    PYGAME_DIRECTIONS = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right"
    }

    def __init__(self):
        self._facing_direction = CARDINAL_DIRECTIONS["down"]
        super().__init__(list(self.PYGAME_DIRECTIONS.keys()))

    def _update(self, event):
        super()._update(event)
        if len([elem for elem in self._key_states if elem]) == 1:
            dir_index = self._key_states.index(True)
            dir_code = self._key_codes[dir_index]
            self._facing_direction = CARDINAL_DIRECTIONS[self.PYGAME_DIRECTIONS[dir_code]]

    def facing_direction(self):
        return self._facing_direction

    def movement_direction(self):
        d = np.array([0.0, 0.0])
        for key, dir_name in self.PYGAME_DIRECTIONS.items():
            dir_vec = CARDINAL_DIRECTIONS[dir_name]
            if self.state(key):
                d += dir_vec
        if not (d[0] == 0.0 and d[1] == 0.0):
            d = (1.0 / np.linalg.norm(d)) * d
        return d

class PlayerEntity(DevEntity):
    def __init__(self, position):
        super().__init__((63, 127, 255), np.array([30, 30]), position)
        self._dir_key_state = DirectionKeyState()
        self._sword_entity = None

    def _update_keys(self, events):
        self._dir_key_state.update(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not self._sword_entity:
                    self._instantiate_sword()

    def _instantiate_sword(self):
        facing_direction = self._dir_key_state.facing_direction()
        self._sword_entity = SwordEntity(self.center() + 20 * facing_direction, facing_direction)

    def _move(self, frame_duration):
        direction = self._dir_key_state.movement_direction()
        delta = 90.0 * frame_duration * direction
        self.translate(delta)

    def blit(self, camera):
        super().blit(camera)
        if self._sword_entity is not None:
            self._sword_entity.blit(camera)

    def update(self, elapsed_time, frame_duration, events):
        if self._sword_entity is not None and self._sword_entity.dead():
            self._sword_entity = None
        self._update_keys(events)
        if not self._sword_entity:
            self._move(frame_duration)
        if self._sword_entity is not None:
            self._sword_entity.update(elapsed_time, frame_duration, events)

class SwordEntity(DevEntity):
    def __init__(self, position, direction):
        size = None
        if direction[0] == 0.0:
            size = np.array([10, 25])
        else:
            size = np.array([25, 10])
        super().__init__((255, 255, 255), size, position - 0.5 * size)
        self._lifetime = 0.5

    def update(self, elapsed_time, frame_duration, events):
        self._lifetime -= frame_duration

    def dead(self):
        return self._lifetime <= 0.0
