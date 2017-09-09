import sys
import pygame
import tile
import numpy as np
import camera
import time

class timed_loop:
    def __init__(self, fps):
        self._fps = fps

    def __call__(self, f):
        desired_period = 1.0 / self._fps
        start_time = time.time()
        while True:
            frame_start = time.time()
            elapsed_time = frame_start - start_time
            f(elapsed_time)
            frame_duration = time.time() - frame_start
            time.sleep(max(0, desired_period - elapsed_time))

cam = camera.Camera(np.array([400, 400]))

tilemap = tile.DevTileMap(np.array([15, 15]))

@timed_loop(60.0)
def main(elapsed_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    cam.move_to(elapsed_time * np.array([-10.0, 0]))

    cam.reset()
    tilemap.blit(cam)
    pygame.display.flip()

main()
