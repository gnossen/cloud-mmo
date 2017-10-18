from actor import Actor
from entity import *
from message import *
import random


class NpcActor(Actor):
    DIRECTIONS = [
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, 0.0]),
        np.array([0.0, -1.0]),
        np.array([0.0, 1.0]),
        np.array([-1.0, 0.0]),
        np.array([1.0, 0.0])
    ]

    def __init__(self, parent, executor, position=None):
        self._entity = NpcEntity(position)
        self._move_duration = 0.0
        self._direction = self.DIRECTIONS[0]
        super().__init__(parent, executor)

    def receive(self, message, sender):
        if isinstance(message, UpdateMessage):
            self.update(message.frame_duration)
        elif isinstance(message, BlitMessage):
            self.entity.blit(message.camera)

    def update(self, frame_duration):
        if self._move_duration < 0:
            self._start_moving()
        self._move(frame_duration)
        self._move_duration -= frame_duration

    def _start_moving(self):
        self._direction = random.choice(self.DIRECTIONS)
        self._move_duration = random.gauss(3.0, 1.0)

    def _move(self, frame_duration):
        delta = 40.0 * frame_duration * self._direction
        self._entity.translate(delta)

