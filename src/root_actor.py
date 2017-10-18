import sys
import pygame
import numpy as np
import camera
import entity
import random
import tile
from actor import *
from message import *

class RootActor(Actor):
    def __init__(self, executor):
        # self._player = PlayerActor(self)
        self._camera = camera.Camera(np.array([800, 800]))
        self._tilemap = tile.DevTileMap(np.array([20, 20]))
        # self._npcs = [NpcActor(self, np.array([np.randrange(320), np.randrange(320)])) for i in range(7)]
        super().__init__(None, executor)

    def receive(self, message, sender):
        if isinstance(message, UpdateMessage):
            self.update(message)
        elif isinstance(message, BlitMessage):
            self.blit()

    def update(self, update_msg):
        self.update_external()
        # for child in self.children():
        #     self.await(self.send(update_msg, child))
        # self._camera.center_on(player.center())
        # self._camera.reset()

    def update_external(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)

        # for event in events:
        #     msg = KeyEventMessage(event)
        #     for child in self.children():
        #         self.await(self.send(msg, child))

    def blit(self):
        # how do we handle ordering of child entities for blitting?
        self._tilemap.blit(self._camera)
        # for child in self.children():
        #     self.await(self.send(BlitMessage(self._camera)))
        pygame.display.flip()