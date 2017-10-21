from camera import *
from actor import *

class CameraMessage:
    pass

class MoveTo(CameraMessage):
    def __init__(self, position):
        self.position = position

class CenterOn(CameraMessage):
    def __init__(self, position):
        self.position = position

class Translate(CameraMessage):
    def __init__(self, delta):
        self.position = delta

class Reset(CameraMessage):
    pass

class GetCamera(CameraMessage):
    pass

class CameraActor(Actor):
    def __init__(self, parent, size):
        super().__init__(parent)
        self._camera = Camera(size)

    def receive(self, message, sender):
        if isinstance(message, GetCamera):
            return self._camera
        elif isinstance(message, MoveTo):
            self._camera.move_to(message.position)
        elif isinstance(message, CenterOn):
            self._camera.center_on(message.position)
        elif isinstance(message, Translate):
            self._camera.translate(message.delta)
        elif isinstance(message, Reset):
            self._camera.reset()
