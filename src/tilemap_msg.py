class TileMapMessage:
    pass

class SetMessage(TileMapMessage):
    def __init__(self, position, tile_type):
        self.position = position
        self.tile_type = tile_type
