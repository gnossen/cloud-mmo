import sys
import pygame
import tile
import numpy as np
import camera
import time
import entity
import random

class timed_loop:
    def __init__(self, fps):
        self._fps = fps

    def __call__(self, f):
        desired_period = 1.0 / self._fps
        frame_duration = 0.0
        start_time = time.time()
        while True:
            frame_start = time.time()
            elapsed_time = frame_start - start_time
            f(elapsed_time, frame_duration)
            frame_duration = time.time() - frame_start
            time.sleep(max(0, desired_period - elapsed_time))

cam = camera.Camera(np.array([400, 400]))
tilemap = tile.DevTileMap(np.array([10, 10]))
player = entity.PlayerEntity(np.array([30, 30]))

npcs = []
for _ in range(7):
    position = np.array([random.randrange(320), random.randrange(320)])
    npc = entity.NpcEntity(position)
    npcs.append(npc)

keys = [False for _ in range(512)]
@timed_loop(60.0)
def main(elapsed_time, frame_duration):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False

    player.update(elapsed_time, frame_duration, keys)
    cam.center_on(player.center())

    cam.reset()
    tilemap.blit(cam)
    player.blit(cam)
    for npc in npcs:
        npc.blit(cam)
    pygame.display.flip()

main()
