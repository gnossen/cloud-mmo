import sys
import pygame
import numpy as np
import camera_actor
import random
from actor import *
from entity_actor import *
import entity_msg
from message import *
from tilemap_actor import *

class RootActor(Actor):
    def __init__(self, executor):
        super().__init__(None, executor)
        self._npcs = [NpcActor(self, np.array([random.randrange(320), random.randrange(320)])) for i in range(7)]
        self._player = PlayerActor(self, np.array([30, 30]))
        self._camera = camera_actor.CameraActor(self, np.array([800, 800]))
        self._tilemap = TileMapActor(np.array([20, 20]), self)

    def receive(self, message, sender):
        if isinstance(message, UpdateMessage):
            self.update(message)
        elif isinstance(message, BlitMessage):
            self.blit()

    def update(self, update_msg):
        self.update_external()
        for child in self.children():
            self.send(update_msg, child)
        player_entity = self.ask(entity_msg.GetEntity(), self._player).result()
        center_msg = camera_actor.CenterOn(player_entity.center())
        self.send(center_msg, self._camera)
        self.send(camera_actor.Reset(), self._camera)

    def update_external(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)

        for event in events:
            msg = KeyEventMessage(event)
            for child in self.children():
                self.await(self.send(msg, child))

    def blit(self):
        camera_obj = self.ask(camera_actor.GetCamera(), self._camera).result()
        blit_msg = BlitMessage(camera_obj)
        self.send(blit_msg, self._tilemap)
        for npc in self._npcs:
            self.send(blit_msg, npc)
        self.send(blit_msg, self._player)
        pygame.display.flip()
