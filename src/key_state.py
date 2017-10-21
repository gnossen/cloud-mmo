from directions import *
import numpy as np
import pygame

class KeyState:
    def __init__(self, key_codes):
        self._key_codes = key_codes
        self._key_states = [False] * len(key_codes)

    def state(self, key_code):
        return self._key_states[self._key_codes.index(key_code)]

    def update(self, event):
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

    def update(self, event):
        super().update(event)
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
