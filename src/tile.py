import numpy as np
import pygame

class Tile:
    def __init__(self, kind=0, tile_size=32)
        self._kind = kind

    def blit(self, screen, screen_pos):
        pygame.draw.rect(screen,
                         self._color(),
                         (screen_pos[0], screen_pos[1], tile_size, tile_size),
                         0)

class TileMap:
    def __init__(self, size, tile_size=32):
        self._size = size
        self._tile_size = 32
        self._tiles = [[Tile(tile_size=self._tile_size) for _ in range(size[0])] for _ in range(size[1])]

    def set(position, tile):
        if any(list(position > size)) or any(list(position < np.array(0, 0))):
            msg = "Cannot set tile at position {}. Out of bounds".format(list(position))
            raise Exception(msg)
        self._tiles[position[0]][position[1]]

    def blit(self, screen):
        base_pos = np.array(0, 0)
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                tile_pos = base_pos + self._tile_size * np.array(x, y)
                self._tiles[x, y].blit(screen, tile_pos)
