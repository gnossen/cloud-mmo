import sys
import pygame
import tile
import numpy as np
import camera

cam = camera.Camera(np.array([400, 400]))

tilemap = tile.DevTileMap(np.array([15, 15]))
counter = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    if counter % 50 == 0:
        cam.translate(np.array([-1, 0]))

    cam.reset()
    tilemap.blit(cam)
    pygame.display.flip()
    counter += 1
