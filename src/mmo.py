import sys
import pygame
import tile
import numpy as np
import camera
import time

cam = camera.Camera(np.array([400, 400]))

fps = 60
desired_time = 1.0 / fps

tilemap = tile.DevTileMap(np.array([15, 15]))
counter = 0
app_start = time.time()
while True:
    frame_start = time.time()
    elapsed_time = frame_start - app_start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    cam.move_to(elapsed_time * np.array([-10.0, 0]))

    cam.reset()
    tilemap.blit(cam)
    pygame.display.flip()
    frame_duration = time.time() - frame_start
    time.sleep(max(0, desired_time - elapsed_time))
    counter += 1
