from actor import Actor
from entity import *
from message import *
import random
from directions import *
from key_state import *
from entity_msg import *

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
        elif isinstance(msg, GetEntity):
            return self._entity

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

class PlayerActor(Actor):
    def __init__(self, parent, position, executor=None):
        self._entity = PlayerEntity(position)
        self._dir_key_state = DirectionKeyState()
        self._sword = None
        super().__init__(parent, executor=executor)

    def receive(self, msg, sender):
        if isinstance(msg, UpdateMessage):
            self.update(msg)
        elif isinstance(msg, BlitMessage):
            self._entity.blit(msg.camera)
            if self._sword:
                self.send(msg, self._sword)
        elif isinstance(msg, KeyEventMessage):
            self._update_keys(msg)
        elif isinstance(msg, GetEntity):
            return self._entity

    def _update_sword(self, update_msg):
        if self._sword is not None and self._sword.dead():
            self._sword = None
        if self._sword is not None:
            self.send(update_msg, self._sword)

    def _update_keys(self, msg):
        self._dir_key_state.update(msg.event)
        if msg.event.type == pygame.KEYDOWN and msg.event.key == pygame.K_SPACE:
            if not self._sword:
                self._instantiate_sword()

    def _instantiate_sword(self):
        facing_direction = self._dir_key_state.facing_direction()
        self._sword = SwordActor(self, self._entity.center() + 20 * facing_direction, facing_direction)

    def _move(self, frame_duration):
        direction = self._dir_key_state.movement_direction()
        delta = 90.0 * frame_duration * direction
        self._entity.translate(delta)

    def update(self, update_msg):
        self._update_sword(update_msg)
        if not self._sword:
            self._move(update_msg.frame_duration)

class SwordActor(Actor):
    def __init__(self, parent, position, direction, executor=None):
        self._entity = SwordEntity(position, direction)
        self._lifetime = 0.5
        super().__init__(parent, executor=executor)

    def receive(self, msg, sender):
        if isinstance(msg, UpdateMessage):
            self.update(msg)
        elif isinstance(msg, BlitMessage):
            self._entity.blit(msg.camera)
        elif isinstance(msg, GetEntity):
            return self._entity

    def update(self, msg):
        self._lifetime -= msg.frame_duration

    def dead(self):
        return self._lifetime <= 0.0
