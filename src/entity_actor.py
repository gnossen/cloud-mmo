from actor import Actor
from entity import *
from message import *
import random
from directions import *

class NpcActor(Actor):
    def __init__(self, parent, position=None, executor=None):
        self._entity = NpcEntity(position)
        self._move_duration = 0.0
        self._direction = CARDINAL_DIRECTIONS["down"]
        super().__init__(parent, executor=executor)

    def receive(self, msg, sender):
        if isinstance(msg, UpdateMessage):
            self.update(msg.frame_duration)
        elif isinstance(msg, BlitMessage):
            self._entity.blit(msg.camera)

    def update(self, frame_duration):
        if self._move_duration < 0:
            self._start_moving()
        self._move(frame_duration)
        self._move_duration -= frame_duration

    def _possible_directions(self):
        return list(CARDINAL_DIRECTIONS.values()) + ([np.array([0.0, 0.0])] * 5)

    def _start_moving(self):
        self._direction = random.choice(self._possible_directions())
        self._move_duration = random.gauss(3.0, 1.0)

    def _move(self, frame_duration):
        delta = 40.0 * frame_duration * self._direction
        self._entity.translate(delta)

