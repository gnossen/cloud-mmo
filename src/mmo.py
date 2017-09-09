import sys
import pygame
import tile
import numpy as np

screen = pygame.display.set_mode((400, 400))

tilemap = tile.DevTileMap(np.array([15, 15]))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill((0, 0, 0))
    tilemap.blit(screen)
    pygame.display.flip()
