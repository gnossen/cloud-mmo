from tile import *
from actor import *
from message import *
from tilemap_msg import *

class TileMapActor(Actor):
    def __init__(self, size, parent, executor=None):
        super().__init__(parent, executor)
        self._tilemap = DevTileMap(size)

    def receive(self, msg, sender):
        if isinstance(msg, BlitMessage):
            self._tilemap.blit(msg.camera)
        elif isinstance(msg, SetMessage):
            self._tilemap.set(msg.position, msg.tile_type)
