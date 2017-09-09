import numpy as np
import pygame
import camera
import bounds

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

class PlayerEntity(DevEntity):
    def __init__(self, position):
        super().__init__((63, 127, 255), np.array([30, 30]), position)

    def update(self, elapsed_time, frame_duration, keys):
        direction = np.array([0.0, 0.0])
        if keys[pygame.K_UP]:
            direction += np.array([0.0, -1.0])
        if keys[pygame.K_DOWN]:
            direction += np.array([0.0, 1.0])
        if keys[pygame.K_LEFT]:
            direction += np.array([-1.0, 0.0])
        if keys[pygame.K_RIGHT]:
            direction += np.array([1.0, 0.0])
        if not (direction[0] == 0.0 and direction[1] == 0.0):
            direction = (1.0 / np.linalg.norm(direction)) * direction
        delta = 90.0 * frame_duration * direction
        self.translate(delta)
