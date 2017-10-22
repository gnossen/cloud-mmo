class UpdateMessage:
    def __init__(self, elapsed_time, frame_duration):
        self.elapsed_time = elapsed_time
        self.frame_duration = frame_duration

class BlitMessage:
    def __init__(self, camera):
        self.camera = camera

class KeyEventMessage:
    def __init__(self, event):
        self.event = event

class DamageMessage:
    def __init__(self, bounds, force, exclude):
        self.bounds = bounds
        self.force = force
        self.exclude = exclude

class InflictDamageMessage(DamageMessage):
    def to_take_msg(self):
        return TakeDamageMessage(self.bounds, self.force, self.exclude)

class TakeDamageMessage(DamageMessage):
    pass
