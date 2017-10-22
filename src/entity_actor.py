from actor import Actor
from entity import *
from message import *
import random
import math
from directions import *
from key_state import *
from entity_msg import *

class EntityActor(Actor):
    TOTAL_BOUNCEBACK_TIME = 0.25
    MAX_BOUNCEBACK_SPEED = 500
    DAMAGE_COLOR = np.array([255, 0, 0])

    def __init__(self, parent, color, entity, executor=None):
        super().__init__(parent, executor=executor)
        self._base_color = color
        self._entity = entity
        self._invincibility_period = 0.0
        self._bounceback_duration = 0.0
        self._bounceback_direction = np.array([0.0, 0.0])

    def entity(self):
        raise Exception("Abstract method!")

    def receive(self, msg, sender):
        if isinstance(msg, UpdateMessage):
            self.update(msg)
        if isinstance(msg, BlitMessage):
            self.blit(msg)
        if isinstance(msg, GetEntity):
            return self._entity
        if isinstance(msg, TakeDamageMessage):
            if self not in msg.exclude and self._entity.bounds().intersects(msg.bounds) and self._invincibility_period <= 0.0:
                self._invincibility_period = 1.0
                self.bounceback(msg.bounds.center(), msg.force)
        if isinstance(msg, InflictDamageMessage):
            self.hoist(msg)

    def bounceback(self, source, force):
        self._bounceback_duration = self.TOTAL_BOUNCEBACK_TIME
        self._move_duration = 0.0
        diff_vec = self._entity.center() - source
        pos_component = diff_vec / np.linalg.norm(diff_vec)
        if np.count_nonzero(force) == 0:
            self._bounceback_direction = pos_component
        else:
            force_dir = force / np.linalg.norm(force)
            self._bounceback_direction = 0.8 * force_dir  + 0.2 * pos_component

    def _update_color(self, update_msg):
        color_diff = self._base_color - self.DAMAGE_COLOR
        color_coeff = (2.0 / (3.0 * math.sqrt(self.TOTAL_BOUNCEBACK_TIME) * self.TOTAL_BOUNCEBACK_TIME)) * color_diff
        color = (color_coeff * math.sqrt(self.TOTAL_BOUNCEBACK_TIME - self._bounceback_duration) * \
                    (self.TOTAL_BOUNCEBACK_TIME - self._bounceback_duration) + \
                    self.DAMAGE_COLOR).astype(int)
        self._entity.set_color(color)

    def _update_position(self, update_msg):
        coeff = self.MAX_BOUNCEBACK_SPEED / math.sqrt(self.TOTAL_BOUNCEBACK_TIME)
        speed = coeff * math.sqrt(self._bounceback_duration)
        delta = speed * update_msg.frame_duration * self._bounceback_direction
        self._entity.translate(delta)

    def update(self, update_msg):
        if self._invincibility_period > 0.0:
            self._invincibility_period -= update_msg.frame_duration
        if self._bounceback_duration > 0.0:
            self._update_color(update_msg)
            self._update_position(update_msg)
            self._bounceback_duration -= update_msg.frame_duration
        else:
            self._entity.set_color(self._base_color)

    def blit(self, blit_msg):
        raise Exception("Abstract method!")

class NpcActor(EntityActor):
    def __init__(self, parent, position=None, executor=None):
        base_color = np.array([random.randrange(256), random.randrange(256), random.randrange(256)])
        entity = NpcEntity(position, base_color)
        super().__init__(parent, base_color, entity, executor=executor)
        self._move_duration = 0.0
        self._direction = CARDINAL_DIRECTIONS["down"]

    def update(self, update_msg):
        super().update(update_msg)
        if self._move_duration <= 0.0:
            self._start_moving()
        self._move(update_msg.frame_duration)
        self._move_duration -= update_msg.frame_duration
        force_direction = np.array([0.0, 0.0])
        if self._bounceback_duration > 0:
            force_direction = self._bounceback_direction
        self.hoist(InflictDamageMessage(self._entity.bounds(), force_direction, [self]))

    def blit(self, blit_msg):
        self._entity.blit(blit_msg.camera)

    def _possible_directions(self):
        return list(CARDINAL_DIRECTIONS.values()) + ([np.array([0.0, 0.0])] * 5)

    def _start_moving(self):
        self._direction = random.choice(self._possible_directions())
        self._move_duration = random.gauss(3.0, 1.0)

    def _move(self, frame_duration):
        delta = 40.0 * frame_duration * self._direction
        self._entity.translate(delta)

class PlayerActor(EntityActor):
    def __init__(self, parent, position, executor=None):
        entity = PlayerEntity(position)
        self._dir_key_state = DirectionKeyState()
        self._sword = None
        super().__init__(parent, entity._color, entity, executor=executor)

    def receive(self, msg, sender):
        if isinstance(msg, KeyEventMessage):
            self._update_keys(msg)
        return super().receive(msg, sender)

    def blit(self, blit_msg):
        self._entity.blit(blit_msg.camera)
        if self._sword:
            self.send(blit_msg, self._sword)

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
        self._sword = SwordActor(self, 20 * facing_direction, facing_direction)

    def _move(self, frame_duration):
        direction = self._dir_key_state.movement_direction()
        delta = 120.0 * frame_duration * direction
        self._entity.translate(delta)

    def update(self, update_msg):
        super().update(update_msg)
        self._update_sword(update_msg)
        if not self._sword:
            self._move(update_msg.frame_duration)

class SwordActor(Actor):
    def __init__(self, parent, offset, direction, executor=None):
        super().__init__(parent, executor=executor)
        self._size = None
        if direction[0] == 0.0:
            self._size = np.array([10, 25])
        else:
            self._size = np.array([25, 10])
        self._offset = offset
        position = self.get_position()
        self._entity = SwordEntity(position, self._size)
        self._direction = direction
        self._lifetime = 0.3

    def get_position(self):
        return self.ask(GetEntity(), self.parent()).result().center() + self._offset - 0.5 * self._size

    def receive(self, msg, sender):
        if isinstance(msg, UpdateMessage):
            self.update(msg)
            self.hoist(InflictDamageMessage(self._entity.bounds(), self._direction, [self.parent()]))
        elif isinstance(msg, BlitMessage):
            self._entity.blit(msg.camera)
        elif isinstance(msg, GetEntity):
            return self._entity

    def update(self, msg):
        self._lifetime -= msg.frame_duration
        self._entity.move_to(self.get_position())

    def dead(self):
        return self._lifetime <= 0.0
