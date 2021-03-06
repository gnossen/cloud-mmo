import numpy as np
import pygame
import bounds

class Tile:
    def __init__(self, kind=0, tile_size=32):
        self._kind = kind
        self._tile_size = tile_size

    def _color(self):
        if self._kind == 0:
            return (64, 64, 64)
        elif self._kind == 1:
            return (64, 255, 64)
        elif self._kind == 2:
            return (244, 64, 96)
        else:
            return (0, 255, 0)

    def blit(self, screen, screen_pos):
        pygame.draw.rect(screen,
                         self._color(),
                         (screen_pos[0], screen_pos[1], self._tile_size, self._tile_size),
                         0)

class TileMap:
    def __init__(self, size, tile_size=32):
        self._size = size
        self._tile_size = 32
        self._tiles = [[Tile(tile_size=self._tile_size) for _ in range(size[0])] for _ in range(size[1])]

    def set(self, position, tile):
        if any(list(position > self._size)) or any(list(position < np.array([0, 0]))):
            msg = "Cannot set tile at position {}. Out of bounds".format(list(position))
            raise TypeError(msg)
        self._tiles[position[0]][position[1]] = tile

    def blit(self, camera):
        camera_bounds = camera.bounds()
        raw_start = np.floor(camera.position() / self._tile_size).astype(int)
        start = np.maximum(raw_start, np.array([0, 0]))
        count = np.ceil(camera.size() / self._tile_size).astype(int)
        end = np.minimum(start + count, self._size).astype(int)
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                tile_pos = self._tile_size * np.array([x, y])
                self._tiles[x][y].blit(camera.screen(), tile_pos - camera.position())

class DevTileMap(TileMap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_map()

    def _init_map(self):
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                if (x + y) % 2 == 0:
                    self.set(np.array([x, y]), Tile(kind=1, tile_size=self._tile_size))
                else:
                    self.set(np.array([x, y]), Tile(kind=0, tile_size=self._tile_size))
